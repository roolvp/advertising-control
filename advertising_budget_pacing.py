import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def run_simulation(budgets: list[int] = [5000, 3000, 2000]):
    data = {
        # Each item is a book that represents a campaign
        'Item': ['Time Series Analysis: Forecasting and Control', 'Practical Statistics for Data Scientists', 'Designing Data-Intensive Applications'],
        # They are all bidding on the same keyword
        'Keyword': ['statistics book', 'statistics book', 'statistics book'],
        # Probability of click through rate (This is a guess as we don't have the actual data)
        'pCTR': [0.03, 0.04, 0.02],
        # Bid amount (this will be randomized around this central amount)
        'Bid': [0.5, 0.48, 0.55],
        'Budget': budgets,
    }

    # Create DataFrame
    items_keywords_df = pd.DataFrame(data)


    def auction(df):
        """
        Gets df with bidding information and simulates an auction
        
        Returns winner and price paid
        
        """
        bid_dict = {}
        for index, id in df.iterrows():
            bid_dict[index] = id['Bid']- np.random.uniform(0.0, 0.2)
        winner = max(bid_dict, key=bid_dict.get)
        try:
            # price paid is the bid of the second highest bidder
            price_paid = sorted(bid_dict.values(), reverse=True)[1]
        except:
            # If there is only one bidder, the price paid is the bid of the winner
            price_paid = bid_dict[winner]
        return winner, price_paid

    winner, price_paid = auction(items_keywords_df)
    print(winner)
    print(f"The winner is {items_keywords_df.loc[winner]['Item']}")
    print(f"The price paid is {price_paid}")

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
    print(f"The winner is {winner}")
    print(f"The price paid is {price_paid}")

    # %%
    test_df = items_keywords_df.copy()

    def decide_budget_proportional_choice(Budget, Spend) -> int:
        """
        Choose a to enter a bid based on the proportion of budget spent
        """
        p = (Budget - Spend) / Budget
        #ensure p is between 0 and 1
        p = max(0, min(1, p))
        return np.random.choice([0, 1], p=[1-p, p])


    def calc_clicks(pCTR, total_impressions = 1000):
        return total_impressions * pCTR

    def calc_total_spend(clicks, price_paid):
        return clicks * price_paid

    # %%
    # Simulate unlimited budget over 1440 minutes
    # iterate over 1440 minutes (flat traffic)
    # Save the winner and price paid
    # Build a dataframe with the results

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
        # Remove winner if Spend is greater than Budget
        #items_keywords_df = items_keywords_df[items_keywords_df['Spend'] < items_keywords_df['Budget']]
        
        # Choose who enters the bid (% to budget strategy)
        
        selection_df = items_keywords_df.copy()
        # Update selection_df with Spend so far from dataframe simulation_results_df.groupby('Winner')['Spend'].sum()
        selection_df = pd.merge(selection_df, simulation_results_df.groupby('Winner')['Spend'].sum(), left_on='Item', right_on='Winner', how='left')
        selection_df['Enter_bid'] = selection_df.apply(lambda x: decide_budget_proportional_choice(x['Budget'], x['Spend']), axis=1)
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
            
            # Update Spend so far for the winner
            #items_keywords_df.loc[winner_index, 'Spend'] = items_keywords_df.loc[winner_index, 'Spend'] + result['Spend']
            
            # print winner and Spend
            print(f"Minute {minute}: {result['Winner']} wins with a bid of {price_paid}. Spend so far: {selection_df.loc[winner_index, 'Spend']}")
            
            
            simulation_results.append(result)
        simulation_results_df = pd.DataFrame(simulation_results)
        #print cumulative summ of spend per winner
        print(simulation_results_df.groupby('Winner')['Spend'].sum())



    # %%
    simulation_results_df.groupby("Winner").agg({"Price Paid": "mean", "pCTR": "mean", "Minute": "count"})
    simulation_results_df['Clicks'] = simulation_results_df.apply(lambda x: calc_clicks(total_impressions=1000, pCTR=x['pCTR']), axis=1)
    simulation_results_df['Total Spend'] = simulation_results_df.apply(lambda x: calc_total_spend(x['Clicks'], x['Price Paid']), axis=1)


    simulation_results_df.groupby("Winner").agg({"Price Paid": "mean", "pCTR": "mean", "Minute": "count", "Clicks": "sum", "Total Spend": "sum"})

    # add cost per click
    simulation_results_df['Cost Per Click'] = simulation_results_df['Total Spend'] / simulation_results_df['Clicks']

    print_df = simulation_results_df.groupby("Winner").agg({"Price Paid": "mean", "pCTR": "mean", "Minute": "count", "Clicks": "sum", "Total Spend": "sum", "Cost Per Click": "mean"})




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




    fig, axs = plt.subplots(3, figsize=(10, 18))  # Create 3 subplots

    items = items_keywords_df['Item'].unique()  # Get unique items

    for i in range(3):  # Loop over each subplot
        item = items[i]  # Get the item for this subplot
        axs[i].plot(campaign_timeseries_df[campaign_timeseries_df['Item'] == item]['Minute'], campaign_timeseries_df[campaign_timeseries_df['Item'] == item]['cumulative_expected_spend_linear'], label=item)
        axs[i].plot(simulation_results_df[simulation_results_df['Winner'] == item]['Minute'], 
                    simulation_results_df[simulation_results_df['Winner'] == item]['Total Spend'].cumsum(), 
                    label=f"{item} Actual")
        axs[i].legend()  # Add a legend to the subplot

    return fig, print_df 

    # %%



