import streamlit as st

from src.advertising_budget_pacing import run_simulation


st.title("Real time bidding simulation")


# Add a number input for budget
budget_1 = st.number_input("Campaign Budget 1", min_value=2000, max_value=10000, value=2000, step=500)
budget_2 = st.number_input("Campaing Budget 2", min_value=2000, max_value=10000, value=4000, step=500)
budget_3 = st.number_input("Campaign Budget 3", min_value=2000, max_value=10000, value=6000, step=500)

budgets = [budget_1, budget_2, budget_3]


# Dropdown for the bidding strategy
bidding_strategy = st.selectbox("Choose a pacing strategy", ["Performance", "Proportional", "PID"])

# Display PID parameters if PID is selected
if bidding_strategy == "PID":
    st.subheader("PID Parameters")
    kp = st.number_input("Kp (Proportional gain)", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    ki = st.number_input("Ki (Integral gain)", min_value=0.0, max_value=10.0, value=0.1, step=0.01)
    kd = st.number_input("Kd (Derivative gain)", min_value=0.0, max_value=10.0, value=0.01, step=0.01)
    # Pass PID parameters to the simulation function
    pid_params = {'kp': kp, 'ki': ki, 'kd': kd}
else:
    pid_params = None

if st.button("🚀  Run simulation"):
    fig, results_df, pacing_error = run_simulation(budgets=budgets, controller_type=bidding_strategy, pid_params=pid_params)
    # Use st.columns to display metrics in the same row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Spend", value=f"${100:,.2f}")

    with col2:
        st.metric(label="Average Spend", value=f"${100:,.2f}")

    with col3:
        st.metric(label="Global Pacing Error", value=f"{pacing_error:.2%}")
    
    
    st.pyplot(fig)
    st.write(results_df)
    