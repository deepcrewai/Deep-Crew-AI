import requests
from typing import Dict, List
import os
from openai import OpenAI
import json

class PatentSearchClient:
    def __init__(self):
        self.base_url = "https://api.projectpq.ai"
        self.api_key = "1afab331b39299fbe63c045eae037b73"
        self.ai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    def search_patents(self, query: str) -> List[Dict]:
        """Search patents related to the query."""
        try:
            response = requests.get(
                f"{self.base_url}/search/102/",
                params={
                    "q": query,
                    "token": self.api_key,
                    "n": 10,
                    "type": "patent"
                },
                timeout=30
            )

            if response.status_code == 200:
                results = response.json().get("results", [])
                formatted_results = []
                for result in results:
                    formatted_results.append({
                        'patent_id': result.get('publication_number'),
                        'title': result.get('title'),
                        'abstract': result.get('abstract'),
                        'filing_date': result.get('filing_date'),
                        'inventors': ', '.join(result.get('inventors', [])),
                        'url': f"https://patents.google.com/patent/{result.get('publication_number')}"
                    })
                return formatted_results
            else:
                print(f"Error searching patents: {response.status_code}")
                return []

        except Exception as e:
            print(f"Error in patent search: {str(e)}")
            return []

    def analyze_patents(self, patents: List[Dict]) -> Dict:
        """Analyze patent results using AI."""
        try:
            # Prepare data for analysis
            patent_data = [
                f"Patent: {p['title']}\nAbstract: {p['abstract']}\nFiling Date: {p['filing_date']}"
                for p in patents
            ]

            # Generate analysis using OpenAI
            response = self.ai_client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """You are a patent analysis expert. Analyze these patents and provide:
                    1. A summary of the technology landscape
                    2. Key technology trends
                    3. Potential market opportunities
                    4. Competitive analysis
                    Return a JSON object with these sections."""
                }, {
                    "role": "user",
                    "content": "\n\n".join(patent_data)
                }],
                response_format={"type": "json_object"}
            )

            analysis = json.loads(response.choices[0].message.content)
            return analysis

        except Exception as e:
            print(f"Error in patent analysis: {str(e)}")
            return {
                "summary": "Error generating analysis",
                "trends": [],
                "opportunities": [],
                "competition": "Analysis unavailable"
            }

    def get_patent_details(self, patent_id: str) -> Dict:
        """Get detailed information about a specific patent."""
        try:
            response = requests.get(
                f"{self.base_url}/patents/{patent_id}",
                params={"token": self.api_key},
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting patent details: {response.status_code}")
                return {}

        except Exception as e:
            print(f"Error fetching patent details: {str(e)}")
            return {}