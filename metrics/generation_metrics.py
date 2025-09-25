from typing import Dict, Any, List, Optional
from ragas.metrics import (
    Faithfulness,
    ResponseRelevancy,
    AnswerCorrectness
)
from ragas.dataset_schema import SingleTurnSample

class GenerationMetrics:
    """Handler for generation-based metrics"""
    
    def __init__(self, llm, embeddings=None):
        self.llm = llm
        self.embeddings = embeddings
        
        # Initialize metrics
        self.metrics = {
            "faithfulness": Faithfulness(llm=llm),
            "answer_relevancy": ResponseRelevancy(llm=llm, embeddings=embeddings),
            "answer_correctness": AnswerCorrectness(llm=llm)
        }
    
    async def calculate(self, data: Dict[str, Any], metric_names: List[str]) -> Dict[str, float]:
        """Calculate requested generation metrics"""
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
        
        if "response" in data:
            sample_data["response"] = data["response"]
        
        # Metric-specific requirements
        if metric_name == "faithfulness":
            # Requires: user_input, response, retrieved_contexts
            if "retrieved_contexts" not in data:
                return None
            sample_data["retrieved_contexts"] = data["retrieved_contexts"]
            
        elif metric_name == "answer_relevancy":
            # Requires: user_input, response
            # Optional: retrieved_contexts
            if "retrieved_contexts" in data:
                sample_data["retrieved_contexts"] = data["retrieved_contexts"]
            
        elif metric_name == "answer_correctness":
            # Requires: user_input, response, reference
            if "reference" not in data:
                return None
            sample_data["reference"] = data["reference"]
            
            # Optional: retrieved_contexts
            if "retrieved_contexts" in data:
                sample_data["retrieved_contexts"] = data["retrieved_contexts"]
        
        # Validate minimum requirements
        if not sample_data.get("user_input") or not sample_data.get("response"):
            return None
        
        return sample_data
    
    @staticmethod
    def get_supported_metrics() -> List[str]:
        """Return list of supported generation metrics"""
        return [
            "faithfulness",
            "answer_relevancy",
            "answer_correctness"
        ]
    
    @staticmethod
    def get_metric_requirements() -> Dict[str, List[str]]:
        """Return required fields for each metric"""
        return {
            "faithfulness": ["user_input", "response", "retrieved_contexts"],
            "answer_relevancy": ["user_input", "response"],
            "answer_correctness": ["user_input", "response", "reference"]
        }