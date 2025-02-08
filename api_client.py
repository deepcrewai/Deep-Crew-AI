import requests
from typing import Dict, List, Optional
import time

class OpenAlexClient:
    def __init__(self):
        self.base_url = "https://api.openalex.org"
        self.email = "anonymous@example.org"  # Best practice for OpenAlex

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make a request to OpenAlex API with rate limiting."""
        headers = {"User-Agent": f"mailto:{self.email}"}
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            params=params,
            headers=headers
        )
        time.sleep(0.1)  # Rate limiting
        return response.json()

    def search(self, query: str) -> List[Dict]:
        """Search OpenAlex for works matching the query."""
        params = {
            "search": query,
            "per_page": 10,  # Limit to 10 results
            "sort": "publication_date:desc",  # Sort by publication date, newest first
            "filter": "is_paratext:false"  # Exclude paratext items
        }

        try:
            response = self._make_request("works", params)
            return response.get("results", [])
        except Exception as e:
            print(f"Error in OpenAlex API request: {e}")
            return []

    def get_citations(self, work_id: str) -> List[Dict]:
        """Get citation information for a specific work."""
        params = {"cited_by": work_id, "per_page": 50}
        try:
            response = self._make_request("works", params)
            return response.get("results", [])
        except Exception as e:
            print(f"Error fetching citations: {e}")
            return []