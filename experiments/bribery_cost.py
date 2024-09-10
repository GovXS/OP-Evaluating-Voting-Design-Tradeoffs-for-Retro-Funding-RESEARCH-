# Import libraries
import numpy as np
import pandas as pd
import os
import sys
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')  # Adjust this to point to the correct folder
sys.path.append(project_root)
from model.VotingModel import VotingModel
from model.EvalMetrics import EvalMetrics

# Add the directory containing the VotingModel to the Python path

from model.VotingRules import VotingRules

# Initialize simulation parameters
num_voters = 144
num_projects = 600
total_op_tokens = 30e6
num_rounds = 100
voter_type = 'mallows_model'
quorum=17
# Initialize the model
model = VotingModel(voter_type=voter_type, num_voters=num_voters, num_projects=num_projects, total_op_tokens=total_op_tokens)

# Initialize the evaluation metrics
model.step()
eval_metrics = EvalMetrics(model)
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current file's directory
output_dir = os.path.join(current_dir, '..', 'data', 'vm_data')  # Define relative path

allocation_df=model.compile_fund_allocations()
allocation_df.to_csv(os.path.join(output_dir, 'allocation_df.csv'), index=False)
print("Fund Allocations for each project")
print(allocation_df.head(10))



# %%
min_increase = 0.01
max_increase = 10
iterations = 10
counter=1

# Create a DataFrame to store the results of each iteration
bribery_results = pd.DataFrame()

# Generate 100 values of desired_increase_percentage from 0.01 to 10
desired_increase_percentages = np.linspace(min_increase, max_increase, iterations)

# Iterate through each desired_increase_percentage
for i, desired_increase_percentage in enumerate(desired_increase_percentages, 1):
    print(f"Iteration {i}/{iterations} with desired_increase_percentage: {desired_increase_percentage}")

    # Evaluate bribery costs for the current desired increase percentage
    bribery_results_df = eval_metrics.evaluate_bribery(num_rounds, desired_increase_percentage)

    # Calculate the average bribery cost for each voting rule over all rounds
    avg_bribery_costs = bribery_results_df.mean()

    # Convert the result to a DataFrame and add the desired_increase_percentage column
    avg_bribery_costs_df = avg_bribery_costs.to_frame().T
    avg_bribery_costs_df['desired_increase_percentage'] = desired_increase_percentage

    # Append the results to the DataFrame using pd.concat
    bribery_results = pd.concat([bribery_results, avg_bribery_costs_df], ignore_index=True)

# Display the results after the loop
print(bribery_results)
output_path=os.path.join(output_dir, 'bribery_experiment_results_{timestamp}_{num_voters}_{num_projects}_{total_op_tokens}_{num_rounds}.csv')

bribery_results.to_csv(output_path, index=False)


# %%
bribery_results.head(100)
print("Bribery experiment Completed")
print("Results saved to {output_path}")

