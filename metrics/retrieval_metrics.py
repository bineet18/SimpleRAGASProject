from typing import Dict, Any, List, Optional
from ragas.metrics import (
    LLMContextPrecisionWithoutReference,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
    ResponseRelevancy
)
from ragas.dataset_schema import SingleTurnSample

class RetrievalMetrics:
    """Handler for retrieval-based metrics"""
    
    def __init__(self, llm, embeddings=None):
        self.llm = llm
        self.embeddings = embeddings
        self.metrics = {
            "context_precision": LLMContextPrecisionWithoutReference(llm=llm),
            "context_precision_with_ref": LLMContextPrecisionWithReference(llm=llm),
            "context_recall": LLMContextRecall(llm=llm),
            "response_relevancy": ResponseRelevancy(llm=llm)
        }
    
    async def calculate(self, data: Dict[str, Any], metric_names: List[str]) -> Dict[str, float]:
        """Calculate requested retrieval metrics"""
        results = {}
        
        for metric_name in metric_names:
            if metric_name not in self.metrics:
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
                results[metric_name] = float(score)
                
            except Exception as e:
                print(f"Error calculating {metric_name}: {str(e)}")
                results[metric_name] = None
        
        return results
    
    def _prepare_sample(self, data: Dict[str, Any], metric_name: str) -> Optional[Dict[str, Any]]:
        """Prepare sample data based on metric requirements"""
        sample_data = {}
        
        # Common fields
        if "user_input" in data:
            sample_data["user_input"] = data["user_input"]
        
        if "retrieved_contexts" in data:
            sample_data["retrieved_contexts"] = data["retrieved_contexts"]
        
        # Metric-specific requirements
        if metric_name == "context_precision":
            # Requires: user_input, response, retrieved_contexts
            if "response" not in data:
                return None
            sample_data["response"] = data["response"]
            
        elif metric_name == "context_precision_with_ref":
            # Requires: user_input, reference, retrieved_contexts
            if "reference" not in data:
                return None
            sample_data["reference"] = data["reference"]
            
        elif metric_name == "context_recall":
            # Requires: user_input, reference, retrieved_contexts
            if "reference" not in data:
                return None
            sample_data["reference"] = data["reference"]
        
        # Validate minimum requirements
        if not sample_data.get("user_input") or not sample_data.get("retrieved_contexts"):
            return None
        
        return sample_data
    
    @staticmethod
    def get_supported_metrics() -> List[str]:
        """Return list of supported retrieval metrics"""
        return [
            "context_precision",
            "context_precision_with_ref",
            "context_recall"
        ]
    
    @staticmethod
    def get_metric_requirements() -> Dict[str, List[str]]:
        """Return required fields for each metric"""
        return {
            "context_precision": ["user_input", "response", "retrieved_contexts"],
            "context_precision_with_ref": ["user_input", "reference", "retrieved_contexts"],
            "context_recall": ["user_input", "reference", "retrieved_contexts"]
        }