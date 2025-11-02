from ragas.metrics.critique import conciseness
from .base_metric import BaseMetric
from typing import Dict, Any

class Conciseness(BaseMetric):
    """Conciseness metric - checks if response is appropriately brief"""
    
    def _get_metric(self):
        return conciseness
    
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Requires: question, answer"""
        return {
            "question": [data["question"]],
            "answer": [data["answer"]]
        }
