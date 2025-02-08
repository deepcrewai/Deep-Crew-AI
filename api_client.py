import requests
from typing import Dict, List, Optional
import time
from difflib import SequenceMatcher

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
        if response.status_code != 200:
            print(f"API Error: {response.status_code}")
            return {"results": []}
        return response.json()

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity between two strings."""
        if not text1 or not text2:
            return 0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _calculate_keywords_similarity(self, paper: Dict, keywords: List[str]) -> float:
        """Calculate similarity between paper and search keywords."""
        # Combine paper title and abstract
        paper_text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
        # Calculate max similarity with any keyword
        similarities = [self._calculate_similarity(paper_text, keyword) for keyword in keywords]
        return max(similarities) if similarities else 0

    def search(self, query: str, keywords: List[str] = None) -> List[Dict]:
        """Search OpenAlex for works matching the query."""
        try:
            # First, try to get results with more specific search
            params = {
                "search": query,
                "per_page": 50,  # Increased for better filtering
                "filter": "is_paratext:false",
                "select": "id,title,abstract,doi,cited_by_count,publication_year"
            }

            response = self._make_request("works", params)
            results = response.get("results", [])

            if not results:
                # If no results, try with a more lenient search
                params["search"] = " OR ".join(keywords) if keywords else query
                response = self._make_request("works", params)
                results = response.get("results", [])

            # Enhance results with properly formatted data
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
                    'url': f"https://doi.org/{paper.get('doi')}" if paper.get('doi') else None
                }

                if keywords:
                    paper_data['similarity_score'] = self._calculate_keywords_similarity(paper_data, keywords)
                else:
                    paper_data['similarity_score'] = 1.0

                enhanced_results.append(paper_data)

            if keywords:
                # Sort by similarity score
                enhanced_results.sort(key=lambda x: x['similarity_score'], reverse=True)
                enhanced_results = enhanced_results[:10]  # Return top 10 most similar results

            return enhanced_results
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