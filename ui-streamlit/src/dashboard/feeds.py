import streamlit as st
from db import fetch_feeds
import datetime

st.markdown(
    """
    <style>
    /* Card container styling */
    .feed-card {
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        transition: transform 0.2s, box-shadow 0.2s;
        background-color: #fafafa;
    }
    .feed-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    /* Feed link hover */
    .feed-card a:hover {
        color: red;
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

EMOJI_MAP = {
    "Tech": "💻",
    "News": "📰",
    "Sports": "🏀",
    "Finance": "💰"
}

def show_feeds(limit=10):
    st.header("📰 Latest Feeds")

    theme = st.sidebar.radio("Theme", ["Light 🌞", "Dark 🌙"])
    if theme == "Dark 🌙":
        st.markdown(
            """
            <style>
            body {
                background-color: #1e1e1e;
                color: #f0f0f0;
            }
            .feed-card {
                background-color: #2a2a2a !important;
                color: #f0f0f0 !important;
            }
            .feed-card a { color: #61dafb !important; }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            body { background-color: #ffffff; color: #000000; }
            .feed-card { background-color: #fafafa !important; color: #000000 !important; }
            .feed-card a { color: #0078d4 !important; }
            </style>
            """,
            unsafe_allow_html=True
        )


    feeds = fetch_feeds(limit)
    if feeds.empty:
        st.info("No feeds available yet.")
        return


    selected_sources = st.multiselect(
        "Select sources to show",
        options=feeds["rss_name"].unique(),
        default=feeds["rss_name"].unique()
    )
    grouped = feeds[feeds["rss_name"].isin(selected_sources)].groupby("rss_name")

    # Group by rss_name
    #grouped = feeds.groupby("rss_name")

    for rss_name, group in grouped:
        emoji = EMOJI_MAP.get(rss_name, "📰")

        # Expander (collapsible)
        with st.expander(f"{emoji} {rss_name} ({len(group)} feeds)", expanded=False):
            # Optional: sort feeds by published date
            group = group.sort_values("published", ascending=False)

            # Grid layout
            n_cols = 3
            cols = st.columns(n_cols)
            for i, row in group.iterrows():
                col = cols[i % n_cols]
                with col:
                    st.markdown(
                        f"""
                        <div class="feed-card">
                            <h4>{row['title']}</h4>
                            <p><b>Feed:</b> {row['rss_feed_name']}</p>
                            <p><b>Published:</b> {row['published']}</p>
                            <p>{row['summary']}</p>
                            <a href="{row['link']}" target="_blank">Read more</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )