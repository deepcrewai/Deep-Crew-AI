import requests
from typing import Dict, List

class PatentSearchClient:
    def __init__(self):
        self.base_url = "https://patent-search-genius.username.repl.co"  # Replace with your actual Patent Search Genius URL
    
    def search_patents(self, query: str) -> List[Dict]:
        """Search patents related to the query."""
        try:
            response = requests.get(
                f"{self.base_url}/api/search",
                params={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error searching patents: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error in patent search: {str(e)}")
            return []
            
    def get_patent_details(self, patent_id: str) -> Dict:
        """Get detailed information about a specific patent."""
        try:
            response = requests.get(
                f"{self.base_url}/api/patent/{patent_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting patent details: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"Error fetching patent details: {str(e)}")
            return {}
