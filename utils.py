import streamlit as st

def setup_page():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Academic Literature Analyzer",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def format_citation(paper: dict) -> str:
    """Format paper information as a citation."""
    authors = paper.get("authorships", [])
    author_names = [a.get("author", {}).get("display_name", "") for a in authors]
    author_text = ", ".join(author_names[:3])
    if len(author_names) > 3:
        author_text += " et al."
    
    return f"{author_text} ({paper.get('publication_year', 'n.d.')}). {paper.get('title', '')}. {paper.get('host_venue', {}).get('display_name', '')}"

def calculate_metrics(results: list) -> dict:
    """Calculate basic bibliometric metrics."""
    total_citations = sum(r.get("cited_by_count", 0) for r in results)
    years = [r.get("publication_year", 0) for r in results]
    avg_year = sum(years) / len(years) if years else 0
    
    return {
        "total_papers": len(results),
        "total_citations": total_citations,
        "avg_year": round(avg_year, 1),
        "avg_citations": round(total_citations / len(results), 1) if results else 0
    }
