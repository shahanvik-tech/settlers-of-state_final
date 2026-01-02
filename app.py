import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import random
import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="HexPolitic | Strategy & Simulation",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- AESTHETIC STYLING (CSS) ---
st.markdown("""
    <style>
    /* Main Background - Parchment/Clean Tone */
    .stApp {
        background-color: #FDFBF7;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        color: #2C3E50;
    }
    p, div {
        font-family: 'Helvetica Neue', sans-serif;
        color: #4A4A4A;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #2C3E50;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] span {
        color: #ECF0F1 !important;
    }
    
    /* Custom Card Styling for Posts */
    .post-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #D35400; /* Brick Red */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIMULATION ENGINE ---
def draw_map(scarcity_level):
    """Generates the Catan-style map based on economic scarcity."""
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_alpha(0) # Transparent background
    ax.set_aspect('equal')
    
    coord = [(0,0), (0,1), (0,-1), (1,0), (-1,0), (1,-1), (-1,1), 
             (0,2), (0,-2), (2,0), (-2,0), (1,1), (-1,-1), (1,-2), (-1,2), (2,-1), (-2,1)]
    
    # Hex Colors: Wheat(Gold), Ore(Grey), Brick(Red), Wood(Green), Sheep(White)
    colors = ['#F1C40F', '#7F8C8D', '#C0392B', '#27AE60', '#ECF0F1']
    
    for x, y in coord:
        shift_x = x * np.sqrt(3) + y * np.sqrt(3)/2
        shift_y = y * 1.5
        
        # Simulation Logic: High scarcity = 'Burnt' resource tiles (Black)
        if random.random() < (scarcity_level / 100):
            hex_color = '#2C3E50' # Failed State / Embargo
        else:
            hex_color = random.choice(colors)
            
        hex = RegularPolygon((shift_x, shift_y), numVertices=6, radius=1, 
                             orientation=np.radians(30), 
                             facecolor=hex_color, edgecolor='#2C3E50', linewidth=1.5)
        ax.add_patch(hex)
        
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axis('off')
    return fig

# --- CONTENT DATABASE (EDIT THIS TO ADD POSTS) ---
# This is where you add new articles.
blog_posts = [
    {
        "title": "The Silicon Blockade",
        "date": "2026-01-02",
        "tag": "Tech War",
        "summary": "Analyzing the impact of Ore (Rare Earth) restrictions on global chip supply chains.",
        "scarcity_setting": 65, # The simulation setting for this post
        "link": "https://substack.com"
    },
    {
        "title": "Wheat as a Weapon",
        "date": "2025-12-24",
        "tag": "Agriculture",
        "summary": "When the 'Breadbasket' hexes fail, political instability follows. A historical comparison.",
        "scarcity_setting": 30,
        "link": "https://substack.com"
    }
]

# --- MAIN APP NAVIGATION ---
st.sidebar.title("⬡ HexPolitic")
st.sidebar.caption("Global Strategy & Simulation")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Intelligence Dashboard", "Mission & About", "Consultant AI"])

st.sidebar.markdown("---")
st.sidebar.info("Subscribe to the weekly briefing on Substack.")

# ==========================================
# PAGE 1: INTELLIGENCE DASHBOARD (HOME)
# ==========================================
if page == "Intelligence Dashboard":
    st.title("Global Situation Room")
    st.markdown("**Weekly analysis of economic statecraft through the lens of game theory.**")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("Latest Analysis")
        # Loop through the blog_posts list and create a card for each
        for post in blog_posts:
            st.markdown(f"""
            <div class="post-card">
                <small style="color: #7F8C8D; font-weight: bold;">{post['tag'].upper()} | {post['date']}</small>
                <h3 style="margin-top: 5px;">{post['title']}</h3>
                <p>{post['summary']}</p>
                <a href="{post['link']}" target="_blank" style="text-decoration: none; color: #D35400; font-weight: bold;">Read Full Briefing →</a>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive Button to load simulation for this specific post
            if st.button(f"Load Simulation: {post['title']}", key=post['title']):
                st.session_state['active_scarcity'] = post['scarcity_setting']
                st.rerun()

    with col2:
        st.subheader("Live Simulation")
        # Default scarcity if none selected
        if 'active_scarcity' not in st.session_state:
            st.session_state['active_scarcity'] = 25
            
        current_scarcity = st.slider("Resource Scarcity Index", 0, 100, st.session_state['active_scarcity'])
        
        st.write(f"Visualizing a world with **{current_scarcity}% resource failure**.")
        st.pyplot(draw_map(current_scarcity))
        
        st.markdown("""
        **Legend:**
        * 🟡 **Wheat:** Food Security
        * 🔴 **Brick:** Infrastructure
        * ⚫ **Black:** Economic Collapse zone
        """)

# ==========================================
# PAGE 2: MISSION
# ==========================================
elif page == "Mission & About":
    st.title("Mission Profile")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa", caption="The Global Board")
    
    st.markdown("""
    ### Why 'HexPolitic'?
    Real-world geopolitics is often too complex to visualize. By reducing nations to 
    **resource nodes** and **trade routes** (similar to the board game Catan), we can 
    better understand the levers of power.
    
    ### About Me
    I am an analyst bridging the gap between economic theory and strategic gaming.
    Every week, I take a headline event and model it here.
    """)

# ==========================================
# PAGE 3: CONSULTANT AI
# ==========================================
elif page == "Consultant AI":
    st.title("🤖 Strategy Consultant")
    st.markdown("Ask questions about the current geopolitical board state.")
    
    # Simple Chat UI
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "I am ready. Ask me about resource constraints or trade routes."}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Placeholder AI response
        response = "This requires analyzing the Ore distribution. In a 65% scarcity scenario, tech manufacturing halts."
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)