from abc import ABC, abstractmethod
from typing import Dict, Any
from ragas import evaluate
from ragas.metrics import Metric
from datasets import Dataset
import pandas as pd

class BaseMetric(ABC):
    """Base class for all metrics"""
    
    def __init__(self, llm, embeddings):
        self.llm = llm
        self.embeddings = embeddings
        self.metric = self._get_metric()
    
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
            
            # Evaluate
            result = evaluate(
                dataset=dataset,
                metrics=[self.metric],
                llm=self.llm,
                embeddings=self.embeddings
            )
            
            # Return score
            return result[self.metric.name]
        except Exception as e:
            raise Exception(f"Error calculating {self.metric.name}: {str(e)}")
