from ragas.metrics import LLMContextRecall as RagasContextRecall
from .base_metric import BaseMetric
from typing import Dict, Any, List


class ContextRecall(BaseMetric):
    """Context Recall metric - measures how much of the reference is covered by retrieved context"""

    def _get_metric(self):
        """Return RAGAS LLMContextRecall metric"""
        metric = RagasContextRecall()
        # BaseMetric will attach wrapped llm/embeddings if supported
        return metric

    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, list]:
        """
        Requires:
          - question (or user_input)
          - answer (or response)
          - ground_truth (or reference)
          - contexts (or retrieved_contexts / retrieved_contexts)
        """
        user_input = data.get("question") or data.get("user_input")
        response = data.get("answer") or data.get("response")
        reference = data.get("ground_truth") or data.get("reference")

        contexts: List[str] = (
            data.get("contexts")
            or data.get("retrieved_contexts")
            or data.get("retrieved_contexts")
            or []
        )

        if user_input is None:
            raise ValueError("Missing required field: 'question' (or 'user_input')")
        if response is None:
            raise ValueError("Missing required field: 'answer' (or 'response')")
        if reference is None:
            raise ValueError("Missing required field: 'ground_truth' (or 'reference')")
        if not isinstance(contexts, list):
            raise ValueError("Field 'contexts' (or 'retrieved_contexts') must be a list of strings")

        return {
            "user_input": [user_input],
            "response": [response],
            "reference": [reference],
            "retrieved_contexts": [contexts],
        }