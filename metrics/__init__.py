# Metrics package
from .answer_relevancy import AnswerRelevancy
from .answer_similarity import AnswerSimilarity
from .answer_correctness import AnswerCorrectness
from .aspect_critic import (
    AspectCriticMetric,
    HarmfulnessMetric,
    MaliciousnessMetric,
    CoherenceMetric,
    CorrectnessMetric,
    ConcisenessMetric,
    ASPECT_DEFINITIONS
)

# Metric registry with all available metrics
METRIC_REGISTRY = {
    "answer_relevancy": AnswerRelevancy,
    "answer_similarity": AnswerSimilarity,
    "answer_correctness": AnswerCorrectness,
    "harmfulness": HarmfulnessMetric,
    "maliciousness": MaliciousnessMetric,
    "coherence": CoherenceMetric,
    "correctness": CorrectnessMetric,
    "conciseness": ConcisenessMetric,
    # Generic aspect critic for custom aspects
    "aspect_critic": AspectCriticMetric
}

# Metrics that require ground_truth
METRICS_WITH_GROUND_TRUTH = ["answer_similarity", "answer_correctness"]

# AspectCritic metrics (binary output)
ASPECT_CRITIC_METRICS = ["harmfulness", "maliciousness", "coherence", "correctness", "conciseness"]