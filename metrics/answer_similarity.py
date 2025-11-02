from ragas.metrics import answer_similarity
from .base_metric import BaseMetric
from typing import Dict, Any

class AnswerSimilarity(BaseMetric):
    """Answer Similarity metric - measures similarity between answer and ground truth"""
    
    def _get_metric(self):
        return answer_similarity
    
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Requires: question, answer, ground_truth"""
        return {
            "question": [data["question"]],
            "answer": [data["answer"]],
            "ground_truth": [data["ground_truth"]]
        }
