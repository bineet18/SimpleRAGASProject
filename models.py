from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from config import config

class ModelManager:
    """Manages LLM and Embedding model instances"""
    
    def __init__(self):
        self.config = config
        self._llm_cache: Dict[str, Any] = {}
        self._embedding_cache: Dict[str, Any] = {}
        self._initialize_default_models()
    
    def _initialize_default_models(self):
        """Pre-initialize default models for faster first request"""
        try:
            # Initialize default LLM
            self.get_llm()
            # Initialize default embeddings
            self.get_embeddings()
        except Exception as e:
            print(f"Warning: Could not initialize default models: {e}")
    
    def get_llm(self, provider: Optional[str] = None, model_name: Optional[str] = None):
        """Get LLM instance based on provider and model name"""
        provider = provider or self.config.DEFAULT_PROVIDER
        model_name = model_name or self.config.DEFAULT_LLM_MODEL
        
        # Check if model is supported
        if provider not in self.config.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported provider: {provider}")
        
        if model_name not in self.config.SUPPORTED_MODELS[provider]["llm"]:
            raise ValueError(f"Unsupported model '{model_name}' for provider '{provider}'")
        
        # Check cache
        cache_key = f"{provider}_{model_name}"
        if cache_key in self._llm_cache:
            return self._llm_cache[cache_key]
        
        # Create new instance
        if provider == "openai":
            if not self.config.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not configured")
            
            llm = ChatOpenAI(
                model=model_name,
                temperature=self.config.MODEL_TEMPERATURE,
                max_tokens=self.config.MODEL_MAX_TOKENS,
                api_key=self.config.OPENAI_API_KEY
            )
        elif provider == "anthropic":
            if not self.config.ANTHROPIC_API_KEY:
                raise ValueError("Anthropic API key not configured")
            
            llm = ChatAnthropic(
                model=model_name,
                temperature=self.config.MODEL_TEMPERATURE,
                max_tokens=self.config.MODEL_MAX_TOKENS,
                api_key=self.config.ANTHROPIC_API_KEY
            )
        else:
            raise ValueError(f"Provider '{provider}' not implemented")
        
        # Wrap for RAGAS
        wrapped_llm = LangchainLLMWrapper(llm)
        self._llm_cache[cache_key] = wrapped_llm
        
        return wrapped_llm
    
    def get_embeddings(self, model_name: Optional[str] = None):
        """Get embeddings instance (currently only OpenAI supported)"""
        model_name = model_name or self.config.DEFAULT_EMBEDDING_MODEL
        
        # Check if model is supported
        if model_name not in self.config.SUPPORTED_MODELS["openai"]["embeddings"]:
            raise ValueError(f"Unsupported embedding model: {model_name}")
        
        # Check cache
        cache_key = f"embeddings_{model_name}"
        if cache_key in self._embedding_cache:
            return self._embedding_cache[cache_key]
        
        # Create new instance (only OpenAI for now)
        if not self.config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key required for embeddings")
        
        embeddings = OpenAIEmbeddings(
            model=model_name,
            api_key=self.config.OPENAI_API_KEY
        )
        
        # Wrap for RAGAS
        wrapped_embeddings = LangchainEmbeddingsWrapper(embeddings)
        self._embedding_cache[cache_key] = wrapped_embeddings
        
        return wrapped_embeddings
    
    def clear_cache(self):
        """Clear model caches"""
        self._llm_cache.clear()
        self._embedding_cache.clear()

# Global instance
model_manager = ModelManager()