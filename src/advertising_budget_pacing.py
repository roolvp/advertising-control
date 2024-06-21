import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.PID_controller import PIDController
from src.proportional_controller import ProportionalController
from src.budget_based_controller import BudgetOnlyController


class Campaign:
    def __init__(self, name: str, pCTR: float, bid: float, budget: int):
        self.name = name
        self.pCTR = pCTR
        self.bid = bid
        self.budget = budget
        self.spend = 0
        self.pacing_errors = []
        self.controller: PIDController = PIDController(0.001, 0.008, 0.9)
    

def run_simulation(budgets: list[int] = [5000, 1000, 4000], controller_type: str = "Performance", pid_params: dict = None):
       
    data = {
        # Each item is a book that represents a campaign
        'Item': ['Time Series Analysis: Forecasting and Control', 'Practical Statistics for Data Scientists', 'Designing Data-Intensive Applications'],
        # Probability of click through rate (This is a guess as we don't have the actual data)
        'pCTR': [0.03, 0.04, 0.02],
        # Bid amount (this will be randomized around this central amount)
        'Bid': [0.5, 0.48, 0.55],
        'Budget': budgets,
    }
    
    # Create Campaign objects in a dictionary
    campaigns = {}
    if controller_type == "PID":
        for i in range(len(data['Item'])):
            campaigns[data['Item'][i]] = Campaign(data['Item'][i], data['pCTR'][i], data['Bid'][i], data['Budget'][i])
            campaigns[data['Item'][i]].controller = PIDController(pid_params['kp'], pid_params['ki'], pid_params['kd'])
    elif controller_type == "Proportional":
        for i in range(len(data['Item'])):
            campaigns[data['Item'][i]] = Campaign(data['Item'][i], data['pCTR'][i], data['Bid'][i], data['Budget'][i])
            campaigns[data['Item'][i]].controller = ProportionalController()
    elif controller_type == "Performance":
        for i in range(len(data['Item'])):
            campaigns[data['Item'][i]] = Campaign(data['Item'][i], data['pCTR'][i], data['Bid'][i], data['Budget'][i])
            campaigns[data['Item'][i]].controller = BudgetOnlyController()
        
        

    # Create DataFrame
    items_keywords_df = pd.DataFrame(data)




    # %%
    def auction(df):
        """
        Gets df with bidding information and simulates an auction
        
        Returns winner's item name and price paid
        
        """
        bid_dict = {}
        for index, id in df.iterrows():
            bid_dict[index] = id['Bid'] - np.random.uniform(0.0, 0.2)
        winner_index = max(bid_dict, key=bid_dict.get)
        winner = df.loc[winner_index]['Item']
        try:
            # price paid is the bid of the second highest bidder
            price_paid = sorted(bid_dict.values(), reverse=True)[1]
        except:
            # If there is only one bidder, the price paid is the bid of the winner
            price_paid = bid_dict[winner_index]
        return winner, price_paid

    winner, price_paid = auction(items_keywords_df)


    def calc_clicks(pCTR, total_impressions = 1000):
        return total_impressions * pCTR

    def calc_total_spend(clicks, price_paid):
        return clicks * price_paid


    simulation_results = []
    simulation_results.append({
                'Minute': 0,
                'Winner': 'Time Series Analysis: Forecasting and Control',
                'Price Paid': 0,
                "pCTR": 0,
                "Spend": 0,
            })
    simulation_results_df = pd.DataFrame(simulation_results)
    for minute in range(1440):
        
        selection_df = items_keywords_df.copy()
        
        for campaign in campaigns:
            
            if controller_type == "PID":
                target_rate = campaigns[campaign].budget * minute / 1440
                actual_rate = campaigns[campaign].spend 

            elif controller_type in ["Proportional", "Performance"]:
                target_rate = campaigns[campaign].budget
                actual_rate = campaigns[campaign].spend
            
            bid = campaigns[campaign].controller.update(target_rate=target_rate, actual_rate=actual_rate, dt=1)
        
            selection_df.loc[selection_df['Item'] == campaign, 'Enter_bid'] = bid
            
            # Pacing error calculations
            budget_spent = campaigns[campaign].spend
            budget_target = campaigns[campaign].budget * minute / 1440
            
            if budget_target == 0:
                campaigns[campaign].pacing_errors.append(0)
            else:
                campaigns[campaign].pacing_errors.append(abs(budget_spent - budget_target)/budget_target)
        
        selection_df = selection_df[selection_df['Enter_bid'] == 1]
          
        
        # If there are no bidders, skip the minute and save as "No Bid" 
        
        if selection_df.shape[0] == 0:
            print("# No Bidder")
            simulation_results.append({
                'Minute': minute,
                'Winner': 'No Bid',
                'Price Paid': 0,
                "pCTR": 0,
                "Spend": 0,
            })
                
        else:    
            print("# Bidding")
            winner_item, price_paid = auction(selection_df)
            winner_index = items_keywords_df[items_keywords_df['Item'] == winner_item].index[0]
            pctr = items_keywords_df.loc[winner_index]['pCTR'] + np.random.normal(-0.001, 0.01)
            result = {
                'Minute': minute,
                'Winner': items_keywords_df.loc[winner_index]['Item'],
                'Price Paid': price_paid,
                "pCTR": pctr,
                "Spend": price_paid * pctr * 1000
            }
            
            # Update Spend so far for the winner update the object
            campaigns[winner_item].spend += result['Spend']
            

                        
            
            simulation_results.append(result)
        simulation_results_df = pd.DataFrame(simulation_results)


    simulation_results_df['Clicks'] = simulation_results_df.apply(lambda x: calc_clicks(total_impressions=1000, pCTR=x['pCTR']), axis=1)
    simulation_results_df['Total Spend'] = simulation_results_df.apply(lambda x: calc_total_spend(x['Clicks'], x['Price Paid']), axis=1)


    simulation_results_df.groupby("Winner").agg({"Price Paid": "mean", "pCTR": "mean", "Minute": "count", "Clicks": "sum", "Total Spend": "sum"})

    # add cost per click
    simulation_results_df['Cost Per Click'] = simulation_results_df['Total Spend'] / simulation_results_df['Clicks']
    average_cost_per_click = simulation_results_df['Cost Per Click'].mean()

    print_df = simulation_results_df.groupby("Winner").agg({"Price Paid": "mean", "pCTR": "mean", "Minute": "count", "Clicks": "sum", "Total Spend": "sum", "Cost Per Click": "mean"})

    # Inventory not sold (Count in simulation_results_df the number of rows with "No Bid" in the "Winner" column)
    inventory_not_sold = simulation_results_df[simulation_results_df['Winner'] == 'No Bid'].shape[0]
    inventory_fill_rate = 1 - inventory_not_sold / 1440
    
    

    timeseries = []

    for item in items_keywords_df['Item']:
        for  minute in range(1440):
            budget = items_keywords_df[items_keywords_df['Item'] == item]['Budget'].values[0]
            timeseries_row = {
                'Minute': minute,
                'Item': item,
                'cumulative_expected_spend_linear': minute * budget / 1440,
            }
            timeseries.append(timeseries_row)
        
    campaign_timeseries_df = pd.DataFrame(timeseries)

    # print the spend for each campaing object
    for campaign in campaigns:
        print(f"{campaign}: {campaigns[campaign].spend}")
    
    # Calculate the global pacing error
    pacing_errors = []
    for campaign in campaigns:
        pacing_errors += campaigns[campaign].pacing_errors
    pacing_error = np.mean(pacing_errors)
    print(f"Global pacing error: {pacing_error}")


    fig, axs = plt.subplots(3, figsize=(10, 18))  # Create 3 subplots

    items = items_keywords_df['Item'].unique()  # Get unique items

    for i in range(3):  # Loop over each subplot
        item = items[i]  # Get the item for this subplot
        axs[i].plot(campaign_timeseries_df[campaign_timeseries_df['Item'] == item]['Minute'], campaign_timeseries_df[campaign_timeseries_df['Item'] == item]['cumulative_expected_spend_linear'], label=item)
        axs[i].plot(simulation_results_df[simulation_results_df['Winner'] == item]['Minute'], 
                    simulation_results_df[simulation_results_df['Winner'] == item]['Total Spend'].cumsum(), 
                    label=f"{item} Actual")
        axs[i].legend()  # Add a legend to the subplot
        axs[i].set_ylabel("Cumulative Spend ($)")
        axs[i].set_xlabel("Time of Day (minutes)")

    return fig, print_df, pacing_error, inventory_fill_rate, average_cost_per_click

    # %%



