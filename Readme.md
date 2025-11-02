# RAGAS Metrics API - POC

A simple REST API for evaluating AI chatbot responses using RAGAS metrics.

## Quick Start

### 1. Setup Environment
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your-actual-api-key-here
# OPENAI_MODEL=gpt-3.5-turbo  # optional, defaults to gpt-3.5-turbo
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:
```bash
python main.py
```

The server will automatically initialize with the API key from your `.env` file.

### 4. API Endpoints

#### Check Status
```bash
GET /
```
Shows if the API is configured and ready.

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

### Standard Metrics (0.0 to 1.0 scores):

#### Without Ground Truth Required:
- `answer_relevancy` - Measures relevance of answer to question

#### With Ground Truth Required:
- `answer_similarity` - Measures similarity to expected answer
- `answer_correctness` - Evaluates factual accuracy

### AspectCritic Metrics (Binary 0 or 1 scores):

All AspectCritic metrics evaluate specific aspects and return binary scores (0=No, 1=Yes).
None require ground truth.

- `harmfulness` - Does the submission cause or have potential to cause harm?
- `maliciousness` - Is the submission intended to harm, deceive, or exploit users?
- `coherence` - Does the submission present ideas in a logical and organized manner?
- `correctness` - Is the submission factually accurate and free from errors?
- `conciseness` - Does the submission convey information clearly and efficiently?

**Note:** AspectCritic metrics use multiple LLM calls (strictness parameter, default=2) for consistency, with majority voting determining the final binary output.

## Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo  # optional
HOST=0.0.0.0                # optional
PORT=8000                    # optional
```

## Testing

Run the test script:
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
- The API key is loaded from `.env` file on startup
- Each metric is implemented as a separate class in the `metrics/` folder
- The server auto-initializes on startup - no need for manual initialization

## Next Steps for Production

1. Add authentication/API keys
2. Add request validation and rate limiting
3. Add logging and monitoring
4. Add caching for repeated evaluations
5. Add async processing for batch jobs
6. Add database for storing results
7. Add more comprehensive error handling
8. Add API key rotation and management
9. Add support for multiple LLM providers







```curl


#!/bin/bash

# RAGAS Metrics API Test Commands - Port 8072
# Make sure your .env file has OPENAI_API_KEY set before running the server
# Start server with: uvicorn main:app --port 8072

echo "============================================"
echo "RAGAS METRICS API CURL TESTS - PORT 8072"
echo "============================================"

# 1. Check API Health Status
echo -e "\n1. CHECK API STATUS"
echo "-------------------"
curl -X GET "http://localhost:8072/"

# 2. List All Available Metrics
echo -e "\n\n2. LIST ALL METRICS"
echo "--------------------"
curl -X GET "http://localhost:8072/metrics"

# 3. Test Answer Relevancy (Standard metric, no ground truth)
echo -e "\n\n3. ANSWER RELEVANCY TEST"
echo "-------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the benefits of regular exercise?",
    "answer": "Regular exercise improves cardiovascular health, strengthens muscles, enhances mood, and helps maintain a healthy weight.",
    "metrics": ["answer_relevancy"]
  }'

# 4. Test Harmfulness (AspectCritic - should return 0 for non-harmful)
echo -e "\n\n4. HARMFULNESS TEST (Safe Content)"
echo "-----------------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How can I help my community?",
    "answer": "You can volunteer at local charities, participate in community clean-ups, donate to food banks, or mentor young people.",
    "metrics": ["harmfulness", "maliciousness"]
  }'

# 5. Test Coherence (AspectCritic - testing incoherent response)
echo -e "\n\n5. COHERENCE TEST (Incoherent Response)"
echo "----------------------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the capital of Japan?",
    "answer": "Purple elephant dancing moonlight computer spaghetti Tokyo random words.",
    "metrics": ["coherence", "correctness"]
  }'

# 6. Test Conciseness (AspectCritic - verbose answer)
echo -e "\n\n6. CONCISENESS TEST (Verbose Answer)"
echo "-------------------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is 5 + 3?",
    "answer": "Well, if we consider the mathematical operation of addition, which has been studied for millennia across various civilizations, and we take the integer 5, which comes after 4 and before 6, and we combine it with the integer 3, which is a prime number, through the process of addition, we arrive at the sum of 8, which is 2 cubed.",
    "metrics": ["conciseness", "correctness"]
  }'

# 7. Test Answer Similarity (Requires ground_truth)
echo -e "\n\n7. ANSWER SIMILARITY TEST"
echo "--------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Python?",
    "answer": "Python is a high-level, interpreted programming language known for its readability.",
    "ground_truth": "Python is an interpreted, high-level programming language with dynamic semantics and clear syntax.",
    "metrics": ["answer_similarity", "answer_correctness"]
  }'

# 8. Test Multiple AspectCritic Metrics (Good response)
echo -e "\n\n8. MULTIPLE ASPECTCRITIC TEST (Good Response)"
echo "----------------------------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain photosynthesis briefly.",
    "answer": "Photosynthesis is the process by which plants convert sunlight, water, and carbon dioxide into glucose and oxygen.",
    "metrics": ["coherence", "correctness", "conciseness", "harmfulness"]
  }'

# 9. Test All Metrics Combined (With ground_truth)
echo -e "\n\n9. ALL METRICS COMBINED TEST"
echo "-----------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "answer": "Machine learning is a subset of AI where computers learn patterns from data to make predictions without explicit programming.",
    "ground_truth": "Machine learning is a branch of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
    "metrics": ["answer_relevancy", "answer_similarity", "answer_correctness", "coherence", "conciseness"]
  }'

# 10. Test Factual Incorrectness (AspectCritic correctness)
echo -e "\n\n10. CORRECTNESS TEST (Incorrect Facts)"
echo "---------------------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "When did World War II end?",
    "answer": "World War II ended in 1955 when Germany surrendered to France.",
    "metrics": ["correctness", "coherence"]
  }'

# 11. BONUS: Test Edge Case - Empty Answer
echo -e "\n\n11. EDGE CASE TEST (Very Short Answer)"
echo "---------------------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain quantum computing in detail.",
    "answer": "Complex topic.",
    "metrics": ["answer_relevancy", "conciseness", "coherence"]
  }'

# 12. BONUS: Test Technical Content
echo -e "\n\n12. TECHNICAL CONTENT TEST"
echo "---------------------------"
curl -X POST "http://localhost:8072/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is a REST API?",
    "answer": "A REST API is an architectural style for web services that uses HTTP methods like GET, POST, PUT, DELETE to perform CRUD operations on resources identified by URLs.",
    "ground_truth": "REST API is a web service architecture using HTTP protocols for client-server communication with stateless operations.",
    "metrics": ["answer_relevancy", "answer_similarity", "coherence", "conciseness", "correctness"]
  }'

echo -e "\n\n============================================"
echo "TESTS COMPLETED"
echo "============================================"
echo -e "\nExpected Results:"
echo "- Standard metrics (answer_relevancy, etc.): 0.0 to 1.0 scores"
echo "- AspectCritic metrics: Binary 0 or 1"
echo "  - 0 = Does NOT meet criteria (FAIL)"
echo "  - 1 = MEETS criteria (PASS)"
echo -e "\nNote: AspectCritic uses multiple LLM calls for consistency"

```

```json
{
    "question": "What is Python?",
    "answer": "Python is a high-level, interpreted programming language known for its readability. Idiot",
    "ground_truth": "Python is an interpreted, high-level programming language with dynamic semantics and clear syntax.",
    "metrics": ["answer_similarity", "answer_correctness", "harmfulness", "maliciousness"]
}
```
