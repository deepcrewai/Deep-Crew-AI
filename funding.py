import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
from openai import OpenAI
import os
import pandas as pd
import json

class FundingAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"  # Latest model as of May 13, 2024
        self.analysis_prompt = """As an AI funding analyst, provide detailed insights for the following data.
        Focus on:
        - Key trends and patterns in the sector
        - Success factors and potential risks
        - Strategic recommendations for researchers
        - Future outlook and emerging opportunities
        Return analysis in JSON format with:
        {
            'detailed_analysis': 'In-depth sector analysis covering current state and future projections...',
            'key_trends': ['trend1', 'trend2', ...],
            'growth_strategies': ['strategy1', 'strategy2', ...],
            'risk_factors': ['risk1', 'risk2', ...],
            'recommendations': ['rec1', 'rec2', ...]
        }"""

    def get_funding_opportunities(self, research_area: str, region: str = None) -> List[Dict]:
        """Find relevant funding opportunities based on research area and region."""
        try:
            current_year = 2025  # Since today is in 2025
            prompt = {
                "research_area": research_area,
                "region": region if region else "global",
                "request": f"Find funding opportunities with deadlines between {current_year} and {current_year + 2}"
            }

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": f"""As a funding expert, analyze the research area and region to identify ONLY funding opportunities with deadlines between {current_year} and {current_year + 2}. 
                    Return a JSON array of opportunities with the following structure:
                    {{
                        "opportunities": [
                            {{
                                "title": "Grant name",
                                "funder": "Organization name",
                                "funder_url": "Organization website URL",
                                "amount": "Funding amount (format as $X,XXX,XXX)",
                                "deadline": "Application deadline (must be between {current_year} and {current_year + 2})",
                                "eligibility": "Eligibility criteria",
                                "region": "Geographical region",
                                "success_rate": "Estimated success rate",
                                "priority_level": "High/Medium/Low match"
                            }}
                        ]
                    }}"""
                }, {
                    "role": "user",
                    "content": json.dumps(prompt)
                }],
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content).get("opportunities", [])
        except Exception as e:
            print(f"Error finding funding opportunities: {str(e)}")
            return []

    def analyze_funding_trends(self, research_area: str) -> Dict:
        """Analyze current funding trends in the specified research area."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """Analyze current funding trends in the specified research area. 
                    Return a JSON object with the following structure:
                    {
                        "detailed_analysis": "Comprehensive analysis of the sector's current state, challenges, and future outlook...",
                        "key_trends": ["List at least 5 major trends shaping the sector"],
                        "growth_strategies": ["List at least 5 detailed growth strategies"],
                        "risk_factors": ["List at least 3 critical risk factors"],
                        "recommendations": ["Provide at least 5 actionable recommendations"]
                    }"""
                }, {
                    "role": "user",
                    "content": research_area
                }],
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error analyzing funding trends: {str(e)}")
            return {}

def render_funding_section(research_query: str):
    """Render the funding section in the Streamlit app."""
    funding_agent = FundingAgent()

    st.markdown("""
        <div class='results-container'>
            <h2>💰 Funding Analysis</h2>
    """, unsafe_allow_html=True)

    # Region selection
    regions = [
        "Global",
        "North America",
        "Europe",
        "Asia",
        "Africa",
        "South America",
        "Oceania"
    ]
    selected_region = st.selectbox("Select Region", regions)

    # Main tabs
    main_tabs = st.tabs(["Funding Opportunities", "Funding Trends"])

    # Funding Opportunities Tab
    with main_tabs[0]:
        st.markdown("""
            <div class='content-section'>
                <h3>Available Opportunities</h3>
            </div>
        """, unsafe_allow_html=True)
        with st.spinner("🔍 Finding and analyzing funding opportunities..."):
            opportunities = funding_agent.get_funding_opportunities(research_query, selected_region)

            if opportunities:
                st.markdown("### 📑 Available Opportunities")
                for opp in opportunities:
                    with st.expander(f"{opp['title']} - {opp['funder']}"):
                        st.markdown(f"""
                            **Amount:** `{opp['amount']}`  
                            **Deadline:** {opp['deadline']}  
                            **Eligibility:** {opp['eligibility']}  
                            **Success Rate:** {opp['success_rate']}  
                            **Priority Level:** {opp['priority_level']}

                            ---
                            **Institution:** [{opp['funder']}]({opp.get('funder_url', '#')})
                        """)

    # Funding Trends Tab
    with main_tabs[1]:
        trend_tabs = st.tabs(["Sector Analysis", "Success Rates"])

        # Sector Analysis Sub-tab
        with trend_tabs[0]:
            st.markdown("""
                <div class='content-section'>
                    <h3>📊 Sector Analysis</h3>
                </div>
            """, unsafe_allow_html=True)
            with st.spinner("Analyzing sector trends with AI..."):
                trends = funding_agent.analyze_funding_trends(research_query)

                if trends:
                    # AI Analysis
                    st.markdown("#### 🤖 Detailed Analysis")
                    st.write(trends.get('detailed_analysis', 'Analysis not available'))

                    with st.expander("🔍 Growth Strategies"):
                        for strategy in trends.get('growth_strategies', []):
                            st.markdown(f"• {strategy}")

                    st.markdown("#### Key Trends")
                    for trend in trends.get('key_trends', []):
                        st.markdown(f"• {trend}")

                    st.markdown("#### Risk Factors")
                    for risk in trends.get('risk_factors', []):
                        st.markdown(f"• {risk}")

                    st.markdown("#### Recommendations")
                    for rec in trends.get('recommendations', []):
                        st.markdown(f"• {rec}")

        # Success Rates Tab
        with trend_tabs[1]:
            st.markdown("""
                <div class='content-section'>
                    <h3>📈 Success Rates Analysis</h3>
                </div>
            """, unsafe_allow_html=True)
            if trends:
                success_metrics = {
                    "Overall Success Rate": "65%",
                    "Average Processing Time": "3-4 months",
                    "Competition Level": "High"
                }

                for metric, value in success_metrics.items():
                    st.metric(metric, value)

    st.markdown("</div>", unsafe_allow_html=True)