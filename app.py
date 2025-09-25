from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime
import traceback

from config import config
from models import model_manager
from metrics import RetrievalMetrics, GenerationMetrics, SimilarityMetrics, get_all_supported_metrics

# Initialize FastAPI app
app = FastAPI(
    title="RAGAS Evaluation API",
    description="API for evaluating RAG systems using RAGAS metrics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class EvalModelConfig(BaseModel):
    provider: Optional[str] = Field(default=None, description="Model provider (openai/anthropic)")
    evaluator_llm: Optional[str] = Field(default=None, description="LLM model name")
    embeddings: Optional[str] = Field(default=None, description="Embedding model name")

class EvaluationRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="Evaluation data")
    metrics: List[str] = Field(..., description="List of metrics to calculate")
    evaluation_config: Optional[EvalModelConfig] = Field(default=None, description="Model configuration")
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "data": {
                        "user_input": "What is the capital of France?",
                        "response": "The capital of France is Paris.",
                        "reference": "Paris is the capital of France.",
                        "retrieved_contexts": ["Paris is the capital and largest city of France."]
                    },
                    "metrics": ["faithfulness", "answer_relevancy", "context_precision"],
                    "evaluation_config": {
                        "provider": "openai",
                        "evaluator_llm": "gpt-4",
                        "embeddings": "text-embedding-ada-002"
                    }
                }
            ]
        }

class EvaluationResponse(BaseModel):
    status: str
    metrics: Dict[str, Optional[float]]
    metadata: Dict[str, Any]
    errors: Optional[List[str]] = None

# Metric evaluator class
class MetricEvaluator:
    def __init__(self):
        self.retrieval_handler = None
        self.generation_handler = None
        self.similarity_handler = None
    
    def initialize_handlers(self, llm, embeddings):
        """Initialize metric handlers with models"""
        self.retrieval_handler = RetrievalMetrics(llm=llm, embeddings=embeddings)
        self.generation_handler = GenerationMetrics(llm=llm, embeddings=embeddings)
        self.similarity_handler = SimilarityMetrics(llm=llm, embeddings=embeddings)
    
    async def evaluate(self, data: Dict[str, Any], metrics: List[str]) -> Dict[str, Optional[float]]:
        """Evaluate requested metrics"""
        results = {}
        
        # Group metrics by handler
        retrieval_metrics = [m for m in metrics if m in RetrievalMetrics.get_supported_metrics()]
        generation_metrics = [m for m in metrics if m in GenerationMetrics.get_supported_metrics()]
        similarity_metrics = [m for m in metrics if m in SimilarityMetrics.get_supported_metrics()]
        
        # Calculate metrics in parallel
        tasks = []
        
        if retrieval_metrics and self.retrieval_handler:
            tasks.append(self.retrieval_handler.calculate(data, retrieval_metrics))
        
        if generation_metrics and self.generation_handler:
            tasks.append(self.generation_handler.calculate(data, generation_metrics))
        
        if similarity_metrics and self.similarity_handler:
            tasks.append(self.similarity_handler.calculate(data, similarity_metrics))
        
        if tasks:
            metric_results = await asyncio.gather(*tasks)
            for result_dict in metric_results:
                results.update(result_dict)
        
        return results

# Global evaluator instance
evaluator = MetricEvaluator()

@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup"""
    try:
        config.validate()
        print("✅ Configuration validated successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "RAGAS Evaluation API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics")
async def list_metrics():
    """List all available metrics"""
    return {
        "retrieval_metrics": RetrievalMetrics.get_supported_metrics(),
        "generation_metrics": GenerationMetrics.get_supported_metrics(),
        "similarity_metrics": SimilarityMetrics.get_supported_metrics(),
        "all_metrics": get_all_supported_metrics()
    }

@app.get("/metrics/requirements")
async def metric_requirements():
    """Get required fields for each metric"""
    return {
        "retrieval": RetrievalMetrics.get_metric_requirements(),
        "generation": GenerationMetrics.get_metric_requirements(),
        "similarity": SimilarityMetrics.get_metric_requirements()
    }

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_metrics(request: EvaluationRequest):
    """Evaluate metrics for given data"""
    start_time = datetime.utcnow()
    errors = []
    
    try:
        # Get model configuration
        eval_config = request.evaluation_config or EvalModelConfig()
        
        # Get LLM and embeddings
        llm = model_manager.get_llm(
            provider=eval_config.provider,
            model_name=eval_config.evaluator_llm
        )
        
        embeddings = None
        if eval_config.embeddings:
            embeddings = model_manager.get_embeddings(model_name=eval_config.embeddings)
        else:
            # Try to get default embeddings
            try:
                embeddings = model_manager.get_embeddings()
            except:
                pass  # Some metrics don't need embeddings
        
        # Initialize handlers
        evaluator.initialize_handlers(llm, embeddings)
        
        # Validate metrics
        supported_metrics = get_all_supported_metrics()
        invalid_metrics = [m for m in request.metrics if m not in supported_metrics]
        if invalid_metrics:
            errors.append(f"Unsupported metrics: {invalid_metrics}")
        
        valid_metrics = [m for m in request.metrics if m in supported_metrics]
        
        # Evaluate metrics
        results = await evaluator.evaluate(request.data, valid_metrics)
        
        # Calculate metadata
        end_time = datetime.utcnow()
        execution_time = (end_time - start_time).total_seconds()
        
        metrics_calculated = [k for k, v in results.items() if v is not None]
        metrics_skipped = [k for k, v in results.items() if v is None]
        
        metadata = {
            "execution_time": execution_time,
            "models_used": {
                "evaluator_llm": f"{eval_config.provider or config.DEFAULT_PROVIDER}/{eval_config.evaluator_llm or config.DEFAULT_LLM_MODEL}",
                "embeddings": f"openai/{eval_config.embeddings or config.DEFAULT_EMBEDDING_MODEL}" if embeddings else None
            },
            "metrics_calculated": len(metrics_calculated),
            "metrics_skipped": metrics_skipped,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return EvaluationResponse(
            status="success",
            metrics=results,
            metadata=metadata,
            errors=errors if errors else None
        )
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List available models"""
    return config.SUPPORTED_MODELS

@app.get("/config")
async def get_configuration():
    """Get current configuration (without sensitive data)"""
    return {
        "default_provider": config.DEFAULT_PROVIDER,
        "default_llm_model": config.DEFAULT_LLM_MODEL,
        "default_embedding_model": config.DEFAULT_EMBEDDING_MODEL,
        "supported_models": config.SUPPORTED_MODELS
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)