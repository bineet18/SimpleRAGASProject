from ragas.metrics import AnswerRelevancy as RagasAnswerRelevancy
from .base_metric import BaseMetric
from typing import Dict, Any

class AnswerRelevancy(BaseMetric):
    """Answer Relevancy metric - measures relevance of answer to question"""
    
    def _get_metric(self):
        """Return RAGAS AnswerRelevancy metric"""
        metric = RagasAnswerRelevancy()
        # Set LLM and embeddings for the metric
        metric.llm = self.llm
        metric.embeddings = self.embeddings
        return metric
    
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Requires: question, answer"""
        return {
            "question": [data["question"]],
            "answer": [data["answer"]]
        }