"""
AI4SG Use Case Assessment
Interactive assessment framework for scoping AI, ML, and data science projects for social good organizations.
"""

import streamlit as st
from utils.navigation import add_navigation_buttons


st.set_page_config(page_title="Introduction", layout="wide")

st.title("AI4SG Use Case Assessment")
st.markdown("### Welcome to the AI for Social Good Project Assessment Tool")

st.write("""
This interactive tool will guide you through an assessment of your organization's
readiness and constraints when planning an AI or data science project.
""")

st.info("Use the sidebar to navigate through the assessment sections.")

# Add navigation buttons
st.markdown("---")
add_navigation_buttons("Introduction")
