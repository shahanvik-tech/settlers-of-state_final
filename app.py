import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import random
import time

# --- 1. APP CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(
    page_title="HexPolitic | Global Strategy",
    page_icon="⬢",
    layout="wide",
    initial_sidebar_state="collapsed" # Collapsed by default for a cleaner "Apple" entry
)

# --- 2. APPLE-STYLE CSS SYSTEM ---
st.markdown("""
    <style>
    /* IMPORT APPLE SYSTEM FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    /* GLOBAL RESET */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1d1d1f; 
        background-color: #f5f5f7; /* Apple's Light Gray Background */
    }

    /* REMOVE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* CUSTOM CARDS (Apple Style) */
    .apple-card {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .apple-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }

    /* TYPOGRAPHY */
    h1 {
        font-weight: 700;
        letter-spacing: -0.02em;
        font-size: 42px;
    }
    h3 {
        font-weight: 600;
        font-size: 20px;
        margin-bottom: 8px;
    }
    .subtitle {
        color: #86868b;
        font-size: 18px;
        font-weight: 400;
        line-height: 1.4;
    }
    
    /* BUTTON STYLING */
    .stButton>button {
        background-color: #0071e3; /* Apple Blue */
        color: white;
        border-radius: 980px; /* Pill shape */
        padding: 8px 20px;
        font-weight: 500;
        border: none;
        box-shadow: none;
    }
    .stButton>button:hover {
        background-color: #0077ED;
    }

    /* SIDEBAR POLISH */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e5e5;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HIGH-END SIMULATION VISUALIZER ---
def draw_aesthetic_map(scarcity_level):
    """Generates a gallery-quality Hex map."""
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_alpha(0) # Transparent background
    ax.set_aspect('equal')
    
    # Grid Logic
    coord = []
    for x in range(-3, 4):
        for y in range(-3, 4):
            if abs(x + y) <= 3:
                coord.append((x, y))

    # Palette: Muted, Professional Tones
    palette = {
        'Wheat': '#E6C229',   # Muted Gold
        'Ore': '#95A5A6',     # Slate Grey
        'Brick': '#D35400',   # Burnt Orange
        'Wood': '#27AE60',    # Forest Green
        'Sheep': '#ECF0F1',   # Cloud White
        'Void': '#2c3e50'     # Dark Blue-Black (Scarcity)
    }
    resources = ['Wheat', 'Ore', 'Brick', 'Wood', 'Sheep']

    # Stats Tracker
    stats = {'Wheat': 0, 'Ore': 0, 'Brick': 0, 'Wood': 0, 'Sheep': 0, 'Void': 0}

    for x, y in coord:
        shift_x = x * np.sqrt(3) + y * np.sqrt(3)/2
        shift_y = y * 1.5
        
        # Scarcity Logic
        if random.random() < (scarcity_level / 100):
            res_type = 'Void'
            face_col = palette['Void']
            alpha_val = 0.9
        else:
            res_type = random.choice(resources)
            face_col = palette[res_type]
            alpha_val = 1.0
        
        stats[res_type] += 1
        
        # Draw Hex
        hex_patch = RegularPolygon(
            (shift_x, shift_y), 
            numVertices=6, 
            radius=1, 
            orientation=np.radians(30), 
            facecolor=face_col, 
            edgecolor='white',
            linewidth=1.5,
            alpha=alpha_val
        )
        ax.add_patch(hex_patch)

    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-5.5, 5.5)
    ax.axis('off')
    return fig, stats

# --- 4. CONTENT STORE ---
if 'simulation_data' not in st.session_state:
    st.session_state['simulation_data'] = {'scarcity': 15, 'stats': {}}

posts = [
    {
        "title": "The Silicon Curtain",
        "date": "Jan 02",
        "category": "Technology",
        "read_time": "4 min read",
        "desc": "How export controls on 'Ore' (Semiconductors) are redrawing the map of the Pacific.",
        "scarcity": 65
    },
    {
        "title": "Grain & Fire",
        "date": "Dec 28",
        "category": "Agriculture",
        "read_time": "6 min read",
        "desc": "Analyzing the failure of the breadbasket hexes and the resulting migration patterns.",
        "scarcity": 30
    }
]

# --- 5. UI LAYOUT ---

# SIDEBAR (Navigation)
with st.sidebar:
    st.title("⬢ HexPolitic")
    st.caption("Intelligence Unit")
    st.markdown("---")
    nav = st.radio("Menu", ["Briefing Room", "Simulation Deck", "About", "Consultant AI"])
    st.markdown("---")
    st.caption("© 2026 HexPolitic Inc.")

# PAGE: BRIEFING ROOM (HOME)
if nav == "Briefing Room":
    # HERO SECTION
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 56px; margin-bottom: 10px;">The Geopolitics of Now.</h1>
        <p class="subtitle" style="max-width: 600px; margin: 0 auto;">
            We model global conflict using hexagonal game theory. 
            Simple rules. Complex outcomes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # TWO COLUMN LAYOUT
    col_content, col_sim = st.columns([1.5, 1], gap="large")

    with col_content:
        st.subheader("Latest Intelligence")
        for post in posts:
            # Custom HTML Card
            st.markdown(f"""
            <div class="apple-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="font-size:12px; font-weight:700; color:#0071e3; text-transform:uppercase;">{post['category']}</span>
                    <span style="font-size:12px; color:#86868b;">{post['date']} • {post['read_time']}</span>
                </div>
                <h3>{post['title']}</h3>
                <p style="color:#515154; font-size:15px; line-height:1.5;">{post['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Load Simulation: {post['title']}", key=post['title']):
                st.session_state['simulation_data']['scarcity'] = post['scarcity']
                st.toast(f"Simulation loaded: {post['title']}", icon="✅")

    with col_sim:
        st.subheader("Live Model")
        # Control Panel within a Card
        with st.container():
            st.markdown('<div class="apple-card">', unsafe_allow_html=True)
            scarcity = st.slider("Global Stress Index", 0, 100, st.session_state['simulation_data']['scarcity'])
            
            # Draw Map
            fig, stats = draw_aesthetic_map(scarcity)
            st.pyplot(fig)
            
            # Data Metrics (Apple Style)
            c1, c2, c3 = st.columns(3)
            c1.metric("GDP", f"${100-scarcity}T", delta=f"-{scarcity}%" if scarcity > 0 else "0%")
            c2.metric("Stability", f"{max(0, 100-(scarcity*1.5)):.0f}/100")
            c3.metric("Failed Nodes", f"{stats['Void']}")
            st.markdown('</div>', unsafe_allow_html=True)

# PAGE: SIMULATION DECK (Deep Dive)
elif nav == "Simulation Deck":
    st.title("The War Room")
    st.markdown("Run custom scenarios to stress-test economic resilience.")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.markdown("#### Configuration")
        st.selectbox("Region", ["Eurasia", "Pacific", "Atlantic"])
        st.select_slider("Aggression Level", ["Diplomatic", "Trade War", "Kinetic"])
        val = st.slider("Resource Scarcity", 0, 100, 50)
        st.button("Run Model", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # Big Map
        fig, _ = draw_aesthetic_map(val)
        st.pyplot(fig)

# PAGE: ABOUT
elif nav == "About":
    st.title("Mission Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070", use_column_width=True)
    with col2:
        st.markdown("""
        ### Why Hexagons?
        Because the world isn't a list of numbers. It's a network of neighbors.
        
        HexPolitic was built to bridge the gap between **Geopolitical Theory** and **System Dynamics**. 
        We use the 'Settlers' mechanic to demonstrate how fragile supply chains truly are.
        
        **Follow the work:**
        """)
        st.markdown("[X (Twitter)](https://twitter.com) • [Substack](https://substack.com)")

# PAGE: AI CONSULTANT
elif nav == "Consultant AI":
    st.title("Consultant AI")
    st.caption("Powered by your historical analysis data.")
    
    # Chat UI Container
    chat_container = st.container()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-end; margin-bottom:10px;">
                    <div style="background-color:#0071e3; color:white; padding:10px 15px; border-radius:18px 18px 4px 18px; max-width:70%;">
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-start; margin-bottom:10px;">
                    <div style="background-color:#E5E5EA; color:black; padding:10px 15px; border-radius:18px 18px 18px 4px; max-width:70%;">
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Input Area
    prompt = st.chat_input("Ask a strategic question...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Dummy Response Logic
        response = "Based on the 'Silicon Curtain' scenario, restricting Ore exports leads to a 40% drop in Blue player stability."
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
