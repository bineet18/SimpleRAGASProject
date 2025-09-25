# RAGAS Backend API

A FastAPI-based evaluation service for RAG (Retrieval-Augmented Generation) systems using the RAGAS framework. This API provides comprehensive metrics to assess the quality of RAG pipelines.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key and/or Anthropic API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ragas-backend-api
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
chmod +x quickstart.sh  # Make script executable (if using quickstart.sh)
source quickstart.sh
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:
```env
# OpenAI Configuration (Required for embeddings)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Configuration (Optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Default Settings
DEFAULT_PROVIDER=openai
DEFAULT_LLM_MODEL=gpt-4
DEFAULT_EMBEDDING_MODEL=text-embedding-3-small

# Model Settings
MODEL_TEMPERATURE=0.0
MODEL_MAX_TOKENS=1000

# API Settings
API_PORT=8072
API_HOST=0.0.0.0
```

### Starting the Server

**Option 1: Using the main script (Recommended)**
```bash
python main.py
```

**Option 2: Using uvicorn directly**
```bash

uvicorn app:app --host 0.0.0.0 --port 8072 --reload
uvicorn app:app --host 0.0.0.0 --port 8072 --reload --loop asyncio
```

**Option 3: For development with auto-reload**
```bash
uvicorn app:app --reload --host localhost --port 8072
```

The server will start at `http://localhost:8072`

## 📊 Available Metrics

### Retrieval Metrics
- `context_precision` - Measures precision of retrieved contexts
- `context_precision_with_ref` - Context precision with reference
- `context_recall` - Measures recall of retrieved contexts

### Generation Metrics
- `faithfulness` - Measures factual consistency between response and contexts
- `answer_relevancy` - Measures relevance of the answer to the question
- `answer_accuracy` - Evaluates accuracy against reference answer

### Similarity Metrics
- `semantic_similarity` - Semantic similarity between response and reference
- `bleu_score` - BLEU score for text similarity
- `rouge_score` - ROUGE score for text overlap

## 🔌 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API info |
| `/health` | GET | Health check |
| `/metrics` | GET | List all available metrics |
| `/metrics/requirements` | GET | Get required fields for each metric |
| `/evaluate` | POST | Evaluate metrics for given data |
| `/models` | GET | List supported models |
| `/config` | GET | Get current configuration |

## 📝 API Usage Examples

### Basic Evaluation Request

```bash
curl -X POST "http://localhost:8072/evaluate" \
-H "Content-Type: application/json" \
-d '{
  "data": {
    "user_input": "What is the capital of France?",
    "response": "The capital of France is Paris.",
    "reference": "Paris is the capital of France.",
    "retrieved_contexts": ["Paris is the capital and largest city of France."]
  },
  "metrics": ["faithfulness", "answer_relevancy", "context_precision"]
}'
```

### Python Example

```python
import requests

# API endpoint
url = "http://localhost:8072/evaluate"

# Evaluation data
payload = {
    "data": {
        "user_input": "What is machine learning?",
        "response": "Machine learning is a subset of AI that enables systems to learn from data.",
        "reference": "Machine learning is a branch of artificial intelligence focused on building systems that learn from data.",
        "retrieved_contexts": [
            "Machine learning is a subset of artificial intelligence.",
            "ML systems learn patterns from data without explicit programming."
        ]
    },
    "metrics": ["faithfulness", "answer_accuracy", "semantic_similarity"],
    "evaluation_config": {
        "provider": "openai",
        "evaluator_llm": "gpt-4",
        "embeddings": "text-embedding-3-small"
    }
}

# Make request
response = requests.post(url, json=payload)
print(response.json())
```

## 🤖 Supported Models

### OpenAI Models
**LLM Models:**
- gpt-4
- gpt-3.5-turbo
- gpt-4-turbo

**Embedding Models:**
- text-embedding-ada-002
- text-embedding-3-small
- text-embedding-3-large

### Anthropic Models
**LLM Models:**
- claude-3-opus-20240229
- claude-3-sonnet-20240229
- claude-3-haiku-20240307

*Note: Anthropic doesn't provide embeddings, OpenAI embeddings are used*

## 📊 Metric Requirements

Each metric requires specific fields in the evaluation data:

### Retrieval Metrics
- **context_precision**: `user_input`, `response`, `retrieved_contexts`
- **context_recall**: `user_input`, `reference`, `retrieved_contexts`

### Generation Metrics
- **faithfulness**: `user_input`, `response`, `retrieved_contexts`
- **answer_relevancy**: `user_input`, `response`
- **answer_accuracy**: `user_input`, `response`, `reference`

### Similarity Metrics
- **semantic_similarity**: `response`, `reference` (requires embeddings)
- **bleu_score**: `response`, `reference`
- **rouge_score**: `response`, `reference`

## 🔍 Testing the API

### Check if server is running
```bash
curl http://localhost:8072/health
```

### List available metrics
```bash
curl http://localhost:8072/metrics
```

### Get metric requirements
```bash
curl http://localhost:8072/metrics/requirements
```

## 🛠️ Development

### Project Structure
```
ragas-backend-api/
├── app.py                  # Main FastAPI application
├── main.py                 # Entry point script
├── config.py              # Configuration management
├── models.py              # Model manager for LLM/embeddings
├── metrics/               # Metric implementations
│   ├── __init__.py
│   ├── retrieval_metrics.py
│   ├── generation_metrics.py
│   └── similarity_metrics.py
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
└── README.md            # This file
```

### Running Tests
```python
# Test basic functionality
python -c "from config import config; config.validate()"
```

### Debug Mode
Set environment variable for detailed logging:
```bash
export PYTHONUNBUFFERED=1
python main.py
```

## ⚙️ Configuration Details

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Yes (for embeddings) |
| `ANTHROPIC_API_KEY` | Anthropic API key | - | No |
| `DEFAULT_PROVIDER` | Default LLM provider | openai | No |
| `DEFAULT_LLM_MODEL` | Default LLM model | gpt-4 | No |
| `DEFAULT_EMBEDDING_MODEL` | Default embedding model | text-embedding-3-small | No |
| `MODEL_TEMPERATURE` | Model temperature | 0.0 | No |
| `MODEL_MAX_TOKENS` | Max tokens for response | 1000 | No |
| `API_PORT` | API server port | 8072 | No |
| `API_HOST` | API server host | 0.0.0.0 | No |

## 🚨 Troubleshooting

### Common Issues

**1. API Key Error**
```
ValueError: OpenAI API key not configured
```
**Solution:** Ensure your `.env` file contains valid API keys

**2. Module Not Found**
```
ModuleNotFoundError: No module named 'ragas'
```
**Solution:** Install dependencies: `pip install -r requirements.txt`

**3. Port Already in Use**
```
[Errno 48] Address already in use
```
**Solution:** Change port in `.env` or kill existing process

**4. Connection Refused**
```
ConnectionError: Connection refused
```
**Solution:** Ensure server is running and check firewall settings

## 📈 Performance Tips

1. **Model Caching**: The API caches model instances for better performance
2. **Parallel Processing**: Metrics are calculated concurrently when possible
3. **Batch Requests**: Group multiple evaluations in a single request (coming soon)
4. **Connection Pooling**: Reuse HTTP connections for multiple requests

## 📄 License

[Your License Here]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainers.

---

**Note:** This API is designed for evaluation purposes. Ensure you have appropriate API credits for the LLM providers you're using, as evaluation can consume significant API calls depending on the metrics and data volume.