# RAGAS Metrics API - POC

A simple REST API for evaluating AI chatbot responses using RAGAS metrics.

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:
```bash
python main.py
```

### 3. API Endpoints

#### Initialize (Required First)
```bash
POST /initialize
{
    "openai_api_key": "your-api-key",
    "model": "gpt-3.5-turbo"  # optional
}
```

#### List Available Metrics
```bash
GET /metrics
```

#### Evaluate Response
```bash
POST /evaluate
{
    "question": "What is Python?",
    "answer": "Python is a programming language",
    "ground_truth": "Python is a high-level programming language",  # optional
    "metrics": ["answer_relevancy", "coherence"]
}
```

#### Batch Evaluation
```bash
POST /evaluate-batch
{
    "questions": ["Q1", "Q2"],
    "answers": ["A1", "A2"],
    "ground_truths": ["GT1", "GT2"],  # optional
    "metrics": ["answer_relevancy"]
}
```

## Available Metrics

### Without Ground Truth Required:
- `answer_relevancy` - Measures relevance of answer to question
- `coherence` - Evaluates logical flow
- `conciseness` - Checks if response is appropriately brief
- `harmfulness` - Checks for harmful content

### With Ground Truth Required:
- `answer_similarity` - Measures similarity to expected answer
- `answer_correctness` - Evaluates factual accuracy

## Testing

Run the test script (update API key first):
```bash
python test_api.py
```

## Response Format

All evaluation endpoints return:
```json
{
    "scores": {
        "metric_name": 0.85,
        "another_metric": 0.92
    },
    "errors": {  // optional
        "failed_metric": "Error message"
    }
}
```

## Notes

- This is a POC version - keep it simple
- All metrics return scores between 0-1 (higher is better)
- The API key is required for OpenAI's GPT model (used as evaluator)
- Each metric is implemented as a separate class in the `metrics/` folder

## Next Steps for Production

1. Add authentication/API keys
2. Add request validation and rate limiting
3. Add logging and monitoring
4. Add caching for repeated evaluations
5. Add async processing for batch jobs
6. Add database for storing results
7. Add more comprehensive error handling
