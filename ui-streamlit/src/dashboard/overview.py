import streamlit as st
from db import get_connection
import pandas as pd
import seaborn as sns

def get_user_info(email):
    conn = get_connection()
    cursor = conn.cursor()
    # User info
    cursor.execute("SELECT name, surname, email FROM users WHERE email = %s", (email,))
    user_row = cursor.fetchone()
    
    # User topics
    cursor.execute("""
        SELECT t.name 
        FROM topics t
        JOIN user_topics ut ON t.topic_id = ut.topic_id
        JOIN users u ON u.user_id = ut.user_id
        WHERE u.email = %s
    """, (email,))
    topics_rows = cursor.fetchall()
    conn.close()
    
    user_info = {
        "name": user_row[0],
        "surname": user_row[1],
        "email": user_row[2],
        "topics": [r[0] for r in topics_rows]
    }
    return user_info


def get_feed_count(email=None):
    """
    Optionally we can filter feeds relevant to user's topics
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM rss_feed_content")
    count = cursor.fetchone()[0]
    conn.close()
    return count


import matplotlib.pyplot as plt
import streamlit as st

def plot_feeds_by_rss():
    conn = get_connection()
    df = pd.read_sql("SELECT rss_name, COUNT(*) as num_feeds FROM rss_feed_content GROUP BY rss_name", conn)
    conn.close()
    
    fig, ax = plt.subplots()
    ax.bar(df['rss_name'], df['num_feeds'], color="#4c72b0")
    ax.set_xlabel("RSS Source")
    ax.set_ylabel("Number of feeds")
    ax.set_title("Feeds by Source")
    st.pyplot(fig)



def plot_feeds_by_rss_sns():
    # Fetch feeds grouped by rss_name
    conn = get_connection()
    df = pd.read_sql("""
        SELECT rss_name, COUNT(*) AS num_feeds 
        FROM rss_feed_content 
        GROUP BY rss_name
    """, conn)
    conn.close()

    if df.empty:
        st.info("No feed data to display")
        return

    # Set Seaborn style
    sns.set_theme(style="whitegrid")

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=df,
        x="rss_name",
        y="num_feeds",
        palette="pastel",  # nicer colors
        ax=ax
    )

    ax.set_xlabel("RSS Source", fontsize=12)
    ax.set_ylabel("Number of Feeds", fontsize=12)
    ax.set_title("Feeds by RSS Source", fontsize=14)
    
    # Optional: rotate x labels if many sources
    plt.xticks(rotation=30, ha="right")

    # Display in Streamlit
    st.pyplot(fig)


def overview_page():
    st.title("📊 Dashboard Overview")
    
    # --- User info card ---
    user_info = get_user_info(st.session_state.user)
    st.subheader("👤 Your Profile")
    st.markdown(f"""
    **Name:** {user_info['name']} {user_info['surname']}  
    **Email:** {user_info['email']}  
    **Topics:** {', '.join(user_info['topics']) if user_info['topics'] else 'None selected'}
    """)
    st.divider()
    
    # --- KPI row ---
    feeds_count = get_feed_count()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Feeds", feeds_count)
    col2.metric("Topics Selected", len(user_info['topics']))
    col3.metric("RSS Sources", 5)  # optional static number, could calculate dynamically
    
    st.divider()
    
    # --- Feed chart ---
    st.subheader("Feeds by RSS Source")
    plot_feeds_by_rss()
    plot_feeds_by_rss_sns()