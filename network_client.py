import requests
from typing import Dict, List, Optional
import os
import json
import streamlit as st

class NetworkAgent:
    def __init__(self):
        self.base_url = "https://pub.orcid.org/v3.0"
        self.headers = {
            "Accept": "application/json"
        }

    def search_orcid(self, author_name: str) -> Optional[Dict]:
        """Search for an author's ORCID profile."""
        try:
            # Format the query
            query = f"q=given-names:{author_name.split()[0]}+AND+family-name:{author_name.split()[-1]}"

            # Make the request
            response = requests.get(
                f"{self.base_url}/expanded-search/?{query}",
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('num-found', 0) > 0:
                    result = data['expanded-result'][0]
                    return {
                        'orcid': result.get('orcid-id'),
                        'given_name': result.get('given-names'),
                        'family_name': result.get('family-names'),
                        'institution': result.get('institution-name', [{}])[0].get('value', 'Not available'),
                        'country': result.get('country', 'Not available')
                    }
            return None
        except Exception as e:
            print(f"Error searching ORCID for {author_name}: {str(e)}")
            return None

    def get_detailed_profile(self, orcid_id: str) -> Optional[Dict]:
        """Get detailed profile information for an ORCID ID."""
        try:
            response = requests.get(
                f"{self.base_url}/{orcid_id}/person",
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                emails = []
                if 'emails' in data and 'email' in data['emails']:
                    for email in data['emails']['email']:
                        if email.get('verified') and email.get('visibility') == 'public':
                            emails.append(email.get('email'))

                return {
                    'orcid_id': orcid_id,
                    'emails': emails,
                    'biography': data.get('biography', {}).get('content', 'Not available'),
                    'keywords': [kw.get('content') for kw in data.get('keywords', {}).get('keyword', [])],
                    'countries': [country.get('country', {}).get('value') 
                                for country in data.get('addresses', {}).get('address', [])]
                }
            return None
        except Exception as e:
            print(f"Error fetching ORCID profile {orcid_id}: {str(e)}")
            return None

    def enrich_author_information(self, authors: List[Dict]) -> List[Dict]:
        """Enrich author information with ORCID data."""
        enriched_authors = []

        for author in authors:
            author_name = author.get('display_name', '')
            if not author_name:
                continue

            # First try to get ORCID profile
            orcid_info = self.search_orcid(author_name)
            if orcid_info:
                # Get detailed profile if ORCID was found
                detailed_info = self.get_detailed_profile(orcid_info['orcid'])

                enriched_author = {
                    **author,
                    'orcid_id': orcid_info['orcid'],
                    'institution': orcid_info['institution'],
                    'country': orcid_info['country']
                }

                if detailed_info:
                    enriched_author.update({
                        'contact_emails': detailed_info['emails'],
                        'biography': detailed_info['biography'],
                        'research_keywords': detailed_info['keywords'],
                        'countries': detailed_info['countries']
                    })

                enriched_authors.append(enriched_author)
            else:
                # If no ORCID found, keep original author info
                enriched_authors.append(author)

        return enriched_authors

def render_network_section(authors: List[Dict]):
    """Render the network analysis section in Streamlit."""
    st.markdown("""
        <div class='network-section'>
            <h2>Research Network Analysis</h2>
        </div>
    """, unsafe_allow_html=True)

    network_agent = NetworkAgent()

    with st.spinner("🔍 Analyzing research network..."):
        enriched_authors = network_agent.enrich_author_information(authors)

        for author in enriched_authors:
            with st.expander(f"👤 {author.get('display_name', 'Unknown Author')}"):
                st.markdown(f"""
                    **Institution:** {author.get('institution', 'Not available')}  
                    **Country:** {author.get('country', 'Not available')}  
                    **ORCID ID:** {author.get('orcid_id', 'Not available')}

                    **Research Keywords:** {', '.join(author.get('research_keywords', ['Not available']))}

                    **Biography:**  
                    {author.get('biography', 'Not available')}

                    **Contact:**  
                    {', '.join(author.get('contact_emails', ['Not available']))}
                """)