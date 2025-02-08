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

    def search(self, query: str, search_type: str, year_range: tuple) -> List[Dict]:
        """Search OpenAlex based on query type and filters."""
        params = {
            "filter": f"publication_year:{year_range[0]}-{year_range[1]}",
            "per_page": 50
        }
        
        if search_type == "Keywords":
            endpoint = "works"
            params["search"] = query
        elif search_type == "Author":
            endpoint = "authors"
            params["search"] = query
        elif search_type == "Institution":
            endpoint = "institutions"
            params["search"] = query
        else:  # Field
            endpoint = "concepts"
            params["search"] = query

        try:
            response = self._make_request(endpoint, params)
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
