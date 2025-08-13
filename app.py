import streamlit as st
import pandas as pd  # we’ll need this later

# page settings
st.set_page_config(page_title="Lab & Notes Viewer", page_icon="🩺", layout="wide")

# title + description
st.title("🩺 Lab & Notes Viewer")
st.caption("Week 5 Day 1 — modular skeleton (no behavior change yet)")

# info box
st.info("This is the new app entry (app.py). We will move real code here over the week.")

st.markdown("---")
st.write("✅ If you can see this, your modular app skeleton runs.")
st.write("Next steps: move CSV loading to data_utils.py (Day 2).")
