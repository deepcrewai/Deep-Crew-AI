import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict

def create_citation_timeline(results: List[Dict]) -> go.Figure:
    """Create a timeline of citations over years."""
    df = pd.DataFrame([{
        'year': r.get('publication_year'),
        'citations': r.get('cited_by_count', 0)
    } for r in results if r.get('publication_year')])
    
    fig = px.line(
        df.groupby('year')['citations'].sum().reset_index(),
        x='year',
        y='citations',
        title='Citations Over Time'
    )
    return fig

def create_topic_distribution(results: List[Dict]) -> go.Figure:
    """Create a pie chart of topic distribution."""
    topics = []
    for r in results:
        if 'concepts' in r:
            topics.extend([c.get('display_name') for c in r['concepts']])
    
    df = pd.DataFrame(topics, columns=['topic'])
    topic_counts = df['topic'].value_counts().head(10)
    
    fig = px.pie(
        values=topic_counts.values,
        names=topic_counts.index,
        title='Top 10 Research Topics'
    )
    return fig

def create_author_network(results: List[Dict]) -> go.Figure:
    """Create a network visualization of author collaborations."""
    edges = []
    for paper in results:
        authors = [a.get('author', {}).get('display_name') 
                  for a in paper.get('authorships', [])]
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                edges.append((authors[i], authors[j]))
    
    df_edges = pd.DataFrame(edges, columns=['source', 'target'])
    df_edges['weight'] = 1
    df_edges = df_edges.groupby(['source', 'target'])['weight'].sum().reset_index()
    
    fig = go.Figure(data=[
        go.Scatter(
            x=[0, 1, 2],
            y=[0, 1, 0],
            mode='markers+text',
            text=df_edges['source'].unique()[:3],
            textposition="top center"
        )
    ])
    
    fig.update_layout(
        title='Author Collaboration Network (Top Authors)',
        showlegend=False
    )
    return fig
