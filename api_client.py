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

    def get_author_details(self, author_id: str) -> Dict:
        """Get detailed information about an author from OpenAlex."""
        try:
            endpoint = f"authors/{author_id}"
            response = self._make_request(endpoint, {})

            if not response:
                return {}

            # Extract relevant information
            return {
                'name': response.get('display_name'),
                'orcid': response.get('orcid'),
                'institution': response.get('last_known_institution', {}).get('display_name', 'Unknown'),
                'works_count': response.get('works_count', 0),
                'cited_by_count': response.get('cited_by_count', 0),
                'h_index': response.get('summary_stats', {}).get('h_index', 0),
                'concepts': [
                    {
                        'name': c.get('display_name'),
                        'level': c.get('level'),
                        'score': c.get('score')
                    }
                    for c in response.get('x_concepts', [])[:5]  # Top 5 research concepts
                ],
                'counts_by_year': response.get('counts_by_year', [])
            }
        except Exception as e:
            print(f"Error fetching author details: {str(e)}")
            return {}

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make a request to OpenAlex API with improved rate limiting and error handling."""
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

            # Try to handle the response even if it's not 200
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

    def search(self, query: str, keywords: List[str] = None) -> List[Dict]:
        """Search OpenAlex for works matching the query with improved error handling."""
        try:
            # Base search parameters with minimal filters
            params = {
                "search": query,
                "per_page": 100  # Get more results initially for better relevance filtering
            }

            # First attempt with exact query
            response = self._make_request("works", params)
            results = response.get("results", [])

            # If no results, try with keywords
            if not results and keywords:
                keyword_query = " OR ".join(keywords)
                params["search"] = keyword_query
                response = self._make_request("works", params)
                results = response.get("results", [])

            # If still no results, try with a more lenient search
            if not results:
                params["search"] = query.replace('"', '')  # Remove quotes
                response = self._make_request("works", params)
                results = response.get("results", [])

            # Process and enhance results
            enhanced_results = []
            for paper in results:
                # Extract and format paper data with proper abstract handling
                abstract = ""
                abstract_inverted_index = paper.get('abstract_inverted_index')
                if abstract_inverted_index:
                    # Reconstruct abstract from inverted index
                    words = []
                    for word, positions in abstract_inverted_index.items():
                        for pos in positions:
                            while len(words) <= pos:
                                words.append('')
                            words[pos] = word
                    abstract = ' '.join(words).strip()

                if not abstract:
                    abstract = "No abstract is available for this publication. You can access more information about this research by clicking the 'View Paper' link below."

                # Get authors from authorships
                authors = []
                for authorship in paper.get('authorships', []):
                    if authorship.get('author', {}).get('display_name'):
                        authors.append(authorship['author']['display_name'])

                paper_data = {
                    'title': paper.get('title', 'Title not found'),
                    'abstract': abstract,
                    'doi': paper.get('doi'),
                    'publication_year': paper.get('publication_year'),
                    'url': f"https://doi.org/{paper.get('doi')}" if paper.get('doi') else None,
                    'concepts': paper.get('concepts', []),
                    'authorships': paper.get('authorships', []),
                    'cited_by_count': paper.get('cited_by_count', 0),
                    'authors': authors
                }

                # Calculate similarity score with more weight on title matches
                if keywords:
                    # Calculate similarity for both title and abstract separately
                    title_similarities = [self._calculate_similarity(paper_data['title'], kw) for kw in keywords]
                    abstract_similarities = [self._calculate_similarity(paper_data['abstract'], kw) for kw in keywords]

                    # Give more weight to title matches (0.7) vs abstract matches (0.3)
                    max_title_sim = max(title_similarities) if title_similarities else 0.0
                    max_abstract_sim = max(abstract_similarities) if abstract_similarities else 0.0
                    paper_data['similarity_score'] = (0.7 * max_title_sim) + (0.3 * max_abstract_sim)
                else:
                    paper_data['similarity_score'] = 0.0

                enhanced_results.append(paper_data)

            # Sort by similarity score
            enhanced_results.sort(key=lambda x: (-x['similarity_score']))
            enhanced_results = enhanced_results[:50]  # Return top 50 most relevant results

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