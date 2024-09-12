import numpy as np
import pandas as pd
import os
import sys
from datetime import datetime
import multiprocessing as mp
from copy import deepcopy

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')  # Adjust this to point to the correct folder
sys.path.append(project_root)
from model.VotingModel import VotingModel
from model.EvalMetrics import EvalMetrics
from model.VotingRules import VotingRules

# Define a function to process a single round of bribery evaluation
def process_bribery_round(model, desired_increase_percentage, round_num):
    model_copy = deepcopy(model)  # Independent copy of the model to avoid state sharing
    eval_metrics_copy = EvalMetrics(model_copy)  # Independent EvalMetrics instance
    
    # Simulate the bribery for the current round
    model_copy.step()  # Advance the simulation for this round
    bribery_results_df = eval_metrics_copy.evaluate_bribery(1, desired_increase_percentage)  # Evaluate for one round
    
    # Add round number for tracking
    bribery_results_df['round'] = round_num
    return bribery_results_df

# Function to run bribery evaluation across rounds in parallel
def run_parallel_bribery_evaluation(model, num_rounds, desired_increase_percentage, num_workers=4):
    with mp.Pool(processes=num_workers) as pool:
        # Parallelize the round execution using pool.starmap
        results = pool.starmap(process_bribery_round, [(deepcopy(model), desired_increase_percentage, round_num) for round_num in range(1, num_rounds + 1)])

    # Combine all results into a single DataFrame
    combined_results = pd.concat(results, ignore_index=True)
    return combined_results

# Main execution
if __name__ == '__main__':
    # Initialize simulation parameters
    num_voters = 144
    num_projects = 600
    total_op_tokens = 30e6
    num_rounds = 10  # Number of rounds to run
    voter_type = 'mallows_model'
    quorum = 17
    
    # Initialize the model
    model = VotingModel(voter_type=voter_type, num_voters=num_voters, num_projects=num_projects, total_op_tokens=total_op_tokens)
    
    # Initialize the evaluation metrics
    model.step()
    eval_metrics = EvalMetrics(model)

    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    output_dir = os.path.join(current_dir, '..', 'data', 'vm_data')  # Define relative path

    # Parameters for bribery evaluation
    min_increase = 1
    max_increase = 10
    iterations = 20
    desired_increase_percentages = np.linspace(min_increase, max_increase, iterations)

    # Iterate over each desired increase percentage
    bribery_results = pd.DataFrame()

    for i, desired_increase_percentage in enumerate(desired_increase_percentages, 1):
        print(f"Iteration {i}/{iterations} with desired_increase_percentage: {desired_increase_percentage}")

        # Run the parallel bribery evaluation for this desired increase percentage
        num_workers = mp.cpu_count()  # Use the available CPU cores
        bribery_results_for_percentage = run_parallel_bribery_evaluation(model, num_rounds, desired_increase_percentage, num_workers)

        # Calculate the average bribery cost for each voting rule over all rounds
        avg_bribery_costs = bribery_results_for_percentage.mean()

        # Convert the result to a DataFrame and add the desired_increase_percentage column
        avg_bribery_costs_df = avg_bribery_costs.to_frame().T
        avg_bribery_costs_df['desired_increase_percentage'] = desired_increase_percentage

        # Append the results to the final DataFrame
        bribery_results = pd.concat([bribery_results, avg_bribery_costs_df], ignore_index=True)

    # Display the results after the parallel execution
    print(bribery_results)

    # Save the results to a CSV file
    output_path = os.path.join(output_dir, f'bribery_experiment_results_{timestamp}_{num_voters}_{num_projects}_{total_op_tokens}_{num_rounds}.csv')
    bribery_results.to_csv(output_path, index=False)

    print("Bribery experiment completed")
    print(f"Results saved to {output_path}")
