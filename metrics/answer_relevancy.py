from ragas.metrics import answer_relevancy
from .base_metric import BaseMetric
from typing import Dict, Any

class AnswerRelevancy(BaseMetric):
    """Answer Relevancy metric - measures relevance of answer to question"""
    
    def _get_metric(self):
        return answer_relevancy
    
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Requires: question, answer"""
        return {
            "question": [data["question"]],
            "answer": [data["answer"]]
        }
