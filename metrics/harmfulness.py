from ragas.metrics.critique import harmfulness
from .base_metric import BaseMetric
from typing import Dict, Any

class Harmfulness(BaseMetric):
    """Harmfulness metric - checks for harmful content"""
    
    def _get_metric(self):
        return harmfulness
    
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Requires: question, answer"""
        return {
            "question": [data["question"]],
            "answer": [data["answer"]]
        }
