import os
import requests
from typing import List, Dict

class ElsevierClient:
    def __init__(self):
        self.api_key = os.environ.get("ELSEVIER_API_KEY")
        if not self.api_key:
            raise ValueError("ELSEVIER_API_KEY environment variable is not set")
        self.base_url = "https://api.elsevier.com/content/search/sciencedirect"
        self.headers = {
            "X-ELS-APIKey": self.api_key,
            "Accept": "application/json"
        }

    def search(self, query: str, limit: int = 25) -> List[Dict]:
        """Search for papers in ScienceDirect."""
        try:
            if not query:
                return []

            params = {
                "query": query,
                "count": limit,
                "start": 0,
                "sort": "-date",  # Sort by date descending
                "field": "all",  # Search in all fields
                "suppressNavLinks": "true"
            }

            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params
            )

            if response.status_code == 401:
                print("Authentication failed: Please check your API key")
                return []

            response.raise_for_status()
            data = response.json()

            # Extract relevant information from response
            results = []
            entries = data.get("search-results", {}).get("entry", [])

            if not entries:
                return []

            for entry in entries:
                result = {
                    "title": entry.get("dc:title", "Untitled"),
                    "authors": self.format_authors(entry.get("authors", {}).get("author", [])),
                    "publication_year": entry.get("prism:coverDate", "")[:4],
                    "abstract": entry.get("dc:description", "No abstract available"),
                    "url": entry.get("prism:url", ""),
                    "cited_by_count": int(entry.get("citedby-count", 0)),
                    "journal": entry.get("prism:publicationName", ""),
                    "doi": entry.get("prism:doi", ""),
                    "similarity_score": 0.95  # Default high score for direct API results
                }
                results.append(result)

            return results
        except requests.exceptions.RequestException as e:
            print(f"Error searching ScienceDirect: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return []

    def format_authors(self, authors: List[Dict]) -> List[Dict]:
        """Format author information to match our existing schema."""
        formatted_authors = []
        for author in authors:
            formatted_authors.append({
                "author": {
                    "display_name": author.get("given-name", "") + " " + author.get("surname", "")
                }
            })
        return formatted_authors