import requests
from typing import Dict, List, Optional
import time
from difflib import SequenceMatcher

class OpenAlexClient:
    def __init__(self):
        self.base_url = "https://api.openalex.org"
        self.email = "anonymous@example.org"  # Best practice for OpenAlex
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make a request to OpenAlex API with improved rate limiting."""
        # Ensure minimum time between requests
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)

        headers = {
            "User-Agent": f"mailto:{self.email}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers=headers,
                timeout=10
            )
            self.last_request_time = time.time()

            if response.status_code == 429:  # Rate limit exceeded
                print("Rate limit exceeded, waiting...")
                time.sleep(5)  # Wait 5 seconds before retry
                return self._make_request(endpoint, params)  # Retry the request

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {str(e)}")
            return {"results": []}

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity between two strings."""
        if not text1 or not text2:
            return 0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def search(self, query: str, keywords: List[str] = None) -> List[Dict]:
        """Search OpenAlex for works matching the query with improved error handling."""
        try:
            # Base search parameters
            params = {
                "search": query,
                "per_page": 50,
                "filter": "is_paratext:false",
                "select": "id,title,abstract,doi,cited_by_count,publication_year,concepts"
            }

            # First attempt with exact query
            response = self._make_request("works", params)
            results = response.get("results", [])

            # If no results, try with keywords
            if not results and keywords:
                keyword_query = " OR ".join(f'"{kw}"' for kw in keywords)
                params["search"] = keyword_query
                response = self._make_request("works", params)
                results = response.get("results", [])

            # If still no results, try with a more lenient search
            if not results:
                params["search"] = query.replace('"', '')  # Remove quotes
                params["filter"] = None  # Remove filters
                response = self._make_request("works", params)
                results = response.get("results", [])

            # Process and enhance results
            enhanced_results = []
            for paper in results:
                # Extract and format paper data
                abstract = paper.get('abstract')
                if abstract is None or abstract == "":
                    abstract = "Abstract not available"

                paper_data = {
                    'title': paper.get('title', 'No title available'),
                    'abstract': abstract,
                    'doi': paper.get('doi'),
                    'cited_by_count': paper.get('cited_by_count', 0),
                    'publication_year': paper.get('publication_year'),
                    'url': f"https://doi.org/{paper.get('doi')}" if paper.get('doi') else None,
                    'concepts': paper.get('concepts', [])
                }

                # Calculate similarity score
                if keywords:
                    paper_text = f"{paper_data['title']} {paper_data['abstract']}"
                    similarities = [self._calculate_similarity(paper_text, kw) for kw in keywords]
                    paper_data['similarity_score'] = max(similarities) if similarities else 0.0
                else:
                    paper_data['similarity_score'] = 1.0

                enhanced_results.append(paper_data)

            # Sort results if we have keywords
            if keywords:
                enhanced_results.sort(key=lambda x: (-x['similarity_score'], -x['cited_by_count']))
                enhanced_results = enhanced_results[:10]  # Return top 10 most relevant results

            return enhanced_results

        except Exception as e:
            print(f"Error in search: {str(e)}")
            return []

    def get_citations(self, work_id: str) -> List[Dict]:
        """Get citation information for a specific work."""
        params = {"cited_by": work_id, "per_page": 50}
        try:
            response = self._make_request("works", params)
            return response.get("results", [])
        except Exception as e:
            print(f"Error fetching citations: {str(e)}")
            return []