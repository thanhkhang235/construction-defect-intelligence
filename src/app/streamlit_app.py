import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.retrieval.search_service import (
    is_search_index_ready,
    search_similar_observations,
)
from src.utils.config import QDRANT_COLLECTION_NAME


st.set_page_config(
    page_title="Building Inspection Intelligence",
    page_icon="",
    layout="wide",
)


def render_result(result: dict, rank: int) -> None:
    severity = result.get("severity", "unknown")
    category = result.get("category", "Unknown")
    observation_type = result.get("observation_type", "unknown")

    with st.container(border=True):
        top_cols = st.columns([1, 1, 1, 1])
        top_cols[0].metric("Rank", rank)
        top_cols[1].metric("Score", f"{result['score']:.3f}")
        top_cols[2].metric("Severity", severity)
        top_cols[3].metric("Page", result.get("source_page", "Unknown"))

        st.subheader(result.get("description", "No description"))

        meta_cols = st.columns(3)
        meta_cols[0].caption(f"Type: {observation_type}")
        meta_cols[1].caption(f"Category: {category}")
        meta_cols[2].caption(f"Location: {result.get('location', 'Unknown')}")

        recommendation = result.get("recommendation")
        if recommendation:
            st.markdown("**Recommendation**")
            st.write(recommendation)

        st.caption(
            f"Source: {result.get('source_file', 'Unknown file')} | "
            f"Observation ID: {result.get('observation_id', 'Unknown')}"
        )


st.title("Building Inspection Intelligence")
st.caption(f"Semantic search over extracted building inspection observations. Collection: {QDRANT_COLLECTION_NAME}")

if not is_search_index_ready():
    st.warning("Search index not found. Run `uv run python -m src.embeddings.index_builder` first.")
    st.stop()

with st.sidebar:
    st.header("Search")
    limit = st.slider("Results", min_value=1, max_value=10, value=5)
    example_query = st.selectbox(
        "Example query",
        [
            "water leakage near roof",
            "termite damage to timber structure",
            "foundation drainage issue",
            "electrical clearance compliance risk",
        ],
    )

with st.form("observation_search"):
    query = st.text_input("Search technical observations", value=example_query)
    submitted = st.form_submit_button("Search")

if submitted and query.strip():
    with st.spinner("Searching similar observations..."):
        results = search_similar_observations(query=query, limit=limit)

    st.markdown(f"**{len(results)} results for:** `{query}`")

    for rank, result in enumerate(results, start=1):
        render_result(result, rank)
else:
    st.info("Enter a technical issue or risk, then run search.")
