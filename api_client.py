import requests
from typing import Dict, List, Optional
import time
from difflib import SequenceMatcher
import trafilatura

class OpenAlexClient:
    def __init__(self):
        self.base_url = "https://api.openalex.org"
        self.email = "research@deepcrew.org"  # Updated email for polite pool
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make a request to OpenAlex API with improved rate limiting and error handling."""
        # Ensure minimum time between requests
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
            print(f"Making request to: {url} with params: {params}")  # Debug log

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=30
            )
            self.last_request_time = time.time()

            print(f"Response status: {response.status_code}")  # Debug log

            if response.status_code == 429:  # Rate limit exceeded
                print("Rate limit exceeded, waiting...")
                time.sleep(5)  # Wait 5 seconds before retry
                return self._make_request(endpoint, params)  # Retry the request

            if response.status_code == 403:
                print("Authentication error. Checking headers:", headers)
                return {"error": "Authentication failed", "results": []}

            response.raise_for_status()  # Raise exception for other error codes

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {str(e)}")
            return {"error": str(e), "results": []}

    def search(self, query: str, keywords: List[str] = None) -> List[Dict]:
        """Search OpenAlex for works matching the query with improved error handling."""
        try:
            # Base search parameters
            params = {
                "filter": "has_abstract:true",  # Only return results with abstracts
                "search": query,
                "per_page": 100,
                "select": "id,title,abstract,doi,publication_year,concepts,cited_by_count"
            }

            print(f"Searching OpenAlex with query: {query}")  # Debug log
            response = self._make_request("works", params)

            if "error" in response:
                print(f"Search error: {response['error']}")
                return []

            results = response.get("results", [])
            print(f"Found {len(results)} initial results")  # Debug log

            # If no results, try with keywords
            if not results and keywords:
                keyword_query = " OR ".join(keywords)
                params["search"] = keyword_query
                response = self._make_request("works", params)
                results = response.get("results", [])
                print(f"Found {len(results)} results with keywords")  # Debug log

            enhanced_results = []
            for paper in results:
                # Extract and format paper data
                abstract = paper.get('abstract', '')
                doi = paper.get('doi')

                # If no abstract but has DOI, try to fetch from DOI
                if (not abstract or abstract == "") and doi:
                    try:
                        doi_url = f"https://doi.org/{doi}"
                        downloaded = trafilatura.fetch_url(doi_url)
                        if downloaded:
                            extracted_text = trafilatura.extract(downloaded)
                            if extracted_text:
                                abstract = extracted_text.split('\n')[0]  # Use first paragraph
                    except Exception as e:
                        print(f"Error fetching abstract from DOI: {str(e)}")

                # If still no abstract, use concepts
                if not abstract or abstract == "":
                    concepts = [c.get('display_name', '') for c in paper.get('concepts', [])]
                    if concepts:
                        abstract = f"This research focuses on {', '.join(concepts[:3])}. Full text available via DOI."
                    else:
                        abstract = "Abstract text will be available in the full paper."

                paper_data = {
                    'title': paper.get('title', 'Untitled'),
                    'abstract': abstract,
                    'doi': doi,
                    'publication_year': paper.get('publication_year'),
                    'url': f"https://doi.org/{doi}" if doi else None,
                    'concepts': paper.get('concepts', []),
                    'cited_by_count': paper.get('cited_by_count', 0)
                }

                # Calculate relevance score
                title_similarity = max([self._calculate_similarity(paper_data['title'], kw) for kw in ([query] + (keywords or []))])
                abstract_similarity = max([self._calculate_similarity(abstract, kw) for kw in ([query] + (keywords or []))])
                paper_data['relevance_score'] = (0.7 * title_similarity) + (0.3 * abstract_similarity)

                enhanced_results.append(paper_data)

            # Sort by relevance and citations
            enhanced_results.sort(key=lambda x: (x['relevance_score'], x['cited_by_count']), reverse=True)
            return enhanced_results[:50]  # Return top 50 results

        except Exception as e:
            print(f"Error in search: {str(e)}")
            return []

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity between two strings."""
        if not text1 or not text2:
            return 0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def get_citations(self, work_id: str) -> List[Dict]:
        """Get citation information for a specific work."""
        params = {"cited_by": work_id, "per_page": 50}
        try:
            response = self._make_request("works", params)
            return response.get("results", [])
        except Exception as e:
            print(f"Error fetching citations: {str(e)}")
            return []