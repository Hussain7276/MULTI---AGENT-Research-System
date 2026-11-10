import time
import streamlit as st

from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)

# ---------------------------------------------------------------------------
# Page config & styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container {padding-top: 2rem; max-width: 1100px;}
        .step-title {font-weight: 600; font-size: 1.05rem;}
        div[data-testid="stStatusWidget"] {font-size: 0.95rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"topic": ..., "result": ...}


# ---------------------------------------------------------------------------
# Pipeline (same logic as pipeline.py, but reports progress to the UI)
# ---------------------------------------------------------------------------
def run_pipeline_with_ui(topic: str) -> dict:
    state = {}
    timings = {}

    progress = st.progress(0, text="Starting research pipeline...")

    # Step 1 - Search agent
    with st.status("🔍 Step 1 — Search agent is working...", expanded=True) as s1:
        t0 = time.time()
        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Find recent, reliable and detailed information about: {topic}",
                    )
                ]
            }
        )
        state["search_results"] = search_result["messages"][-1].content
        timings["search"] = time.time() - t0
        st.write("Search complete.")
        s1.update(
            label=f"🔍 Step 1 — Search complete ({timings['search']:.1f}s)",
            state="complete",
            expanded=False,
        )
    progress.progress(25, text="Search done. Reading top resources...")

    # Step 2 - Reader agent
    with st.status("📖 Step 2 — Reader agent is scraping top resources...", expanded=True) as s2:
        t0 = time.time()
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}",
                    )
                ]
            }
        )
        state["scraped_content"] = reader_result["messages"][-1].content
        timings["reader"] = time.time() - t0
        st.write("Scraping complete.")
        s2.update(
            label=f"📖 Step 2 — Scraping complete ({timings['reader']:.1f}s)",
            state="complete",
            expanded=False,
        )
    progress.progress(50, text="Content gathered. Drafting report...")

    # Step 3 - Writer chain
    with st.status("✍️ Step 3 — Writer is drafting the report...", expanded=True) as s3:
        t0 = time.time()
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke(
            {"topic": topic, "research": research_combined}
        )
        timings["writer"] = time.time() - t0
        st.write("Draft complete.")
        s3.update(
            label=f"✍️ Step 3 — Report drafted ({timings['writer']:.1f}s)",
            state="complete",
            expanded=False,
        )
    progress.progress(75, text="Report drafted. Critic is reviewing...")

    # Step 4 - Critic chain
    with st.status("🧐 Step 4 — Critic is reviewing the report...", expanded=True) as s4:
        t0 = time.time()
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        timings["critic"] = time.time() - t0
        st.write("Review complete.")
        s4.update(
            label=f"🧐 Step 4 — Review complete ({timings['critic']:.1f}s)",
            state="complete",
            expanded=False,
        )
    progress.progress(100, text="Done!")

    state["timings"] = timings
    return state


def as_text(value) -> str:
    """Chain outputs may be str or message objects; normalise to text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return getattr(value, "content", str(value))


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🔎 Research Agent")
    st.caption("Search → Read → Write → Critique")

    st.markdown("### Pipeline")
    st.markdown(
        "1. **Search agent** finds sources\n"
        "2. **Reader agent** scrapes the best one\n"
        "3. **Writer** drafts the report\n"
        "4. **Critic** reviews the draft"
    )

    st.divider()
    st.markdown("### History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            idx = len(st.session_state.history) - 1 - i
            if st.button(item["topic"], key=f"hist_{idx}", use_container_width=True):
                st.session_state.result = item
                st.rerun()
        if st.button("🗑️ Clear history", use_container_width=True):
            st.session_state.history = []
            st.session_state.result = None
            st.rerun()
    else:
        st.caption("No past researches yet.")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.title("Multi-Agent Research System")
st.write("Enter a topic and let the agents research, write, and review a report for you.")

with st.form("research_form", clear_on_submit=False):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Latest advances in solid-state batteries",
    )
    submitted = st.form_submit_button("🚀 Run research", type="primary")

if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        try:
            result = run_pipeline_with_ui(topic.strip())
            entry = {"topic": topic.strip(), **result}
            st.session_state.result = entry
            st.session_state.history.append(entry)
            st.success("Research complete!")
        except Exception as e:
            st.error(f"Something went wrong while running the pipeline: {e}")
            st.exception(e)

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
res = st.session_state.result
if res:
    st.divider()
    st.subheader(f"Results: {res['topic']}")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📖 Scraped Content"]
    )

    report_text = as_text(res.get("report"))
    feedback_text = as_text(res.get("feedback"))

    with tab_report:
        st.markdown(report_text)
        st.download_button(
            "⬇️ Download report (.md)",
            data=report_text,
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown(feedback_text)

    with tab_search:
        st.markdown(as_text(res.get("search_results")))

    with tab_scraped:
        st.markdown(as_text(res.get("scraped_content")))

    timings = res.get("timings")
    if timings:
        st.caption(
            "Timings — "
            + " · ".join(f"{k}: {v:.1f}s" for k, v in timings.items())
            + f" · total: {sum(timings.values()):.1f}s"
        )