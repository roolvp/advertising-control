import streamlit as st

from src.advertising_budget_pacing import run_simulation

markdown_text = """
## Welcome to the Pacing Control Lab!

**The Scenario**

Imagine three of your data science books are competing for the same ad space on search results for the keyword "data science book." These books are:

1.  **Campaign 1:** "Time Series Analysis: Forecasting and Control"
2.  **Campaign 2:** "Practical Statistics for Data Scientists"
3.  **Campaign 3:** "Designing Data-Intensive Applications"

Each book has a different budget, click-through rate, and bid amount. The goal is to spend the budget wisely throughout the day, ensuring your ads reach the right audience without overspending or underspending.

**Your Pacing Toolkit**

You can choose from three different pacing algorithms to control how your ad spend is distributed over time:

*   **PID Controller (Proportional-Integral-Derivative):** This advanced algorithm continuously adjusts your bid based on how far off you are from your spending target (proportional), the accumulated error over time (integral), and how quickly the error is changing (derivative). It's like a supercharged cruise control for your ad spend! You can tune its responsiveness with the Kp, Ki, and Kd parameters.

*   **Proportional Controller:** This simpler algorithm adjusts your bid proportionally to how far off you are from your spending target. It's a good option if you want a straightforward, responsive controller.

*   **Budget Only Controller (Performance-Based):** This basic algorithm doesn't adjust your bid directly. Instead, it focuses on spending your budget evenly throughout the day. 

**Let's Experiment!**

1.  **Set Your Budgets:**  Decide how much you want to spend on each book campaign.
2.  **Choose an Algorithm:** Select the pacing algorithm you'd like to test.
3.  **Tune Your Parameters (if applicable):** If you chose the PID controller, you can fine-tune the Kp, Ki, and Kd values.
4.  **Run the Simulation:** Click the "Run Simulation" button to see how your chosen algorithm performs!

**Analyze the Results**

The simulator provides detailed results, including:

*   **Inventory Fill Rate:** The percentage of available ad impressions you captured.
*   **Average Cost Per Click:** The average amount you paid for each click on your ads.
*   **Global Pacing Error:**  A measure of how well the algorithm kept your spending on track.
*   **Time Series Graphs:** Visualizations of planned vs. actual spending for each book.

Feel free to experiment with different combinations of budgets, algorithms, and parameters to find the optimal pacing strategy for your campaigns! 

Let me know if you'd like more details on any of these features! 
"""

st.title("Pacing Control Lab")
st.subheader("Master the art of smooth campaign delivery! This simulator allows you to explore different pacing control algorithms, maximizing reach and inventory utilization for your advertising platform.")
with st.expander("Full Explanation", expanded=False):
    st.markdown(markdown_text)
# Add a number input for budget
col1, col2, col3 = st.columns(3)
with col1:
    budget_1 = st.number_input("Campaign 1 budget ($)", min_value=1000, max_value=10000, value=3000, step=500)
with col2:
    budget_2 = st.number_input("Campaign 2 budget ($)", min_value=1000, max_value=10000, value=4000, step=500)
with col3:
    budget_3 = st.number_input("Campaign 3 budget ($)", min_value=1000, max_value=10000, value=6000, step=500)

budgets = [budget_1, budget_2, budget_3]


# Dropdown for the bidding strategy
bidding_strategy = st.selectbox("Choose a pacing strategy", ["Performance", "Proportional", "PID"])

# Display PID parameters if PID is selected
if bidding_strategy == "PID":
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
    
with st.sidebar:
    st.markdown("---")
    st.markdown("**Made by [@roolvp](https://github.com/roolvp)**")  # Replace with your username
    st.markdown("[LinkedIn](https://www.linkedin.com/in/raulvences/)")
    st.markdown("[raul.ven.par@gmail.com](mailto:raul.ven.par@gmail.com)")