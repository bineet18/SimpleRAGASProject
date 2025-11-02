from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ragas import evaluate
from ragas.metrics import Metric
from datasets import Dataset
import pandas as pd
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

class BaseMetric(ABC):
    """Base class for all metrics"""
    
    def __init__(self, llm, embeddings):
        self.llm = llm
        self.embeddings = embeddings
        # Wrap LLM and embeddings for RAGAS compatibility
        self.wrapped_llm = LangchainLLMWrapper(llm) if llm else None
        self.wrapped_embeddings = LangchainEmbeddingsWrapper(embeddings) if embeddings else None
        self.metric = self._get_metric()
        # Set LLM for the metric if it has llm attribute
        if hasattr(self.metric, 'llm') and self.wrapped_llm:
            self.metric.llm = self.wrapped_llm
        if hasattr(self.metric, 'embeddings') and self.wrapped_embeddings:
            self.metric.embeddings = self.wrapped_embeddings
    
    @abstractmethod
    def _get_metric(self) -> Metric:
        """Return the RAGAS metric instance"""
        pass
    
    @abstractmethod
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Prepare data for evaluation"""
        pass
    
    def calculate(self, data: Dict[str, Any]) -> float:
        """Calculate the metric score"""
        try:
            # Prepare data
            eval_data = self.prepare_data(data)
            
            # Create dataset
            dataset = Dataset.from_dict(eval_data)
            
            # Evaluate using wrapped LLM and embeddings
            result = evaluate(
                dataset=dataset,
                metrics=[self.metric],
                llm=self.wrapped_llm,
                embeddings=self.wrapped_embeddings
            )
            
            # Return score - extract from list if necessary
            score = result[self.metric.name]
            return float(score[0]) if isinstance(score, list) else float(score)
        except Exception as e:
            raise Exception(f"Error calculating {self.metric.name}: {str(e)}")