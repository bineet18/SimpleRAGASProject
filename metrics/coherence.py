from ragas.metrics.critique import coherence
from .base_metric import BaseMetric
from typing import Dict, Any

class Coherence(BaseMetric):
    """Coherence metric - evaluates logical flow"""
    
    def _get_metric(self):
        return coherence
    
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Requires: question, answer"""
        return {
            "question": [data["question"]],
            "answer": [data["answer"]]
        }
