import os
import requests
from typing import List, Dict

class ElsevierClient:
    def __init__(self):
        self.api_key = os.environ.get("ELSEVIER_API_KEY")
        self.base_url = "https://api.elsevier.com/content/search/sciencedirect"
        self.headers = {
            "X-ELS-APIKey": self.api_key,
            "Accept": "application/json"
        }

    def search(self, query: str, limit: int = 25) -> List[Dict]:
        """Search for papers in ScienceDirect."""
        try:
            params = {
                "query": query,
                "count": limit,
                "start": 0,
                "sort": "-date"  # Sort by date descending
            }

            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()

            # Extract relevant information from response
            results = []
            for entry in data.get("search-results", {}).get("entry", []):
                result = {
                    "title": entry.get("dc:title", "Untitled"),
                    "authors": entry.get("authors", []),
                    "publication_year": entry.get("prism:coverDate", "")[:4],
                    "abstract": entry.get("dc:description", ""),
                    "url": entry.get("prism:url", ""),
                    "cited_by_count": int(entry.get("citedby-count", 0)),
                    "journal": entry.get("prism:publicationName", ""),
                    "doi": entry.get("prism:doi", ""),
                    "similarity_score": 1.0  # Default score, can be adjusted based on relevance
                }
                results.append(result)

            return results
        except Exception as e:
            print(f"Error searching ScienceDirect: {str(e)}")
            return []

    def format_authors(self, authors: List[Dict]) -> List[Dict]:
        """Format author information to match our existing schema."""
        formatted_authors = []
        for author in authors:
            formatted_authors.append({
                "author": {
                    "display_name": author.get("name", "Unknown Author")
                }
            })
        return formatted_authors
