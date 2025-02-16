import requests
from typing import Dict, List

class PatentSearchClient:
    def __init__(self):
        self.base_url = "https://api.projectpq.ai"
        self.api_key = "1afab331b39299fbe63c045eae037b73"

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