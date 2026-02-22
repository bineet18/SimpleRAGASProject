from ragas.metrics import LLMContextPrecisionWithReference as RagasContextPrecision
from .base_metric import BaseMetric
from typing import Dict, Any, List


class ContextPrecision(BaseMetric):
    """Context Precision metric - measures how much retrieved context is relevant to the reference"""

    def _get_metric(self):
        """Return RAGAS LLMContextPrecisionWithReference metric"""
        metric = RagasContextPrecision()
        # BaseMetric will attach wrapped llm/embeddings if supported
        return metric

    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """
        Requires:
          - question (or user_input)
          - ground_truth (or reference)
          - contexts (or retrieved_contexts / retrieved_contexts)
        """
        user_input = data.get("question") or data.get("user_input")
        reference = data.get("ground_truth") or data.get("reference")

        contexts: List[str] = (
            data.get("contexts")
            or data.get("retrieved_contexts")
            or data.get("retrieved_contexts")
            or []
        )

        if user_input is None:
            raise ValueError("Missing required field: 'question' (or 'user_input')")
        if reference is None:
            raise ValueError("Missing required field: 'ground_truth' (or 'reference')")
        if not isinstance(contexts, list):
            raise ValueError("Field 'contexts' (or 'retrieved_contexts') must be a list of strings")

        return {
            "user_input": [user_input],
            "reference": [reference],
            "retrieved_contexts": [contexts],
        }