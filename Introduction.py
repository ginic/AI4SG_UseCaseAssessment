"""
AI4SG Use Case Assessment
Interactive assessment framework for scoping AI, ML, and data science projects for social good organizations.
"""

import streamlit as st

from utils.config import INTRO_TEXT_MARKDOWN
from utils.navigation import add_navigation_buttons
from utils.loader import initialize_questions_cache


st.set_page_config(page_title="Introduction", layout="wide")

# Initialize questions cache at application startup
initialize_questions_cache()

st.title("AI4SG Use Case Assessment")
st.markdown(body=INTRO_TEXT_MARKDOWN.read_text())

# Add navigation buttons
st.markdown("---")
add_navigation_buttons("Introduction")
