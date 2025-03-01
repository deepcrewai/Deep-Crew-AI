import requests
from typing import Dict, List
import os
from openai import OpenAI
import json
import time

class PatentSearchClient:
    def __init__(self):
        self.base_url = "https://pqai-api.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": "1afab331b39299fbe63c045eae037b73",
            "X-RapidAPI-Host": "pqai-api.p.rapidapi.com"
        }
        self.ai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    def search_patents(self, query: str) -> List[Dict]:
        """Search patents related to the query."""
        try:
            response = requests.post(
                f"{self.base_url}/patent/search",
                headers=self.headers,
                json={
                    "question": query,
                    "limit": 10
                },
                timeout=30
            )

            print(f"Patent search response status: {response.status_code}")  # Debug log

            if response.status_code == 200:
                results = response.json().get("patents", [])
                print(f"Found {len(results)} patent results")  # Debug log
                print("Raw API response structure:", json.dumps(results[0] if results else {}, indent=2))

                formatted_results = []
                for result in results:
                    # Get publication number
                    publication_id = result.get('publication_number')

                    # Extract inventors
                    inventors = result.get('inventors', [])
                    if isinstance(inventors, str):
                        inventors = [inv.strip() for inv in inventors.split(',')]
                    elif not isinstance(inventors, list):
                        inventors = []

                    formatted_result = {
                        'patent_id': publication_id,
                        'title': result.get('title', 'Untitled Patent'),
                        'abstract': result.get('abstract', 'No abstract available'),
                        'filing_date': result.get('filing_date', 'N/A'),
                        'inventors': ', '.join(inventors) if inventors else 'No inventors listed',
                        'url': f"https://patents.google.com/patent/{publication_id}" if publication_id else None
                    }

                    print(f"Processed patent ID: {formatted_result['patent_id']}")  # Debug log
                    formatted_results.append(formatted_result)

                return formatted_results
            else:
                print(f"Error searching patents: {response.status_code}, {response.text}")
                return []

        except Exception as e:
            print(f"Error in patent search: {str(e)}")
            return []

    def analyze_patents(self, patents: List[Dict]) -> Dict:
        """Analyze patent results using AI."""
        try:
            # Prepare data for analysis
            patent_data = [
                f"Patent ID: {p['patent_id']}\nTitle: {p['title']}\nAbstract: {p['abstract']}\nFiling Date: {p['filing_date']}\nInventors: {p['inventors']}"
                for p in patents
            ]

            print("Sending patents to OpenAI for analysis...")  # Debug log

            # Generate analysis using OpenAI
            response = self.ai_client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """As a patent analysis expert, analyze these patents and provide a JSON response with the following structure:
                    {
                        "summary": "A detailed overview of the technology landscape...",
                        "trends": ["trend1", "trend2", "trend3"],
                        "opportunities": ["opportunity1", "opportunity2", "opportunity3"],
                        "competition": "A detailed competitive analysis..."
                    }"""
                }, {
                    "role": "user",
                    "content": "\n\n".join(patent_data)
                }],
                response_format={"type": "json_object"}
            )

            analysis = json.loads(response.choices[0].message.content)
            print("Successfully received AI analysis")  # Debug log
            return analysis

        except Exception as e:
            print(f"Error in patent analysis: {str(e)}")
            return {
                "summary": f"Error generating analysis: {str(e)}",
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