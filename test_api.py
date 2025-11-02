import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    """Test the RAGAS API with sample data"""
    
    # Step 1: Initialize with OpenAI API key
    print("1. Initializing...")
    init_response = requests.post(
        f"{BASE_URL}/initialize",
        json={
            "openai_api_key": "YOUR_OPENAI_API_KEY_HERE",  # Replace with actual key
            "model": "gpt-3.5-turbo"
        }
    )
    print(f"   Status: {init_response.status_code}")
    print(f"   Response: {init_response.json()}\n")
    
    # Step 2: List available metrics
    print("2. Available metrics:")
    metrics_response = requests.get(f"{BASE_URL}/metrics")
    print(f"   {json.dumps(metrics_response.json(), indent=2)}\n")
    
    # Step 3: Evaluate without ground truth
    print("3. Evaluating without ground truth...")
    eval_response = requests.post(
        f"{BASE_URL}/evaluate",
        json={
            "question": "What is the capital of France?",
            "answer": "The capital of France is Paris, which is known for the Eiffel Tower.",
            "metrics": ["answer_relevancy", "coherence", "conciseness"]
        }
    )
    print(f"   Status: {eval_response.status_code}")
    print(f"   Scores: {json.dumps(eval_response.json(), indent=2)}\n")
    
    # Step 4: Evaluate with ground truth
    print("4. Evaluating with ground truth...")
    eval_response = requests.post(
        f"{BASE_URL}/evaluate",
        json={
            "question": "What is the capital of France?",
            "answer": "The capital of France is Paris.",
            "ground_truth": "Paris is the capital of France.",
            "metrics": ["answer_similarity", "answer_correctness"]
        }
    )
    print(f"   Status: {eval_response.status_code}")
    print(f"   Scores: {json.dumps(eval_response.json(), indent=2)}\n")
    
    # Step 5: Batch evaluation
    print("5. Batch evaluation...")
    batch_response = requests.post(
        f"{BASE_URL}/evaluate-batch",
        json={
            "questions": [
                "What is Python?",
                "What is machine learning?"
            ],
            "answers": [
                "Python is a programming language.",
                "Machine learning is a subset of AI that enables systems to learn from data."
            ],
            "metrics": ["answer_relevancy", "coherence"]
        }
    )
    print(f"   Status: {batch_response.status_code}")
    print(f"   Results: {json.dumps(batch_response.json(), indent=2)}\n")

if __name__ == "__main__":
    test_api()
