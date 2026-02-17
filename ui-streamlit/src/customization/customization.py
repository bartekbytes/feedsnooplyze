import streamlit as st
from db import get_available_topics, save_user_topics


    # Initialize session_state for selected topics
if "selected_topics" not in st.session_state:
    st.session_state.selected_topics = []


def show():

    
    default_color = "#888888"

    # predefined_topics = {
    #     # 📰 News / Politics
    #     "Politics": {"color": "#e74c3c", "icon": "🏛️"},
    #     "Economy": {"color": "#e74c3c", "icon": "💰"},
    #     "World News": {"color": "#e74c3c", "icon": "🗞️"},
    #     "Technology News": {"color": "#e74c3c", "icon": "💻"},

    #     # 🌍 Travel / Geography
    #     "Travel": {"color": "#3498db", "icon": "✈️"},
    #     "Asia": {"color": "#3498db", "icon": "🌏"},
    #     "Europe": {"color": "#3498db", "icon": "🌍"},
    #     "Nature": {"color": "#3498db", "icon": "🌲"},
    #     "Adventure": {"color": "#3498db", "icon": "🧗"},

    #     # 🍽️ Food / Lifestyle
    #     "Cooking": {"color": "#f39c12", "icon": "👩‍🍳"},
    #     "Eating": {"color": "#f39c12", "icon": "🍴"},
    #     "Baking": {"color": "#f39c12", "icon": "🧁"},
    #     "Restaurants": {"color": "#f39c12", "icon": "🍽️"},
    #     "Coffee": {"color": "#f39c12", "icon": "☕"},

    #     # 📸 Photography / Art
    #     "Photography": {"color": "#9b59b6", "icon": "📷"},
    #     "Art": {"color": "#9b59b6", "icon": "🎨"},
    #     "Design": {"color": "#9b59b6", "icon": "🖌️"},
    #     "Digital Art": {"color": "#9b59b6", "icon": "💻"},

    #     # ⚽ Sports / Fitness
    #     "Football": {"color": "#2ecc71", "icon": "⚽"},
    #     "Basketball": {"color": "#2ecc71", "icon": "🏀"},
    #     "Tennis": {"color": "#2ecc71", "icon": "🎾"},
    #     "Fitness": {"color": "#2ecc71", "icon": "🏋️"},
    #     "Running": {"color": "#2ecc71", "icon": "🏃"},

    #     # 🧠 Science / Knowledge
    #     "Science": {"color": "#1abc9c", "icon": "🔬"},
    #     "Space": {"color": "#1abc9c", "icon": "🚀"},
    #     "Health": {"color": "#1abc9c", "icon": "💊"},
    #     "Environment": {"color": "#1abc9c", "icon": "🌱"},
    #     "Psychology": {"color": "#1abc9c", "icon": "🧠"},

    #     # 🎵 Entertainment / Media
    #     "Movies": {"color": "#e67e22", "icon": "🎬"},
    #     "Music": {"color": "#e67e22", "icon": "🎵"},
    #     "Gaming": {"color": "#e67e22", "icon": "🎮"},
    #     "TV Shows": {"color": "#e67e22", "icon": "📺"},
    #     "Books": {"color": "#e67e22", "icon": "📚"},
    # }

    # -----------------------------------
    # Centered Layout
    # -----------------------------------
    left, center, right = st.columns([1, 2, 1])

    with center:

        st.title("👤 You as Well-Informed Person")
        st.write("### Tell us more about you.")

        name = st.text_input("Name", key="name")
        surname = st.text_input("Surname", key="surname")

        st.title("🎨 Customize Your Experience")
        st.write("### Tell us your interests so we can personalize your dashboard.")


        # Get topics from DB
        topics = get_available_topics() 

        # Initialize session_state
        if "selected_topics" not in st.session_state:
            st.session_state.selected_topics = []

        # Top bar: Deselect All button + counter
        topics_top_deselect, topics_top_counter = st.columns([1, 1])  # two columns: button + counter

        with topics_top_deselect:
            if st.button("Deselect All"):
                st.session_state.selected_topics = []

        st.write("### Click to select topics:")

        # Display tags in 5 columns
        num_cols = 5
        cols = st.columns(num_cols)

        for idx, tag in enumerate(topics):
            col = cols[idx % num_cols]
            data = topics.get(tag, {"color": default_color, "icon": ""})
            color = data["color"]
            icon = data["icon"]
            
            # Style based on selection
            # if tag in st.session_state.selected_topics:
            #     bg_color = color
            #     text_color = "white"
            #     font_weight = "bold"
            # else:
            #     bg_color = "#f0f0f0"
            #     text_color = color
            #     font_weight = "normal"
            
            # Button toggles selection
            if col.button(f"{icon} {tag}" if icon else tag, key=tag):
                if tag in st.session_state.selected_topics:
                    st.session_state.selected_topics.remove(tag)
                else:
                    if len(st.session_state.selected_topics) < 10:
                        st.session_state.selected_topics.append(tag)
                    else:
                        st.warning("You can select up to 10 topics only!")
        
        with topics_top_counter:
            st.markdown(f"**Selected: {len(st.session_state.selected_topics)} / 10**")


        # Display selected tags inline
        if st.session_state.selected_topics:
            inline_tags = ""
            for tag in st.session_state.selected_topics:
                data = topics.get(tag, {"color": default_color, "icon": ""})
                inline_tags += f"<span style='background-color:{data['color']}; color:white; padding:5px 10px; border-radius:10px; margin:3px; display:inline-block;'>{data['icon']} {tag}</span> " if data["icon"] else f"<span style='background-color:{data['color']}; color:white; padding:5px 10px; border-radius:10px; margin:3px; display:inline-block;'>{tag}</span> "
            st.markdown("### Selected Tags:")
            st.markdown(inline_tags, unsafe_allow_html=True)


        selected_topics_list = st.session_state.selected_topics

        if st.button("Save Preferences"):
            if not selected_topics_list or not name or not surname:
                st.warning("Please provide your name and surname and select at least one topic.")
            else:
                # Save to DB
                save_user_topics(st.session_state["user"], selected_topics_list, name, surname)
                # Mark user as customized
                st.session_state["needs_customization"] = False
                st.success("Preferences saved! Redirecting to dashboard...")
                st.session_state.selected_topics = []
                st.rerun()