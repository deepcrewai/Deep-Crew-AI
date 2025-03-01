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

        # Strip any whitespace from the API key
        self.api_key = self.api_key.strip()

        # Log a masked version of the API key for debugging
        masked_key = f"{self.api_key[:4]}...{self.api_key[-4:]}" if len(self.api_key) > 8 else "***"
        logger.info(f"Initializing ElsevierClient with API key starting with: {masked_key}")

        self.base_url = "https://api.elsevier.com/content/search/sciencedirect"
        self.headers = {
            "X-ELS-APIKey": self.api_key,
            "Accept": "application/json"
        }

    def test_connection(self) -> bool:
        """Test the API connection and permissions."""
        try:
            # Try to access the ScienceDirect API info endpoint
            response = requests.get(
                "https://api.elsevier.com/content/serial/title",
                headers=self.headers,
                params={"issn": "0004-3702"}  # AI journal ISSN as test
            )

            if response.status_code == 200:
                logger.info("Successfully connected to Elsevier API")
                return True
            elif response.status_code == 401:
                logger.error("Authentication failed: Invalid API key")
                raise ValueError("Invalid API key. Please check your Elsevier API key and ensure it has access to ScienceDirect API.")
            elif response.status_code == 403:
                logger.error("Authorization failed: Insufficient permissions")
                raise ValueError("API key does not have sufficient permissions. Please ensure your API key has access to ScienceDirect API.")
            else:
                logger.error(f"API request failed with status code: {response.status_code}")
                error_message = response.json().get('error-message', str(response.content))
                raise ValueError(f"API request failed with status code {response.status_code}: {error_message}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while testing API connection: {str(e)}")
            raise ValueError(f"Network error while connecting to Elsevier API: {str(e)}")

    def search(self, query: str, limit: int = 25) -> List[Dict]:
        """Search for papers in ScienceDirect."""
        try:
            if not query:
                logger.warning("Empty query provided")
                return []

            # First test the connection
            self.test_connection()

            logger.info(f"Searching ScienceDirect for: {query}")
            params = {
                "query": query,
                "count": limit,
                "start": 0,
                "sort": "-date",  # Sort by date descending
                "field": "all",  # Search in all fields
                "httpAccept": "application/json",
                "suppressNavLinks": "true"
            }

            logger.debug(f"Making API request to {self.base_url}")
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params
            )

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
                    "authorships": self.format_authors(entry.get("authors", {}).get("author", [])),
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