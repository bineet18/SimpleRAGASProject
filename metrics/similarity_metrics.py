from typing import Dict, Any, List, Optional
from ragas.metrics import (
    SemanticSimilarity,
    BleuScore,
    RougeScore
)
from ragas.dataset_schema import SingleTurnSample

class SimilarityMetrics:
    """Handler for similarity-based metrics"""
    
    def __init__(self, llm=None, embeddings=None):
        self.llm = llm
        self.embeddings = embeddings
        
        # Initialize metrics
        self.metrics = {}
        
        # Semantic similarity needs embeddings
        if embeddings:
            self.metrics["semantic_similarity"] = SemanticSimilarity(embeddings=embeddings)
        
        # BLEU and ROUGE don't need LLM or embeddings
        self.metrics["bleu_score"] = BleuScore()
        self.metrics["rouge_score"] = RougeScore()
    
    async def calculate(self, data: Dict[str, Any], metric_names: List[str]) -> Dict[str, float]:
        """Calculate requested similarity metrics"""
        results = {}
        
        for metric_name in metric_names:
            if metric_name not in self.metrics:
                if metric_name == "semantic_similarity" and not self.embeddings:
                    results[metric_name] = None
                    print(f"Skipping {metric_name}: embeddings not available")
                continue
            
            try:
                # Prepare sample based on metric requirements
                sample_data = self._prepare_sample(data, metric_name)
                if sample_data is None:
                    results[metric_name] = None
                    continue
                
                sample = SingleTurnSample(**sample_data)
                metric = self.metrics[metric_name]
                
                # Calculate metric
                score = await metric.single_turn_ascore(sample)
                
                # Handle different score types
                if isinstance(score, dict):
                    # For ROUGE score which returns multiple values
                    results[metric_name] = score
                else:
                    results[metric_name] = float(score)
                
            except Exception as e:
                print(f"Error calculating {metric_name}: {str(e)}")
                results[metric_name] = None
        
        return results
    
    def _prepare_sample(self, data: Dict[str, Any], metric_name: str) -> Optional[Dict[str, Any]]:
        """Prepare sample data based on metric requirements"""
        sample_data = {}
        
        # All similarity metrics need response and reference
        if "response" not in data or "reference" not in data:
            return None
        
        sample_data["response"] = data["response"]
        sample_data["reference"] = data["reference"]
        
        # Add optional fields if available
        if "user_input" in data:
            sample_data["user_input"] = data["user_input"]
        
        return sample_data
    
    @staticmethod
    def get_supported_metrics() -> List[str]:
        """Return list of supported similarity metrics"""
        return [
            "semantic_similarity",
            "bleu_score",
            "rouge_score"
        ]
    
    @staticmethod
    def get_metric_requirements() -> Dict[str, List[str]]:
        """Return required fields for each metric"""
        return {
            "semantic_similarity": ["response", "reference"],
            "bleu_score": ["response", "reference"],
            "rouge_score": ["response", "reference"]
        }