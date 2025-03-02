import os
from openai import OpenAI
from typing import Dict, List
import json

class AIAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4"

    def analyze_combined_results(self, research_results: List[Dict], patent_results: List[Dict], funding_data: Dict = None, network_data: List[Dict] = None) -> Dict:
        """Analyze combined research and patent results for comprehensive insights with enhanced detail."""
        try:
            # Prepare enhanced combined data for analysis
            combined_data = {
                'research_papers': [
                    {
                        'title': r.get('title', ''),
                        'abstract': r.get('abstract', ''),
                        'year': r.get('publication_year', ''),
                        'type': 'research',
                        'concepts': r.get('concepts', []),
                        'citations': r.get('cited_by_count', 0),
                        'authors': r.get('authors', [])
                    } for r in research_results
                ] if research_results else [],
                'patents': [
                    {
                        'title': p.get('title', ''),
                        'abstract': p.get('abstract', ''),
                        'filing_date': p.get('filing_date', ''),
                        'type': 'patent',
                        'inventors': p.get('inventors', ''),
                        'patent_id': p.get('patent_id', '')
                    } for p in patent_results
                ] if patent_results else [],
                'funding_data': funding_data if funding_data else {},
                'network_data': network_data if network_data else []
            }

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """As an expert research analyst, provide a comprehensive analysis of the research ecosystem including papers, patents, funding opportunities, and collaboration networks.
                    Include detailed insights, recommendations, and future predictions. Return a JSON object with the following structure:
                    {
                        "comprehensive_summary": "Detailed overview analyzing all available components, including key themes and overall direction of the field",
                        "key_findings": [
                            {"finding": "description", "impact_score": 1-10, "evidence": "supporting evidence", "component": "research/patent/funding/network"}
                        ],
                        "research_patent_alignment": {
                            "overview": "Detailed analysis of how research aligns with patent activity",
                            "gaps": ["specific gaps between research and patents"],
                            "opportunities": ["specific opportunities based on gaps"]
                        },
                        "funding_landscape": {
                            "available_opportunities": ["detailed funding descriptions"],
                            "alignment_with_research": "how funding aligns with current research",
                            "recommendations": ["specific funding pursuit strategies"]
                        },
                        "collaboration_insights": {
                            "key_researchers": ["prominent researchers in the field"],
                            "institutional_networks": ["major research institutions"],
                            "partnership_opportunities": ["potential collaboration suggestions"]
                        },
                        "innovation_trajectory": {
                            "current_state": "description of present innovation landscape",
                            "short_term_predictions": ["6-12 month predictions"],
                            "long_term_outlook": ["2-5 year predictions"]
                        },
                        "market_potential": {
                            "immediate_applications": ["ready-to-market innovations"],
                            "development_needs": ["required improvements"],
                            "market_size_estimates": ["potential market valuations"]
                        },
                        "research_gaps": [
                            {"area": "description", "priority": 1-10, "resources_needed": "description"}
                        ],
                        "technology_assessment": {
                            "maturity_levels": {"research": 1-10, "patents": 1-10},
                            "development_stages": ["stage descriptions"],
                            "commercialization_readiness": "assessment"
                        },
                        "risk_analysis": {
                            "technical_risks": ["risk descriptions"],
                            "market_risks": ["risk descriptions"],
                            "funding_risks": ["risk descriptions"],
                            "mitigation_strategies": ["strategy descriptions"]
                        },
                        "investment_recommendations": [
                            {"area": "description", "potential_roi": "high/medium/low", "timeframe": "description", "required_investment": "estimation"}
                        ],
                        "regulatory_compliance": {
                            "current_requirements": ["regulatory considerations"],
                            "future_changes": ["anticipated regulatory changes"],
                            "compliance_strategies": ["recommended approaches"]
                        },
                        "sustainability_impact": {
                            "environmental_considerations": ["impact descriptions"],
                            "social_implications": ["impact on society"],
                            "economic_effects": ["economic implications"]
                        }
                    }"""
                }, {
                    "role": "user",
                    "content": json.dumps(combined_data)
                }],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error in combined analysis: {str(e)}")
            return {
                "comprehensive_summary": "Error performing combined analysis",
                "key_findings": [],
                "research_patent_alignment": {"overview": "Analysis unavailable", "gaps": [], "opportunities": []},
                "funding_landscape": {"available_opportunities": [], "alignment_with_research": "", "recommendations": []},
                "collaboration_insights": {"key_researchers": [], "institutional_networks": [], "partnership_opportunities": []},
                "innovation_trajectory": {"current_state": "", "short_term_predictions": [], "long_term_outlook": []},
                "market_potential": {"immediate_applications": [], "development_needs": [], "market_size_estimates": []},
                "research_gaps": [],
                "technology_assessment": {"maturity_levels": {}, "development_stages": [], "commercialization_readiness": ""},
                "risk_analysis": {"technical_risks": [], "market_risks": [], "funding_risks": [], "mitigation_strategies": []},
                "investment_recommendations": [],
                "regulatory_compliance": {"current_requirements": [], "future_changes": [], "compliance_strategies": []},
                "sustainability_impact": {"environmental_considerations": [], "social_implications": [], "economic_effects": []}
            }

    def generate_search_keywords(self, query: str) -> List[str]:
        """Generate optimal search keywords from the user's query."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """You are a research expert. Extract exactly 4 focused keywords that capture 
                    different aspects of the query. Return a JSON object with 'keywords' array. The keywords should 
                    cover both broad and specific aspects of the research topic.
                    
                    Examples:
                    Query: "A mobile phone that detects users' facial expressions and adjusts text size"
                    Keywords: ["Adaptive display", "Facial recognition", "Mobile accessibility", "Human-computer interaction"]
                    
                    Query: "A coffee maker that detects empty carafe and turns off heating"
                    Keywords: ["Smart appliances", "Coffee maker automation", "Safety mechanisms", "Automatic shutoff"]
                    
                    Query: "A vehicle tire with built-in pump using centrifugal forces"
                    Keywords: ["Self-inflating tire", "Centrifugal pump", "Automotive innovation", "Tire pressure system"]
                    
                    The response should be in format: {"keywords": ["term1", "term2", "term3", "term4"]}"""
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
                              "Return a JSON object with an array of gap descriptions in the format: "
                              "{'gaps': ['gap1', 'gap2', ...]}."
                }, {
                    "role": "user",
                    "content": json.dumps(data)
                }],
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return result.get('gaps', [])
        except Exception as e:
            print(f"Error identifying gaps: {str(e)}")
            return [f"Error identifying gaps: {str(e)}"]

    def _optimize_keywords(self, data: Dict) -> List[str]:
        """Suggest optimized keywords for better search results."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": "Based on the titles and concepts, suggest improved keywords "
                              "for searching this topic. Return a JSON object with an array "
                              "of keywords in the format: {'keywords': ['keyword1', 'keyword2', ...]}."
                }, {
                    "role": "user",
                    "content": json.dumps(data)
                }],
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return result.get('keywords', [])
        except Exception as e:
            print(f"Error optimizing keywords: {str(e)}")
            return []

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