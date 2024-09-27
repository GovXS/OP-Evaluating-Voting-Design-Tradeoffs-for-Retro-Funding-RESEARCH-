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
num_voters = 40
num_projects = 145
total_op_tokens = 8e6
num_rounds = 100
voter_type = 'mallows_model'
quorum=17
# Initialize the model
model = VotingModel(voter_type=voter_type, num_voters=num_voters, num_projects=num_projects, total_op_tokens=total_op_tokens)

# Initialize the evaluation metrics
model.step()
eval_metrics = EvalMetrics(model)
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current file's directory
output_dir = os.path.join(current_dir, '..', 'data', 'experiment_results', f'{num_voters}_{num_projects}_{total_op_tokens}_{num_rounds}')

    # Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

allocation_df=model.compile_fund_allocations()
allocation_df.to_csv(os.path.join(output_dir, 'allocation_df.csv'), index=False)
print("Fund Allocations for each project")
print(allocation_df.head(10))


robustness_results = eval_metrics.evaluate_robustness(num_rounds=num_rounds)
robustness_results.to_csv(os.path.join(output_dir,f'robustness_results_{num_projects}_{num_voters}_{total_op_tokens}_{num_rounds}_{timestamp}.csv'), index=False)
print("Robustness Results:")
print(robustness_results.head(100))

print("Experiment Completed")

# Save the experiment parameters to a text file
parameters = {
    "num_voters": num_voters,
    "num_projects": num_projects,
    "total_op_tokens": total_op_tokens,
    "num_rounds per iteration": num_rounds,
    "voter_type": voter_type,
    "quorum": quorum,
    "timestamp": timestamp
}

script_file_name = os.path.splitext(os.path.basename(__file__))[0]

# Set the path for the parameter file, including the script file name
param_file_path = os.path.join(output_dir, f'{script_file_name}_experiment_parameters_{timestamp}.txt')

# Write the parameters to the text file
with open(param_file_path, 'w') as f:
    for key, value in parameters.items():
        f.write(f'{key}: {value}\n')
