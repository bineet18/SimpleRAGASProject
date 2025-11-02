from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
from dotenv import load_dotenv

from metrics import METRIC_REGISTRY, METRICS_WITH_GROUND_TRUTH, ASPECT_CRITIC_METRICS

# Load environment variables
load_dotenv()

app = FastAPI(title="RAGAS Metrics API", version="1.0.0")

# Initialize LLM and embeddings from environment variables
def initialize_models():
    """Initialize OpenAI models from environment variables"""
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables. "
            "Please create a .env file with your OpenAI API key. "
            "See .env.example for template."
        )
    
    # Set API key in environment for libraries
    os.environ["OPENAI_API_KEY"] = api_key
    
    try:
        llm = ChatOpenAI(
            model=model_name,
            temperature=0
        )
        embeddings = OpenAIEmbeddings()
        print(f"✅ Models initialized successfully with {model_name}")
        return llm, embeddings
    except Exception as e:
        raise ValueError(f"Failed to initialize OpenAI models: {str(e)}")

# Initialize models on startup
try:
    llm, embeddings = initialize_models()
except ValueError as e:
    print(f"❌ Error: {str(e)}")
    print("The API will start but won't be functional until you set the environment variables.")
    llm, embeddings = None, None

class EvaluateRequest(BaseModel):
    """Request model for evaluation"""
    question: str = Field(..., description="User's question/input")
    answer: str = Field(..., description="Chatbot's response")
    ground_truth: Optional[str] = Field(None, description="Expected answer (required for some metrics)")
    metrics: List[str] = Field(..., description="List of metrics to evaluate")

class EvaluateResponse(BaseModel):
    """Response model for evaluation"""
    scores: Dict[str, float] = Field(..., description="Metric scores")
    errors: Optional[Dict[str, str]] = Field(None, description="Any errors during evaluation")

@app.get("/")
async def root():
    """Health check endpoint"""
    status = "ready" if (llm and embeddings) else "not_configured"
    return {
        "status": status, 
        "service": "RAGAS Metrics API",
        "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo") if llm else None
    }

@app.get("/metrics")
async def list_metrics():
    """List all available metrics with their types"""
    metrics_info = []
    for metric_name in METRIC_REGISTRY.keys():
        metric_info = {
            "name": metric_name,
            "requires_ground_truth": metric_name in METRICS_WITH_GROUND_TRUTH,
            "type": "aspect_critic" if metric_name in ASPECT_CRITIC_METRICS else "standard",
            "output": "binary (0 or 1)" if metric_name in ASPECT_CRITIC_METRICS else "score (0.0 to 1.0)"
        }
        if metric_name in ASPECT_CRITIC_METRICS:
            # Add aspect description
            from metrics.aspect_critic import ASPECT_DEFINITIONS
            metric_info["description"] = ASPECT_DEFINITIONS.get(metric_name, "")
        metrics_info.append(metric_info)
    return {"metrics": metrics_info}

@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(request: EvaluateRequest):
    """Evaluate chatbot response using specified metrics"""
    
    # Check if models are initialized
    if llm is None or embeddings is None:
        raise HTTPException(
            status_code=503, 
            detail="Service not configured. Please set OPENAI_API_KEY in .env file and restart the server."
        )
    
    # Validate metrics
    invalid_metrics = [m for m in request.metrics if m not in METRIC_REGISTRY]
    if invalid_metrics:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid metrics: {invalid_metrics}. Use /metrics endpoint to see available metrics"
        )
    
    # Check if ground_truth is required
    needs_ground_truth = any(m in METRICS_WITH_GROUND_TRUTH for m in request.metrics)
    if needs_ground_truth and not request.ground_truth:
        missing = [m for m in request.metrics if m in METRICS_WITH_GROUND_TRUTH]
        raise HTTPException(
            status_code=400,
            detail=f"Metrics {missing} require ground_truth field"
        )
    
    # Prepare data
    data = {
        "question": request.question,
        "answer": request.answer
    }
    if request.ground_truth:
        data["ground_truth"] = request.ground_truth
    
    # Calculate metrics
    scores = {}
    errors = {}
    
    for metric_name in request.metrics:
        try:
            # Get metric class
            metric_class = METRIC_REGISTRY[metric_name]
            
            # Initialize metric
            metric = metric_class(llm=llm, embeddings=embeddings)
            
            # Calculate score
            score = metric.calculate(data)
            scores[metric_name] = float(score)
            
        except Exception as e:
            errors[metric_name] = str(e)
    
    # Prepare response
    response = {"scores": scores}
    if errors:
        response["errors"] = errors
    
    return response

@app.post("/evaluate-batch")
async def evaluate_batch(
    questions: List[str],
    answers: List[str],
    ground_truths: Optional[List[str]] = None,
    metrics: List[str] = ["answer_relevancy"]
):
    """Evaluate multiple responses in batch"""
    
    # Check if models are initialized
    if llm is None or embeddings is None:
        raise HTTPException(
            status_code=503, 
            detail="Service not configured. Please set OPENAI_API_KEY in .env file and restart the server."
        )
    
    # Validate input lengths
    if len(questions) != len(answers):
        raise HTTPException(
            status_code=400,
            detail="Questions and answers must have the same length"
        )
    
    if ground_truths and len(ground_truths) != len(questions):
        raise HTTPException(
            status_code=400,
            detail="Ground truths must have the same length as questions"
        )
    
    # Process batch
    results = []
    for i in range(len(questions)):
        request = EvaluateRequest(
            question=questions[i],
            answer=answers[i],
            ground_truth=ground_truths[i] if ground_truths else None,
            metrics=metrics
        )
        result = await evaluate(request)
        results.append(result)
    
    return {"results": results, "count": len(results)}

if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Check if port is provided as command line argument
    port = 8000  # default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}. Using default port 8000.")
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", port))
    
    print(f"Starting RAGAS API on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)