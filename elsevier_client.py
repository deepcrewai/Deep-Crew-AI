import os
import requests
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ElsevierClient:
    def __init__(self):
        self.api_key = os.environ.get("ELSEVIER_API_KEY")
        if not self.api_key:
            raise ValueError("ELSEVIER_API_KEY environment variable is not set")
        logger.info("Initializing ElsevierClient")
        self.base_url = "https://api.elsevier.com/content/search/sciencedirect"
        self.headers = {
            "X-ELS-APIKey": self.api_key,
            "Accept": "application/json"
        }

    def search(self, query: str, limit: int = 25) -> List[Dict]:
        """Search for papers in ScienceDirect."""
        try:
            if not query:
                logger.warning("Empty query provided")
                return []

            logger.info(f"Searching ScienceDirect for: {query}")
            params = {
                "query": query,
                "count": limit,
                "start": 0,
                "sort": "-date",  # Sort by date descending
                "field": "all",  # Search in all fields
                "suppressNavLinks": "true"
            }

            logger.debug(f"Making API request to {self.base_url}")
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params
            )

            if response.status_code == 401:
                logger.error("Authentication failed: Invalid API key")
                raise ValueError("Invalid API key. Please check your Elsevier API key.")
            elif response.status_code == 403:
                logger.error("Authorization failed: Insufficient permissions")
                raise ValueError("API key does not have sufficient permissions.")
            elif response.status_code != 200:
                logger.error(f"API request failed with status code: {response.status_code}")
                raise ValueError(f"API request failed with status code: {response.status_code}")

            response.raise_for_status()
            data = response.json()

            # Extract relevant information from response
            results = []
            entries = data.get("search-results", {}).get("entry", [])

            if not entries:
                logger.info("No results found in API response")
                return []

            logger.info(f"Found {len(entries)} results")
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
            logger.error(f"Network error while searching ScienceDirect: {str(e)}")
            raise ValueError(f"Network error while connecting to ScienceDirect: {str(e)}")
        except ValueError as e:
            # Re-raise ValueError for authentication/authorization issues
            raise
        except Exception as e:
            logger.error(f"Unexpected error in search: {str(e)}", exc_info=True)
            raise ValueError(f"Error searching ScienceDirect: {str(e)}")

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