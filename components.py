import streamlit as st
import plotly.express as px
from utils import format_citation, calculate_metrics

def render_search_section(results):
    """Render the search results section."""
    metrics = calculate_metrics(results)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Papers", metrics["total_papers"])
    col2.metric("Total Citations", metrics["total_citations"])
    col3.metric("Average Year", metrics["avg_year"])
    col4.metric("Average Citations", metrics["avg_citations"])

    # Display results
    st.subheader("Search Results")
    for paper in results:
        with st.expander(paper.get("title", "Untitled")):
            st.write(format_citation(paper))
            st.write(f"Citations: {paper.get('cited_by_count', 0)}")
            st.write(f"Abstract: {paper.get('abstract', 'No abstract available')}")

def render_analysis_section(analysis):
    """Render the AI analysis section."""
    st.header("AI Analysis")

    # Summary
    st.subheader("Research Summary")
    st.write(analysis["summary"])

    # Trends
    st.subheader("Research Trends")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Emerging Topics")
        for topic in analysis["trends"]["emerging_topics"]:
            st.write(f"• {topic}")
    with col2:
        st.write("Declining Topics")
        for topic in analysis["trends"]["declining_topics"]:
            st.write(f"• {topic}")

    # Research Gaps
    st.subheader("Research Gaps")
    for gap in analysis["gaps"]:
        st.write(f"• {gap}")

    # Keyword Suggestions
    st.subheader("Keyword Suggestions")
    st.write("Consider using these keywords to refine your search:")
    cols = st.columns(3)
    for i, keyword in enumerate(analysis["keywords"]):
        cols[i % 3].write(f"• {keyword}")

    # Complexity Assessment
    st.subheader("Complexity Assessment")
    complexity = analysis["complexity"]
    st.progress(complexity["complexity_score"] / 10)
    st.write(f"Complexity Score: {complexity['complexity_score']}/10")
    st.write(complexity["explanation"])
