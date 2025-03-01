import requests
from typing import Dict, List
import os
from openai import OpenAI
import json
import time

class PatentSearchClient:
    def __init__(self):
        self.base_url = "https://api.projectpq.ai"
        self.token = os.environ.get("RAPIDAPI_KEY")  # Using the existing environment variable
        self.ai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    def search_patents(self, query: str) -> List[Dict]:
        """Search patents related to the query."""
        try:
            # Configure the API endpoint
            route = "/search/102"
            url = f"{self.base_url}{route}"

            # Configure search parameters
            params = {
                "q": query,
                "n": 10,
                "type": "patent",
                "after": "2016-01-01",
                "token": self.token
            }

            # Make the request
            response = requests.get(url, params=params, timeout=30)
            print(f"Patent search response status: {response.status_code}")
            print(f"Response content: {response.text[:500]}")  # Print first 500 chars of response

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                print(f"Found {len(results)} patent results")

                if results:
                    print("First result structure:", json.dumps(results[0], indent=2))

                formatted_results = []
                for result in results:
                    # Extract and clean publication number
                    publication_id = result.get('id', '')
                    if publication_id:
                        publication_id = ''.join(filter(str.isalnum, publication_id))

                    # Handle inventors - ensure it's a string
                    inventors = result.get('inventors', [])
                    if isinstance(inventors, list):
                        inventors = ', '.join(str(inv) for inv in inventors)
                    elif not isinstance(inventors, str):
                        inventors = 'No inventors listed'

                    formatted_result = {
                        'patent_id': result.get('id', 'N/A'),  # Using 'id' field for patent_id
                        'title': result.get('title', 'Untitled Patent'),
                        'abstract': result.get('abstract', 'No abstract available'),
                        'filing_date': result.get('publication_date', 'N/A'),  # Using 'publication_date' for filing_date
                        'inventors': inventors,
                        'url': result.get('www_link')  # Using 'www_link' for the patent URL
                    }

                    print(f"Processed patent ID: {formatted_result['patent_id']}")
                    formatted_results.append(formatted_result)

                return formatted_results
            else:
                error_msg = f"Error searching patents: {response.status_code}, {response.text}"
                print(error_msg)
                raise Exception(error_msg)

        except Exception as e:
            print(f"Error in patent search: {str(e)}")
            return []

    def analyze_patents(self, patents: List[Dict]) -> Dict:
        """Analyze patent results using AI."""
        try:
            patent_data = [
                f"Patent ID: {p['patent_id']}\nTitle: {p['title']}\nAbstract: {p['abstract']}\nFiling Date: {p['filing_date']}\nInventors: {p['inventors']}"
                for p in patents
            ]

            print("Sending patents to OpenAI for analysis...")

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
            print("Successfully received AI analysis")
            return analysis

        except Exception as e:
            print(f"Error in patent analysis: {str(e)}")
            return {
                "summary": f"Error generating analysis: {str(e)}",
                "trends": [],
                "opportunities": [],
                "competition": "Analysis unavailable"
            }