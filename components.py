import streamlit as st
import plotly.express as px
from utils import format_citation, calculate_metrics
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

def generate_pdf_report(results, analysis):
    """Generate a PDF report of search results and analysis."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    y = 750  # Starting y position

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Research Analysis Report")
    y -= 30

    # Date
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 40

    # Papers
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Research Papers")
    y -= 20

    c.setFont("Helvetica", 10)
    for paper in results[:5]:  # Limit to top 5 papers
        if y < 100:  # Check if we need a new page
            c.showPage()
            y = 750

        title = paper.get('title', 'Untitled')
        citation = format_citation(paper)

        c.drawString(50, y, title[:80] + '...' if len(title) > 80 else title)
        y -= 15
        citation_lines = [citation[i:i+80] for i in range(0, len(citation), 80)]
        for line in citation_lines:
            c.drawString(50, y, line)
            y -= 15
        y -= 10

    # Analysis Summary
    if y < 200:  # Ensure enough space for summary
        c.showPage()
        y = 750

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Analysis Summary")
    y -= 20

    c.setFont("Helvetica", 10)
    summary = analysis.get("summary", "No summary available")
    summary_lines = [summary[i:i+80] for i in range(0, len(summary), 80)]
    for line in summary_lines[:10]:  # Limit summary length
        c.drawString(50, y, line)
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer

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

            # Abstract preview with PDF-like styling
            with st.container():
                st.markdown("""
                <style>
                .pdf-preview {
                    background-color: white;
                    border: 1px solid #ddd;
                    padding: 20px;
                    border-radius: 5px;
                    font-family: serif;
                    line-height: 1.6;
                }
                </style>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="pdf-preview">
                <h4>Abstract</h4>
                {paper.get('abstract', 'No abstract available')}
                </div>
                """, unsafe_allow_html=True)

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

def handle_pdf_export(results, analysis):
    """Handle PDF export functionality."""
    # Add export button at the top of the results
    if st.download_button(
        label="📑 Export Results as PDF",
        data=generate_pdf_report(results, analysis),
        file_name="research_report.pdf",
        mime="application/pdf"
    ):
        st.success("PDF report generated successfully!")