import requests
from typing import Dict, List, Optional
import time
from difflib import SequenceMatcher
import trafilatura

class OpenAlexClient:
    def __init__(self):
        self.base_url = "https://api.openalex.org"
        self.email = "research@deepcrew.org"
        self.last_request_time = 0
        self.min_request_interval = 1.0

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
            print(f"Response content: {response.text[:500]}")  # Debug log (first 500 chars)

            if response.status_code == 200:
                data = response.json()
                print(f"Found {len(data.get('results', []))} results")  # Debug log
                return data
            else:
                print(f"Error response: {response.text}")  # Debug log
                return {"error": f"API error: {response.status_code}", "results": []}

        except Exception as e:
            print(f"Request error: {str(e)}")  # Debug log
            return {"error": str(e), "results": []}

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
                "select": "id,title,abstract,doi,publication_year,concepts,cited_by_count",
                "sort": "cited_by_count:desc",
                "filter": "type:journal-article"  # Only return journal articles
            }

            print(f"Searching OpenAlex with parameters:")  # Debug log
            print(f"Query: {cleaned_query}")
            print(f"Parameters: {params}")

            # First try with direct query
            response = self._make_request("works", params)

            if "error" in response:
                print(f"Search error: {response['error']}")
                return []

            results = response.get("results", [])
            print(f"Initial search returned {len(results)} results")  # Debug log

            # If no results and we have keywords, try with keywords
            if not results and keywords:
                print("No results with direct query, trying with keywords")  # Debug log
                keyword_query = " OR ".join(f'"{kw}"' for kw in keywords)  # Quote each keyword
                params["search"] = keyword_query
                print(f"Keyword search query: {keyword_query}")  # Debug log
                response = self._make_request("works", params)
                results = response.get("results", [])
                print(f"Keyword search returned {len(results)} results")  # Debug log

            # Process and enhance results
            enhanced_results = []
            for paper in results:
                try:
                    # Extract basic paper data
                    title = paper.get('title', '')
                    doi = paper.get('doi', '')
                    abstract = paper.get('abstract', '')

                    print(f"Processing paper: {title[:50]}...")  # Debug log

                    if not abstract and doi:
                        print(f"Fetching abstract for DOI: {doi}")  # Debug log
                        try:
                            doi_url = f"https://doi.org/{doi}"
                            downloaded = trafilatura.fetch_url(doi_url)
                            if downloaded:
                                extracted_text = trafilatura.extract(downloaded)
                                if extracted_text:
                                    abstract = extracted_text.split('\n')[0]
                                    print("Successfully fetched abstract from DOI")  # Debug log
                        except Exception as e:
                            print(f"Error fetching DOI abstract: {str(e)}")

                    # If still no abstract, use concepts
                    if not abstract:
                        concepts = [c.get('display_name', '') for c in paper.get('concepts', [])]
                        if concepts:
                            abstract = f"This research focuses on {', '.join(concepts[:3])}."
                            print("Generated abstract from concepts")  # Debug log

                    paper_data = {
                        'title': title or 'Untitled',
                        'abstract': abstract,
                        'doi': doi,
                        'publication_year': paper.get('publication_year'),
                        'url': f"https://doi.org/{doi}" if doi else None,
                        'concepts': paper.get('concepts', []),
                        'cited_by_count': paper.get('cited_by_count', 0)
                    }
                    enhanced_results.append(paper_data)

                except Exception as e:
                    print(f"Error processing paper: {str(e)}")
                    continue

            print(f"Successfully processed {len(enhanced_results)} papers")  # Debug log
            return enhanced_results[:50]  # Return top 50 results

        except Exception as e:
            print(f"Search error: {str(e)}")
            return []

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity between two strings."""
        if not text1 or not text2:
            return 0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()