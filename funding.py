import streamlit as st
import plotly.express as px
from typing import Dict, List
from openai import OpenAI
import os
import pandas as pd
import json

class FundingAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"  # Latest model as of May 13, 2024
        
    def get_funding_opportunities(self, research_area: str, region: str = None) -> List[Dict]:
        """Find relevant funding opportunities based on research area and region."""
        try:
            prompt = {
                "research_area": research_area,
                "region": region if region else "global",
                "request": "Find relevant funding opportunities"
            }
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """As a funding expert, analyze the research area and region to identify relevant funding opportunities. 
                    Return a JSON array of opportunities with the following structure:
                    {
                        "opportunities": [
                            {
                                "title": "Grant name",
                                "funder": "Organization name",
                                "amount": "Funding amount",
                                "deadline": "Application deadline",
                                "eligibility": "Eligibility criteria",
                                "link": "Application link",
                                "region": "Geographical region",
                                "success_rate": "Estimated success rate",
                                "priority_level": "High/Medium/Low match"
                            }
                        ]
                    }"""
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
                        "trending_areas": ["area1", "area2", "area3"],
                        "top_funders": [
                            {"name": "funder name", "focus_areas": ["area1", "area2"], "typical_amount": "amount range"}
                        ],
                        "emerging_opportunities": ["opportunity1", "opportunity2"],
                        "funding_cycles": {"peak_months": ["month1", "month2"], "preparation_time": "recommended time"},
                        "success_factors": ["factor1", "factor2"]
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
    
    def get_regional_insights(self, region: str) -> Dict:
        """Get funding insights for a specific region."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": """Provide regional funding insights. 
                    Return a JSON object with the following structure:
                    {
                        "total_funding_available": "amount",
                        "key_organizations": ["org1", "org2"],
                        "regional_priorities": ["priority1", "priority2"],
                        "success_stories": ["story1", "story2"],
                        "local_resources": ["resource1", "resource2"],
                        "upcoming_deadlines": [
                            {"program": "name", "deadline": "date", "amount": "funding amount"}
                        ]
                    }"""
                }, {
                    "role": "user",
                    "content": region
                }],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error getting regional insights: {str(e)}")
            return {}
    
    def generate_opportunity_heatmap(self, opportunities: List[Dict]) -> None:
        """Generate a heatmap visualization of funding opportunities."""
        try:
            # Convert opportunities to DataFrame for visualization
            df = pd.DataFrame(opportunities)
            
            # Create a heatmap using plotly
            fig = px.density_heatmap(
                df,
                x="region",
                y="amount",
                title="Funding Opportunity Heatmap",
                labels={"region": "Region", "amount": "Funding Amount"},
                color_continuous_scale="Viridis"
            )
            
            # Display the heatmap
            st.plotly_chart(fig)
            
        except Exception as e:
            st.error(f"Error generating heatmap: {str(e)}")

def render_funding_section(research_query: str):
    """Render the funding section in the Streamlit app."""
    funding_agent = FundingAgent()

    st.markdown("## 💰 Funding Analysis")

    # Region selection
    regions = ["Global", "North America", "Europe", "Asia", "Africa", "South America", "Oceania"]
    selected_region = st.selectbox("Select Region", regions)

    # Main tabs
    main_tabs = st.tabs(["Funding Opportunities", "Funding Trends", "Regional Insights"])

    # Funding Opportunities Tab
    with main_tabs[0]:
        st.markdown("### Available Opportunities")
        with st.spinner("🔍 Finding funding opportunities..."):
            opportunities = funding_agent.get_funding_opportunities(research_query, selected_region)

        if opportunities:
            for opp in opportunities:
                with st.expander(f"{opp['title']} - {opp['funder']}"):
                    st.markdown(f"**Amount:** {opp['amount']}")
                    st.markdown(f"**Deadline:** {opp['deadline']}")
                    st.markdown(f"**Eligibility:** {opp['eligibility']}")
                    st.markdown(f"**Success Rate:** {opp['success_rate']}")
                    st.markdown(f"**Priority Level:** {opp['priority_level']}")
                    st.markdown(f"**[Apply Now]({opp['link']})**")

    # Funding Trends Tab
    with main_tabs[1]:
        trend_tabs = st.tabs(["Sector Analysis", "Success Rates", "Market Analysis"])

        # Sector Analysis Sub-tab
        with trend_tabs[0]:
            st.markdown("### 📊 Sector Analysis")
            with st.spinner("Analyzing sector trends..."):
                trends = funding_agent.analyze_funding_trends(research_query)

                if trends:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Trending Areas")
                        for area in trends.get("trending_areas", []):
                            st.markdown(f"• {area}")

                    with col2:
                        st.markdown("#### Top Funders")
                        for funder in trends.get("top_funders", []):
                            st.markdown(f"• **{funder['name']}**")
                            st.markdown(f"  - Focus: {', '.join(funder['focus_areas'])}")
                            st.markdown(f"  - Typical Amount: {funder['typical_amount']}")

        # Success Rates Sub-tab
        with trend_tabs[1]:
            st.markdown("### 📈 Success Rates Analysis")
            if trends:
                st.markdown("#### Funding Cycles")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Peak Application Months**")
                    for month in trends.get("funding_cycles", {}).get("peak_months", []):
                        st.markdown(f"• {month}")
                with col2:
                    st.markdown("**Success Factors**")
                    for factor in trends.get("success_factors", []):
                        st.markdown(f"• {factor}")

        # Market Analysis Sub-tab
        with trend_tabs[2]:
            st.markdown("### 🌍 Market Analysis")
            if trends:
                st.markdown("#### Emerging Opportunities")
                for opp in trends.get("emerging_opportunities", []):
                    st.markdown(f"• {opp}")

                # Add opportunity heatmap
                if opportunities:
                    st.markdown("#### Funding Distribution")
                    funding_agent.generate_opportunity_heatmap(opportunities)

    # Regional Insights Tab
    with main_tabs[2]:
        st.markdown("### 🌐 Regional Funding Landscape")
        if selected_region != "Global":
            with st.spinner(f"Getting insights for {selected_region}..."):
                insights = funding_agent.get_regional_insights(selected_region)

            if insights:
                st.markdown(f"**Total Available Funding:** {insights['total_funding_available']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Key Organizations")
                    for org in insights.get("key_organizations", []):
                        st.markdown(f"• {org}")

                with col2:
                    st.markdown("#### Regional Priorities")
                    for priority in insights.get("regional_priorities", []):
                        st.markdown(f"• {priority}")

                st.markdown("#### Upcoming Deadlines")
                for deadline in insights.get("upcoming_deadlines", []):
                    st.markdown(f"• **{deadline['program']}**")
                    st.markdown(f"  - Deadline: {deadline['deadline']}")
                    st.markdown(f"  - Amount: {deadline['amount']}")