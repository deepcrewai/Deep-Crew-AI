import requests
from typing import Dict, List, Optional
import time
from difflib import SequenceMatcher

class OpenAlexClient:
    def __init__(self):
        self.base_url = "https://api.openalex.org"
        self.email = "researcher@example.org"
        self.last_request_time = 0
        self.min_request_interval = 1.0

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make a request to OpenAlex API with improved rate limiting and error handling."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)

        headers = {
            "User-Agent": f"mailto:{self.email}",
            "Accept": "application/json"
        }

        try:
            url = f"{self.base_url}/{endpoint}"
            print(f"Making request to: {url} with params: {params}")

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=30
            )
            self.last_request_time = time.time()

            print(f"Response status: {response.status_code}")

            if response.status_code == 429:
                print("Rate limit exceeded, waiting...")
                time.sleep(5)
                return self._make_request(endpoint, params)

            try:
                return response.json()
            except Exception as e:
                print(f"Error parsing response: {str(e)}")
                return {"results": []}

        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {str(e)}")
            return {"results": []}

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity between two strings."""
        if not text1 or not text2:
            return 0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def search(self, query: str, keywords: List[str] = []) -> List[Dict]:
        """Search OpenAlex for works matching the query with improved error handling."""
        try:
            if not query.strip():
                return []

            params = {
                "search": query,
                "per_page": 100
            }

            response = self._make_request("works", params)
            if not isinstance(response, dict):
                print(f"Invalid API response format: {response}")
                return []

            results = response.get("results", [])

            if not results and keywords:
                keyword_query = " OR ".join(keywords)
                params["search"] = keyword_query
                response = self._make_request("works", params)
                if not isinstance(response, dict):
                    print(f"Invalid API response format: {response}")
                    return []
                results = response.get("results", [])

            if not results:
                params["search"] = query.replace('"', '')
                response = self._make_request("works", params)
                results = response.get("results", [])

            enhanced_results = []
            for paper in results:
                abstract = paper.get('abstract')
                if abstract is None or abstract == "":
                    abstract = "Abstract is not available for this paper. Please refer to the full paper for detailed information."

                paper_data = {
                    'title': paper.get('title', 'Title not found'),
                    'abstract': abstract,
                    'doi': paper.get('doi'),
                    'publication_year': paper.get('publication_year'),
                    'url': f"https://doi.org/{paper.get('doi')}" if paper.get('doi') else None,
                    'concepts': paper.get('concepts', [])
                }

                if keywords:
                    title_similarities = [self._calculate_similarity(paper_data['title'], kw) for kw in keywords]
                    abstract_similarities = [self._calculate_similarity(paper_data['abstract'], kw) for kw in keywords]
                    max_title_sim = max(title_similarities) if title_similarities else 0.0
                    max_abstract_sim = max(abstract_similarities) if abstract_similarities else 0.0
                    paper_data['similarity_score'] = (0.7 * max_title_sim) + (0.3 * max_abstract_sim)
                else:
                    paper_data['similarity_score'] = 0.0

                enhanced_results.append(paper_data)

            enhanced_results.sort(key=lambda x: (-x['similarity_score']))
            enhanced_results = enhanced_results[:10]

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