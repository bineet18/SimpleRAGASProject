import os
from dotenv import load_dotenv
from typing import Optional, Dict, List

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Default Models
    DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "openai")
    DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gpt-4")
    DEFAULT_EMBEDDING_MODEL = os.getenv("DEFAULT_EMBEDDING_MODEL", "text-embedding-ada-002")
    
    # Model Settings
    MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.0"))
    MODEL_MAX_TOKENS = int(os.getenv("MODEL_MAX_TOKENS", "1000"))
    
    # API Settings
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    
    # Supported Models
    SUPPORTED_MODELS = {
        "openai": {
            "llm": ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
            "embeddings": ["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"]
        },
        "anthropic": {
            "llm": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
            "embeddings": []  # Anthropic doesn't provide embeddings, will use OpenAI
        }
    }
    
    # Metric Requirements - which metrics need what models
    METRIC_REQUIREMENTS = {
        # Retrieval Metrics
        "context_precision": {"needs_llm": True, "needs_embeddings": False},
        "context_recall": {"needs_llm": True, "needs_embeddings": False},
        
        # Generation Metrics
        "faithfulness": {"needs_llm": True, "needs_embeddings": False},
        "answer_relevancy": {"needs_llm": True, "needs_embeddings": True},
        "answer_correctness": {"needs_llm": True, "needs_embeddings": False},
        
        # Similarity Metrics
        "semantic_similarity": {"needs_llm": False, "needs_embeddings": True},
        "bleu_score": {"needs_llm": False, "needs_embeddings": False},
        "rouge_score": {"needs_llm": False, "needs_embeddings": False}
    }

    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        errors = []
        
        if not cls.OPENAI_API_KEY and cls.DEFAULT_PROVIDER == "openai":
            errors.append("OPENAI_API_KEY is required when using OpenAI as default provider")
        
        if not cls.ANTHROPIC_API_KEY and cls.DEFAULT_PROVIDER == "anthropic":
            errors.append("ANTHROPIC_API_KEY is required when using Anthropic as default provider")
        
        # For embeddings, we always need OpenAI API key as Anthropic doesn't provide embeddings
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required for embedding models")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))
        
        return True

config = Config()