import streamlit as st

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("📊 Nifty 100 Analytics")

st.sidebar.success("Select a page from the sidebar.")

# --------------------------------------------------
# Main Page
# --------------------------------------------------
st.title("📈 Nifty 100 Financial Intelligence Platform")

st.markdown(
    """
    Welcome to the **Nifty 100 Financial Intelligence Dashboard**.

    Use the **sidebar** to navigate between dashboard pages.

    ### Available Modules

    - 🏠 Home
    - 🏢 Company Profile
    - 🔍 Screener
    - 🤝 Peer Comparison
    - 📈 Trend Analysis
    - 🏭 Sector Analysis
    - 🌳 Capital Allocation
    - 📄 Annual Reports
    """
)

st.info("Dashboard scaffold created successfully. 🚀")