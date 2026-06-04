import sys
from pathlib import Path

import fitz
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.retrieval.search_service import (
    get_filter_options,
    is_search_index_ready,
    search_similar_observations,
)
from src.utils.config import QDRANT_COLLECTION_NAME, RAW_DATA_DIR


st.set_page_config(
    page_title="Building Inspection Intelligence",
    page_icon="",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def render_pdf_page(source_file: str, source_page: int) -> bytes:
    source_path = RAW_DATA_DIR / source_file
    with fitz.open(source_path) as document:
        page_index = max(0, min(source_page - 1, document.page_count - 1))
        page = document.load_page(page_index)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
        return pixmap.tobytes("png")


def render_result(result: dict, rank: int) -> None:
    severity = result.get("severity", "unknown")
    category = result.get("category", "Unknown")
    normalized_category = result.get("normalized_category", "Other")
    observation_type = result.get("observation_type", "unknown")
    source_file = result.get("source_file", "Unknown file")
    source_page = result.get("source_page", "Unknown")

    with st.container(border=True):
        top_cols = st.columns([1, 1, 1, 2])
        top_cols[0].metric("Rank", rank)
        top_cols[1].metric("Severity", severity)
        top_cols[2].metric("Page", source_page)
        top_cols[3].metric("Report", source_file)

        st.subheader(result.get("description", "No description"))

        meta_cols = st.columns(3)
        meta_cols[0].caption(f"Type: {observation_type}")
        meta_cols[1].caption(f"Category: {normalized_category}")
        meta_cols[2].caption(f"Location: {result.get('location', 'Unknown')}")
        if category != normalized_category:
            st.caption(f"Original extracted category: {category}")

        recommendation = result.get("recommendation")
        if recommendation:
            st.markdown("**Recommendation**")
            st.write(recommendation)

        source_path = RAW_DATA_DIR / source_file
        if source_path.exists() and isinstance(source_page, int):
            with st.expander("View source report"):
                page_image = render_pdf_page(source_file, source_page)
                st.image(
                    page_image,
                    caption=f"{source_file}, page {source_page}",
                    use_container_width=True,
                )

        st.caption(
            f"Source: {source_file} | Page: {source_page} | "
            f"Observation ID: {result.get('observation_id', 'Unknown')}"
        )


st.title("Building Inspection Intelligence")
st.caption(f"Semantic search over extracted building inspection observations. Collection: {QDRANT_COLLECTION_NAME}")

if not is_search_index_ready():
    st.warning("Search index not found. Run `uv run python -m src.embeddings.index_builder` first.")
    st.stop()

filter_options = get_filter_options()

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
    st.header("Filters")
    selected_types = st.multiselect(
        "Observation type",
        options=filter_options["observation_types"],
    )
    selected_severities = st.multiselect(
        "Severity",
        options=filter_options["severities"],
    )
    selected_categories = st.multiselect(
        "Category",
        options=filter_options["categories"],
    )
    selected_source_files = st.multiselect(
        "Source report",
        options=filter_options["source_files"],
    )

with st.form("observation_search"):
    query = st.text_input("Search technical observations", value=example_query)
    submitted = st.form_submit_button("Search")

if submitted and query.strip():
    with st.spinner("Searching similar observations..."):
        results = search_similar_observations(
            query=query,
            limit=limit,
            observation_types=selected_types,
            severities=selected_severities,
            normalized_categories=selected_categories,
            source_files=selected_source_files,
        )

    st.markdown(f"**{len(results)} results for:** `{query}`")

    for rank, result in enumerate(results, start=1):
        render_result(result, rank)
else:
    st.info("Enter a technical issue or risk, then run search.")
