#!/bin/bash

# RAGAS API - cURL Examples

# 1. Initialize with OpenAI API Key
echo "Initializing..."
curl -X POST "http://localhost:8000/initialize" \
  -H "Content-Type: application/json" \
  -d '{
    "openai_api_key": "YOUR_OPENAI_API_KEY_HERE",
    "model": "gpt-3.5-turbo"
  }'

echo "\n\n"

# 2. List available metrics
echo "Available metrics:"
curl -X GET "http://localhost:8000/metrics"

echo "\n\n"

# 3. Evaluate without ground truth
echo "Evaluating without ground truth:"
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the capital of France?",
    "answer": "The capital of France is Paris, known for the Eiffel Tower.",
    "metrics": ["answer_relevancy", "coherence", "conciseness"]
  }'

echo "\n\n"

# 4. Evaluate with ground truth
echo "Evaluating with ground truth:"
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the capital of France?",
    "answer": "The capital of France is Paris.",
    "ground_truth": "Paris is the capital of France.",
    "metrics": ["answer_similarity", "answer_correctness"]
  }'

echo "\n"
