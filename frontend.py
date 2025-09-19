import streamlit as st
import main  # Import backend process_ticket()

# Page config
st.set_page_config(page_title="Smart Ticket Classifier", page_icon="🎫", layout="wide")

# Header
st.markdown('<h1 style="text-align:center; color:#1f77b4;">🎫 Smart Ticket Classifier</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("""
    AI-powered tool to classify support tickets and suggest responses.
    Categories:
    - 🔐 Password Reset
    - 🔑 Login Problems
    - 👥 HR Queries
    - ❓ Other
    """)

# Input
ticket_text = st.text_area("📝 Enter your support ticket:", height=100)

if st.button("🚀 Process Ticket"):
    if ticket_text.strip():
        with st.spinner("Analyzing..."):
            category, response = main.process_ticket(ticket_text)
            st.session_state.category, st.session_state.response, st.session_state.ticket_text = category, response, ticket_text
    else:
        st.warning("⚠️ Please enter a ticket first.")

# Results
if "category" in st.session_state:
    st.markdown("---")
    st.subheader("📋 Results")
    emoji = {"password_reset": "🔐", "login_problem": "🔑", "hr_query": "👥", "unknown": "❓"}
    st.markdown(f"**Ticket:** {st.session_state.ticket_text}")
    st.markdown(f"**Category:** {emoji.get(st.session_state.category, '❓')} {st.session_state.category.replace('_',' ').title()}")
    st.markdown("**Response:**")
    st.success(st.session_state.response)
