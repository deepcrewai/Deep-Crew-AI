import os
from openai import OpenAI
from typing import Dict, List
import json

class AIAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        self.model = "gpt-4o"

    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze search results using AI."""
        analysis = {
            "summary": self._generate_summary(results),
            "trends": self._analyze_trends(results),
            "gaps": self._identify_gaps(results),
            "keywords": self._optimize_keywords(results),
            "complexity": self._assess_complexity(results)
        }
        return analysis

    def _generate_summary(self, results: List[Dict]) -> str:
        """Generate an AI summary of the research articles."""
        texts = [f"Title: {r.get('title', '')}\nAbstract: {r.get('abstract', '')}"
                for r in results[:5]]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "You are an academic research expert. Summarize these papers, "
                          "highlighting key findings and common themes."
            }, {
                "role": "user",
                "content": "\n\n".join(texts)
            }],
            max_tokens=500
        )
        return response.choices[0].message.content

    def _analyze_trends(self, results: List[Dict]) -> Dict:
        """Analyze research trends in the results."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "Analyze the research trends in these papers. "
                          "Return JSON with 'emerging_topics' and 'declining_topics'"
            }, {
                "role": "user",
                "content": str(results)
            }],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def _identify_gaps(self, results: List[Dict]) -> List[str]:
        """Identify research gaps in the literature."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "Identify potential research gaps in this literature. "
                          "Return a JSON array of gap descriptions."
            }, {
                "role": "user",
                "content": str(results)
            }],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def _optimize_keywords(self, results: List[Dict]) -> List[str]:
        """Suggest optimized keywords for better search results."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "Suggest improved keywords for searching this topic. "
                          "Return a JSON array of keyword suggestions."
            }, {
                "role": "user",
                "content": str(results)
            }],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def _assess_complexity(self, results: List[Dict]) -> Dict:
        """Assess the complexity of research papers."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "Assess the complexity of these papers. "
                          "Return JSON with 'complexity_score' (1-10) and 'explanation'"
            }, {
                "role": "user",
                "content": str(results)
            }],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
