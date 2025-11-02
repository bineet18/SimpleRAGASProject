from ragas.metrics import answer_correctness
from .base_metric import BaseMetric
from typing import Dict, Any

class AnswerCorrectness(BaseMetric):
    """Answer Correctness metric - evaluates factual accuracy"""
    
    def _get_metric(self):
        return answer_correctness
    
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Requires: question, answer, ground_truth"""
        return {
            "question": [data["question"]],
            "answer": [data["answer"]],
            "ground_truth": [data["ground_truth"]]
        }
