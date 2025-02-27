import requests
from typing import Dict, List, Optional
import time

class OpenAlexClient:
    def __init__(self):
        self.base_url = "https://api.openalex.org"
        self.email = "research@deepcrew.org"
        self.last_request_time = 0
        self.min_request_interval = 1.0

    def search(self, query: str, keywords: List[str] = None) -> List[Dict]:
        """Search OpenAlex for works matching the query."""
        try:
            # Clean and prepare the query
            cleaned_query = query.strip()
            if not cleaned_query:
                return []

            # Base search parameters
            params = {
                "search": cleaned_query,
                "per_page": 100,
                "filter": "type:journal-article",
                "sort": "relevance_score:desc"
            }

            print(f"Searching OpenAlex with parameters:")  # Debug log
            print(f"Query: {cleaned_query}")
            print(f"Parameters: {params}")

            # First try with direct query
            response = self._make_request("works", params)
            results = response.get("results", [])
            print(f"Initial search returned {len(results)} results")  # Debug log

            # If no results, try with keywords
            if not results and keywords:
                print("No results with direct query, trying with keywords")  # Debug log
                keyword_query = f"{cleaned_query} OR " + " OR ".join(keywords)
                params["search"] = keyword_query
                print(f"Keyword search query: {keyword_query}")  # Debug log
                response = self._make_request("works", params)
                results = response.get("results", [])
                print(f"Keyword search returned {len(results)} results")  # Debug log

            # Process and enhance results
            enhanced_results = []
            for result in results:
                try:
                    # Basic paper data
                    paper_data = {
                        'title': result.get('title') or 'Untitled',
                        'publication_year': result.get('publication_year'),
                        'cited_by_count': result.get('cited_by_count', 0),
                        'doi': result.get('doi'),
                        'abstract': self._get_abstract(result),
                        'concepts': result.get('concepts', [])
                    }

                    if paper_data['doi']:
                        paper_data['url'] = f"https://doi.org/{paper_data['doi']}"

                    enhanced_results.append(paper_data)
                    print(f"Processed paper: {paper_data['title'][:50]}...")  # Debug log

                except Exception as e:
                    print(f"Error processing paper: {str(e)}")
                    continue

            print(f"Successfully processed {len(enhanced_results)} papers")  # Debug log

            # Sort by citation count and return top results
            enhanced_results.sort(key=lambda x: x.get('cited_by_count', 0), reverse=True)
            return enhanced_results[:50]

        except Exception as e:
            print(f"Search error: {str(e)}")
            return []

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make a request to OpenAlex API with improved error handling."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)

        headers = {
            "User-Agent": f"DeepCrew Research Platform (mailto:{self.email})",
            "Accept": "application/json"
        }

        try:
            url = f"{self.base_url}/{endpoint}"
            print(f"Making request to: {url}")  # Debug log
            print(f"With params: {params}")  # Debug log

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=30
            )
            self.last_request_time = time.time()

            print(f"Response status: {response.status_code}")  # Debug log
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Error response: {response.text}")  # Debug log
                return {"error": f"API error: {response.status_code}", "results": []}

        except Exception as e:
            print(f"Request error: {str(e)}")  # Debug log
            return {"error": str(e), "results": []}

    def _get_abstract(self, result: Dict) -> str:
        """Extract or generate abstract for a paper."""
        # Try to get abstract directly
        abstract = result.get('abstract', '')
        if abstract:
            return abstract

        # If no abstract but has concepts, generate a summary
        concepts = result.get('concepts', [])
        if concepts:
            concept_names = [c.get('display_name', '') for c in concepts if c.get('display_name')]
            if concept_names:
                return f"This research focuses on {', '.join(concept_names[:3])}. Full text available via DOI."

        # Default fallback
        return "Abstract will be available in the full paper."