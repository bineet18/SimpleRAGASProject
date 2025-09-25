from .retrieval_metrics import RetrievalMetrics
from .generation_metrics import GenerationMetrics
from .similarity_metrics import SimilarityMetrics
from .aspect_critic_metrics import AspectCriticMetrics

__all__ = [
    "RetrievalMetrics",
    "GenerationMetrics",
    "SimilarityMetrics",
    "AspectCriticMetrics"
]

# Metric registry for easy lookup
METRIC_REGISTRY = {
    # Retrieval metrics
    "context_precision": RetrievalMetrics,
    "context_precision_with_ref": RetrievalMetrics,
    "context_recall": RetrievalMetrics,
    
    # Generation metrics
    "faithfulness": GenerationMetrics,
    "answer_relevancy": GenerationMetrics,
    "answer_correctness": GenerationMetrics,
    
    # Similarity metrics
    "semantic_similarity": SimilarityMetrics,
    "bleu_score": SimilarityMetrics,
    "rouge_score": SimilarityMetrics,
    
    # Aspect critic metrics
    "coherence": AspectCriticMetrics,
    "conciseness": AspectCriticMetrics,
    "harmfulness": AspectCriticMetrics,
    "maliciousness": AspectCriticMetrics
}

def get_all_supported_metrics():
    """Get list of all supported metrics"""
    return list(METRIC_REGISTRY.keys())

def get_metric_handler(metric_name: str):
    """Get the appropriate handler class for a metric"""
    return METRIC_REGISTRY.get(metric_name)