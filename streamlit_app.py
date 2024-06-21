import streamlit as st

from src.advertising_budget_pacing import run_simulation


st.title("Pacing Control Lab")
st.subheader("Master the art of smooth campaign delivery! This simulator allows you to explore different pacing control algorithms, maximizing reach and inventory utilization for your advertising platform.")

# Add a number input for budget
col1, col2, col3 = st.columns(3)
with col1:
    budget_1 = st.number_input("Set campaign budget 1", min_value=1000, max_value=10000, value=3000, step=500)
with col2:
    budget_2 = st.number_input("Set campaign budget 2", min_value=1000, max_value=10000, value=4000, step=500)
with col3:
    budget_3 = st.number_input("Set campaign budget 3", min_value=1000, max_value=10000, value=6000, step=500)

budgets = [budget_1, budget_2, budget_3]


# Dropdown for the bidding strategy
bidding_strategy = st.selectbox("Choose a pacing strategy", ["Performance", "Proportional", "PID"])

# Display PID parameters if PID is selected
if bidding_strategy == "PID":
    st.subheader("PID Parameters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        kp = st.number_input("Kp (Proportional gain)", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    
    with col2:
        ki = st.number_input("Ki (Integral gain)", min_value=0.0, max_value=10.0, value=0.1, step=0.01)
    
    with col3:
        kd = st.number_input("Kd (Derivative gain)", min_value=0.0, max_value=10.0, value=0.01, step=0.1)
    
    pid_params = {'kp': kp, 'ki': ki, 'kd': kd}
else:
    pid_params = None

if st.button("🚀  Run simulation"):
    with st.spinner('Simulation is running...'):
        fig, results_df, pacing_error, inventory_fill_rate, average_cost_per_click = run_simulation(budgets=budgets, controller_type=bidding_strategy, pid_params=pid_params)
    # Use st.columns to display metrics in the same row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Inventory Fill Rate", value=f"{inventory_fill_rate:.2%}")

    with col2:
        st.metric(label="Average Cost Per Click", value=f"${average_cost_per_click:,.2f}")

    with col3:
        st.metric(label="Global Pacing Error", value=f"{pacing_error:.2%}")
    
    
    st.pyplot(fig)
    st.write(results_df)
    