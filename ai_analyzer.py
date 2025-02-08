import os
from openai import OpenAI
from typing import Dict, List
import json

class AIAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    def generate_search_keywords(self, query: str) -> List[str]:
        """Generate optimal search keywords from the user's query."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """You are a research expert. Extract 1-2 concise, focused keywords that capture 
                    the core concept of the query. Return a JSON object with 'keywords' array. Focus on the 
                    main innovation or concept, not the technical details.

                    Examples:
                    Query: "A mobile phone that detects users' facial expressions and adjusts text size"
                    Keywords: ["Adaptive display"]

                    Query: "A coffee maker that detects empty carafe and turns off heating"
                    Keywords: ["Coffee maker"]

                    Query: "A vehicle tire with built-in pump using centrifugal forces"
                    Keywords: ["Self-inflating tire"]

                    The response should be in format: {"keywords": ["term1", "term2"]}"""
                }, {
                    "role": "user",
                    "content": query
                }],
                response_format={"type": "json_object"}
            )
            keywords = json.loads(response.choices[0].message.content)
            return keywords.get("keywords", [query])  # Fallback to original query if extraction fails
        except Exception as e:
            print(f"Error generating keywords: {e}")
            return [query]  # Fallback to original query

    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze search results using AI."""
        analysis = {
            "summary": self._generate_summary(results[:5]),  # Limit to 5 papers for summary
            "trends": self._analyze_trends(results),
            "gaps": self._identify_gaps(self._prepare_data_for_analysis(results)),
            "keywords": self._optimize_keywords(self._prepare_data_for_analysis(results)),
            "complexity": self._assess_complexity(results[:10])  # Limit to 10 papers
        }
        return analysis

    def _prepare_data_for_analysis(self, results: List[Dict]) -> Dict:
        """Prepare a condensed version of results for analysis."""
        return {
            'titles': [r.get('title', '') for r in results],
            'years': [r.get('publication_year', '') for r in results],
            'concepts': [
                [c.get('display_name', '') for c in r.get('concepts', [])]
                for r in results
            ]
        }

    def _generate_summary(self, results: List[Dict]) -> str:
        """Generate an AI summary of the research articles."""
        try:
            texts = [f"Title: {r.get('title', '')}\nAbstract: {r.get('abstract', '')}"
                    for r in results]

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
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def _analyze_trends(self, results: List[Dict]) -> Dict:
        """Analyze research trends in the results."""
        try:
            # Prepare simplified trend data
            trend_data = {
                'publication_years': [r.get('publication_year', '') for r in results],
                'concepts': [
                    [c.get('display_name', '') for c in r.get('concepts', [])]
                    for r in results
                ]
            }

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": "Analyze publication years and concepts to identify research trends. "
                              "Return JSON with 'emerging_topics' and 'declining_topics'"
                }, {
                    "role": "user",
                    "content": json.dumps(trend_data)
                }],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"emerging_topics": [], "declining_topics": [], "error": str(e)}

    def _identify_gaps(self, data: Dict) -> List[str]:
        """Identify research gaps in the literature."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": "Identify potential research gaps based on the titles and concepts. "
                              "Return a JSON array of gap descriptions."
                }, {
                    "role": "user",
                    "content": json.dumps(data)
                }],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return [f"Error identifying gaps: {str(e)}"]

    def _optimize_keywords(self, data: Dict) -> List[str]:
        """Suggest optimized keywords for better search results."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": "Based on the titles and concepts, suggest improved keywords "
                              "for searching this topic. Return a JSON array of keywords."
                }, {
                    "role": "user",
                    "content": json.dumps(data)
                }],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return [f"Error optimizing keywords: {str(e)}"]

    def _assess_complexity(self, results: List[Dict]) -> Dict:
        """Assess the complexity of research papers."""
        try:
            # Prepare simplified data for complexity analysis
            complexity_data = [{
                'title': r.get('title', ''),
                'abstract': r.get('abstract', '')[:500]  # Limit abstract length
            } for r in results]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": "Assess the complexity of these papers. "
                              "Return JSON with 'complexity_score' (1-10) and 'explanation'"
                }, {
                    "role": "user",
                    "content": json.dumps(complexity_data)
                }],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"complexity_score": 0, "explanation": f"Error assessing complexity: {str(e)}"}