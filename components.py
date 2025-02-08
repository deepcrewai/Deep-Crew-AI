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
        similarity = paper.get('similarity_score', 0)
        with st.expander(f"{paper.get('title', 'Untitled')} (Similarity: {similarity:.2f})"):
            st.write(format_citation(paper))
            if paper.get('url'):
                st.write(f"🔗 [View Paper]({paper['url']})")
            st.write(f"Citations: {paper.get('cited_by_count', 0)}")
            st.write(f"Abstract: {paper.get('abstract')}")

def render_analysis_section(analysis):
    """Render the AI analysis section."""
    st.header("AI Analysis")

    # Summary
    st.subheader("Research Summary")
    st.write(analysis.get("summary", "No summary available"))

    # Trends
    st.subheader("Research Trends")
    trends = analysis.get("trends", {})
    col1, col2 = st.columns(2)
    with col1:
        st.write("Emerging Topics")
        for topic in trends.get("emerging_topics", []):
            st.write(f"• {topic}")
    with col2:
        st.write("Declining Topics")
        for topic in trends.get("declining_topics", []):
            st.write(f"• {topic}")

    # Research Gaps
    st.subheader("Research Gaps")
    for gap in analysis.get("gaps", []):
        st.write(f"• {gap}")

    # Keyword Suggestions
    st.subheader("Keyword Suggestions")
    st.write("Consider using these keywords to refine your search:")
    keywords = analysis.get("keywords", [])
    if keywords:
        cols = st.columns(3)
        for i, keyword in enumerate(keywords):
            cols[i % 3].write(f"• {keyword}")

    # Complexity Assessment
    st.subheader("Complexity Assessment")
    complexity = analysis.get("complexity", {})
    score = complexity.get("complexity_score", 0)
    st.progress(score / 10)
    st.write(f"Complexity Score: {score}/10")
    st.write(complexity.get("explanation", "No explanation available"))