import streamlit as st
import plotly.express as px
from utils import format_citation, calculate_metrics
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.lib.utils import ImageReader

def generate_pdf_report(results, analysis):
    """Generate a PDF report of AI analysis."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    page_width, page_height = letter

    def add_page_footer():
        """Add date and link to bottom of page"""
        c.setFont("Helvetica", 10)
        # Add date to bottom left
        c.drawString(50, 30, datetime.now().strftime('%Y-%m-%d'))
        # Add link to bottom right
        c.setFillColorRGB(0, 0, 1)  # Blue color for link
        c.drawString(page_width - 150, 30, "deep-crew.ai")

    # Add logo to top right
    logo = ImageReader("attached_assets/deep-crew.jpg")
    c.drawImage(logo, page_width - 250, page_height - 100, width=200, preserveAspectRatio=True)

    y = page_height - 150  # Start after logo and spacing

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AI Analysis Report")
    y -= 30

    # Date
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 40

    # Analysis Summary
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Research Summary")
    y -= 20

    c.setFont("Helvetica", 10)
    summary = analysis.get("summary", "No summary available")
    summary_lines = [summary[i:i+80] for i in range(0, len(summary), 80)]
    for line in summary_lines:
        if y < 100:  # Check if we need a new page
            add_page_footer()
            c.showPage()
            y = page_height - 50

        c.drawString(50, y, line)
        y -= 15
    y -= 20

    # Research Trends
    if y < 200:  # Ensure enough space for trends section
        add_page_footer()
        c.showPage()
        y = page_height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Research Trends")
    y -= 20

    trends = analysis.get("trends", {})
    c.setFont("Helvetica", 10)

    # Emerging Topics
    c.drawString(50, y, "Emerging Topics:")
    y -= 20
    for topic in trends.get("emerging_topics", []):
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50
        c.drawString(70, y, f"• {topic}")
        y -= 15
    y -= 20

    # Declining Topics
    c.drawString(50, y, "Declining Topics:")
    y -= 20
    for topic in trends.get("declining_topics", []):
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50
        c.drawString(70, y, f"• {topic}")
        y -= 15
    y -= 20

    # Research Gaps
    if y < 200:
        add_page_footer()
        c.showPage()
        y = page_height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Research Gaps")
    y -= 20

    c.setFont("Helvetica", 10)
    for gap in analysis.get("gaps", []):
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50
        c.drawString(70, y, f"• {gap}")
        y -= 15
    y -= 20

    # Complexity Assessment
    if y < 200:
        add_page_footer()
        c.showPage()
        y = page_height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Complexity Assessment")
    y -= 20

    c.setFont("Helvetica", 10)
    complexity = analysis.get("complexity", {})
    score = complexity.get("complexity_score", 0)
    c.drawString(50, y, f"Complexity Score: {score}/10")
    y -= 15

    explanation = complexity.get("explanation", "No explanation available")
    explanation_lines = [explanation[i:i+80] for i in range(0, len(explanation), 80)]
    for line in explanation_lines:
        if y < 100:
            add_page_footer()
            c.showPage()
            y = page_height - 50
        c.drawString(50, y, line)
        y -= 15

    # Add footer to the last page
    add_page_footer()

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

            # Display authors with OpenAlex profiles
            st.write("📚 Authors:")
            for author in paper.get('authors', []):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {author['name']} ({author['institution']})")
                with col2:
                    if author.get('openalex_url'):
                        st.write(f"[OpenAlex Profile]({author['openalex_url']})")

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
    # Initialize the session state for PDF generation if not exists
    if 'pdf_generated' not in st.session_state:
        st.session_state.pdf_generated = False

    # Add export button at the top of the results
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.download_button(
            label="📑 Export Results as PDF",
            data=generate_pdf_report(results, analysis),
            file_name="research_report.pdf",
            mime="application/pdf",
            key="pdf_download"
        ):
            st.session_state.pdf_generated = True

    # Show success message if PDF was generated
    with col2:
        if st.session_state.pdf_generated:
            st.success("PDF report generated successfully!")
            # Reset the state for next time
            st.session_state.pdf_generated = False