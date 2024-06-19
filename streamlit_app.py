import streamlit as st

from advertising_budget_pacing import run_simulation


st.title("Real time bidding simulation")


# Add a number input for budget
budget_1 = st.number_input("Set the budget of your campaign", min_value=2000, max_value=10000, value=2000, step=500)
budgets = [budget_1, 3000, 2000]


# Dropdown for the bidding strategy
# bidding_strategy = st.selectbox("Choose a pacing strategy", ["Performance", "Proportional to budget", "PID controller"])

if st.button("Run simulation"):
    fig, results_df = run_simulation(budgets=budgets)
    st.pyplot(fig)
    st.write(results_df)
    