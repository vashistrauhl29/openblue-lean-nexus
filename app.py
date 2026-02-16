import streamlit as st
from tabs.digital_twin import render_digital_twin
from tabs.rca_copilot import render_rca_copilot
from tabs.strategy import render_strategy

# Configure the Streamlit page
st.set_page_config(
    page_title="OpenBlu Lean Nexus",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom JCI Branding CSS
st.markdown("""
<style>
/* JCI Navy Blue Headers */
h1, h2, h3 {
    color: #003057; 
}
/* Green Accent for Metrics */
div[data-testid="stMetricValue"] {
    color: #00A651;
}
/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'current_vibration' not in st.session_state:
    st.session_state['current_vibration'] = 0.05
if 'carbon_waste' not in st.session_state:
    st.session_state['carbon_waste'] = 0.0

# Sidebar Navigation
st.sidebar.title("Navigation")
st.sidebar.checkbox("Connect to OpenBlu Bridge (Live)", value=False, disabled=True, help="Simulated Mode Active")

if st.sidebar.button("🔄 Reset Simulation Scenario"):
    st.session_state['current_vibration'] = 0.05
    st.session_state['carbon_waste'] = 0.0
    st.rerun()

selection = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "1. Strategy Deployment (Hoshin)",
        "2. Operational Digital Twin",
        "3. RCA Copilot & Sustainment"
    ]
)

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.info("Prototype for Johnson Controls | Built by Rahul Vashisht")

# Main Content Area
if selection == "Home":
    st.title("Welcome to OpenBlu Lean Nexus")
    st.markdown("""
    ### Bridging the Gap: Net Zero Strategy to Shop Floor Execution
    
    OpenBlu Lean Nexus is designed to be the digital bridge within Johnson Controls, 
    aligning high-level **Net Zero** strategic goals with daily **Shop Floor** operational reality.
    
    This tool integrates lean principles with advanced digital insights to:
    *   **Visualize Strategy:** Deploy Hoshin Kanri goals across the organization.
    *   **Digital Twin Integration:** Monitor real-time operational performance.
    *   **Sustainment:** Utilize RCA (Root Cause Analysis) tools to ensure long-term efficiency and sustainability.
    """)
elif selection == "1. Strategy Deployment (Hoshin)":
    render_strategy()
elif selection == "2. Operational Digital Twin":
    render_digital_twin()
elif selection == "3. RCA Copilot & Sustainment":
    render_rca_copilot()
else:
    st.title(selection)
    st.write("Module Under Construction")
