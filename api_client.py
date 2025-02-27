import requests
from typing import Dict, List, Optional
import time
from difflib import SequenceMatcher
import trafilatura

class OpenAlexClient:
    def __init__(self):
        self.base_url = "https://api.openalex.org"
        self.email = "researcher@example.org"  # Updated email for better rate limits
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
                "per_page": 100,  # Get more results initially for better relevance filtering
                "select": "title,abstract,doi,publication_year,concepts,cited_by_count"  # Specify fields
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
                # Extract and format paper data with improved abstract handling
                abstract = paper.get('abstract', '')

                # If no abstract available, try to fetch from DOI URL
                if (not abstract or abstract == "") and paper.get('doi'):
                    try:
                        doi_url = f"https://doi.org/{paper.get('doi')}"
                        downloaded = trafilatura.fetch_url(doi_url)
                        if downloaded:
                            extracted_text = trafilatura.extract(downloaded)
                            if extracted_text:
                                # Try to find an abstract section in the extracted text
                                lines = extracted_text.split('\n')
                                for i, line in enumerate(lines):
                                    if 'abstract' in line.lower():
                                        abstract = lines[i+1] if i+1 < len(lines) else ''
                                        break
                    except Exception as e:
                        print(f"Error fetching abstract from DOI: {str(e)}")

                # If still no abstract, provide a more informative message
                if not abstract or abstract == "":
                    try:
                        # Try to generate a summary from the title and concepts
                        title = paper.get('title', '')
                        concepts = [c.get('display_name', '') for c in paper.get('concepts', [])]
                        abstract = f"This paper titled '{title}' focuses on {', '.join(concepts[:3])}. Additional details can be found in the full paper."
                    except:
                        abstract = "This paper's abstract is not available in our database. You can access the full paper for detailed information."

                paper_data = {
                    'title': paper.get('title', 'Title not found'),
                    'abstract': abstract,
                    'doi': paper.get('doi'),
                    'publication_year': paper.get('publication_year'),
                    'url': f"https://doi.org/{paper.get('doi')}" if paper.get('doi') else None,
                    'concepts': paper.get('concepts', []),
                    'cited_by_count': paper.get('cited_by_count', 0)
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

            # Sort by citation count and similarity score
            enhanced_results.sort(key=lambda x: (-x['cited_by_count'], -x['similarity_score']))
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