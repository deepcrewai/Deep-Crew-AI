import requests
from typing import Dict, List
import os
from openai import OpenAI
import json
import time

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

            print(f"Patent search response status: {response.status_code}")  # Debug log

            if response.status_code == 200:
                results = response.json().get("results", [])
                print(f"Found {len(results)} patent results")  # Debug log

                formatted_results = []
                for result in results:
                    # Extract inventors correctly - handle both string and list formats
                    inventors = result.get('inventors', [])
                    if isinstance(inventors, str):
                        inventors = [inv.strip() for inv in inventors.split(',')]
                    elif not isinstance(inventors, list):
                        inventors = []

                    # Get publication number without any prefix
                    pub_number = result.get('publication_number', '')
                    if pub_number:
                        # Remove any prefix/suffix and keep only the number
                        pub_number = ''.join(filter(str.isalnum, pub_number))

                    formatted_result = {
                        'patent_id': pub_number or result.get('patent_id', 'N/A'),
                        'title': result.get('title', 'Untitled Patent'),
                        'abstract': result.get('abstract', 'No abstract available'),
                        'filing_date': result.get('filing_date') or result.get('date', 'N/A'),
                        'inventors': ', '.join(inventors) if inventors else 'No inventors listed',
                        'url': f"https://patents.google.com/patent/{pub_number}" if pub_number else None
                    }
                    formatted_results.append(formatted_result)
                    print(f"Processed patent: {formatted_result['patent_id']}")  # Debug log

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