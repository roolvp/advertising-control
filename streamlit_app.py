import streamlit as st

from advertising_budget_pacing import run_simulation


st.title("Real time bidding simulation")

if st.button("Run simulation"):
    fig = run_simulation()
    st.pyplot(fig)