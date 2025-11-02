# Metrics package
from .answer_relevancy import AnswerRelevancy
from .answer_similarity import AnswerSimilarity
from .answer_correctness import AnswerCorrectness
from .harmfulness import Harmfulness
from .coherence import Coherence
from .conciseness import Conciseness

# Metric registry
METRIC_REGISTRY = {
    "answer_relevancy": AnswerRelevancy,
    "answer_similarity": AnswerSimilarity,
    "answer_correctness": AnswerCorrectness,
    "harmfulness": Harmfulness,
    "coherence": Coherence,
    "conciseness": Conciseness
}

# Metrics that require ground_truth
METRICS_WITH_GROUND_TRUTH = ["answer_similarity", "answer_correctness"]