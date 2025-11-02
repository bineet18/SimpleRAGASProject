from ragas.metrics import AnswerCorrectness as RagasAnswerCorrectness
from .base_metric import BaseMetric
from typing import Dict, Any

class AnswerCorrectness(BaseMetric):
    """Answer Correctness metric - evaluates factual accuracy"""
    
    def _get_metric(self):
        """Return RAGAS AnswerCorrectness metric"""
        metric = RagasAnswerCorrectness()
        # Set LLM and embeddings for the metric
        metric.llm = self.llm
        metric.embeddings = self.embeddings
        return metric
    
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Requires: question, answer, ground_truth"""
        return {
            "question": [data["question"]],
            "answer": [data["answer"]],
            "ground_truth": [data["ground_truth"]]
        }