# Evaluating-Voting-Design-Tradeoffs-for-Retro-Funding
### GovXS Retro Funding Simulator - README

# Overview

The **GovXS Retro Funding Simulator** is a tool designed to simulate different voting mechanisms used in a Retro Funding context. It's part of the GovXS Voting Design Evaluation Framework that covers typical Retro Funding design goals and respective axioms and metrics to evaluate any given voting design.

![GovXS-Evaluation-Framework-V11](https://github.com/user-attachments/assets/c2f48967-fde2-4d04-ad86-dc3abd4bb586)


The simulator allows users to test various voting rules, simulate voter behavior, and evaluate key performance metrics like Cost of Control or Voter Extractable Value by applying agent-based simulations.

This simulator models both **voters** and **projects** using agents, and supports multiple voting systems such as **quadratic voting**, **mean voting**, **median voting**, and **capped voting**. The voting rules aggregate votes into a final fund allocation for projects, enabling researchers to evaluate the effects of these rules under different simulation conditions.

The simulator is implemented using the **Mesa** agent-based modeling framework, and it includes mechanisms to test for various evaluation metrics and voter behaviors, making it highly flexible and extensible.

# Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   .\venv\Scripts\activate    # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Existing Simulations**:
   - Open and run simulations in **`simulations/evaluations.ipynb`** to reproduce results.

5. **Run Existing Experiments**:
   - Navigate to the **`experiments`** folder and run predefined experiments for control, bribery, robustness, and more.

6. **Define New Experiments or Voting Rules**:
   - Add custom voting rules in **`models/VotingRules.py`**.
   - Add new evaluation metrics in **`models/EvalMetrics.py`**.
   - Run simulations or custom experiments using the simulator infrastructure.

This setup allows for both running pre-existing experiments and defining new voting rules and metrics to explore different scenarios.

# Key Components

### Models

1. **VotingModel** (`models.VotingModel`)
   - The core simulation engine for the Retro Funding Simulator. It defines the number of voters, projects, and the voting rules.
   - Allows for custom voting rules, fund allocation methods, and the computation of evaluation metrics.
   - Key features include:
     - **Voting Rules Discovery:** The simulator automatically detects all voting rule functions and can apply them to allocate funds.
     - **Voting Matrix:** Represents votes cast by each voter for each project.
     - **Run Simulation:** Steps through each simulation round, collecting results for fund allocations.
     - **Allocate Funds:** Different fund allocation methods can be tested, such as quadratic, mean, median, capped median, etc.

2. **Voting Rules** (`models.VotingRules`)
   - Contains the implementation of different voting rules, including:
     - `r1_quadratic`: R1 Quadratic Voting, where the square root of the votes is used to determine allocation. We replicate the [Optimism RetroPGF Round 1](https://community.optimism.io/citizens-house/rounds/retropgf-1) voting rule.
     - `r2_mean`: R2 Mean Rule, where the mean number of votes is used for allocation. We replicate the [Optimism RetroPGF Round 2](https://community.optimism.io/citizens-house/rounds/retropgf-2) voting rule, the results are normalized.
     - `r3_median`: R3 Quorum Median rule, using the median of votes cast to allocate funds. We replicate the [Optimism RetroPGF Round 3](https://community.optimism.io/citizens-house/rounds/retropgf-3) voting rule, where a quorum applies and the results are normalized.
     - `r4_capped_median`: R4 Median Impact Metric Score, a capped version of median voting to ensure fairness across projects. We replicate the [Optimism Retro Funding Round 4](https://community.optimism.io/citizens-house/rounds/retropgf-4)) voting rule, where a quorum applies and the results are normalized. In our simulations we work with a simplified version R4a Simplified Capped Median and ignore first step to calculate the Impact Metric Score based on the project's KPIs.


3. **Evaluation Metrics** (`metrics.EvalMetrics`)
   - Provides functions to evaluate the performance of voting rules based on various metrics, such as
     - **VEV (Voter Extractable Value)**: Tests how much a voter can skew results for personal gain.
     - **Robustness**: Measures the system’s stability when a voter’s vote is altered.
     - **Cost of Bribery**: Measures how susceptible each voting rule is to bribery.
     - **Cost of Control**: Evaluates how difficult it is to control the voting outcome by adding or removing voters.
     - **Social Welfare**: Measures how well the allocation of funds satisfies the preferences of the voters.


### Agents

1. **VoterAgent** (`agents.VoterAgent`)
   - Models a voter who casts votes across multiple projects.
   - The behavior of voters is determined by different **voting models**, which simulate how voters distribute their tokens across projects:
     - **Random Uniform Model:** Voters randomly allocate their tokens using a uniform distribution.
     - **Optimized Reinforcement Model (Urn Model):** Uses an urn process where voters select projects based on past votes, and their choices influence future votes.
     - **Mallows Model:** Voters’ preferences deviate slightly from a central base vote, simulating how real-world preferences might differ by a small amount.
     - **Euclidean Model:** Projects and voters are placed in a 2D space, and votes are distributed based on proximity.
     - **Multinomial Model:** Voters distribute their tokens using probabilities sampled from a multinomial distribution.

2. **ProjectAgent** (`agents.ProjectAgent`)
   - Represents a project in the Retro Funding simulation.
   - Receives votes from the voters and eventually, funds are allocated based on the aggregated votes.
   - Tracks the total votes received and the final funds allocated for each project.

# Usage Guide

### Simulation Setup

1. **Initialization:**
   - The `VotingModel` is initialized with a defined number of voters, projects, and tokens to allocate. The simulation uses a variety of **voter types** and **voting rules** to simulate how different voting behaviors affect fund allocations.

   ```python
   model = VotingModel(voter_type="rn_model", num_voters=100, num_projects=10, total_op_tokens=10000)
   ```

2. **Running a Simulation:**
   - A simulation is run by calling the `run_simulation` method, which will execute one voting round and compile the fund allocations.

   ```python
   results = model.run_simulation()
   print(results)
   ```

3. **Allocating Funds:**
   - You can allocate funds using a specific voting rule. For example, to allocate funds using the quadratic rule:

   ```python
   allocation = model.allocate_funds('r1_quadratic')
   print(allocation)
   ```

4. **Custom Voting Rules:**
   - You can also define your own voting rule and add it to the model:

   ```python
   def custom_voting_rule(voting_matrix, total_funds, num_voters):
       # Custom logic here
       return np.sum(voting_matrix, axis=0) / np.sum(voting_matrix) * total_funds

   model.add_voting_rule("custom_rule", custom_voting_rule)
   ```

### Evaluation Metrics (examples)

1. **Cost of Bribery:**
   - Evaluate how difficult it is to bribe voters to skew the allocation toward a specific project:

   ```python
   metrics = EvalMetrics(model)
   bribery_results = metrics.evaluate_bribery(num_rounds=10)
   ```

2. **Gini Index Calculation:**
   - The Gini index measures the fairness of fund allocation:

   ```python
   gini_results, _ = metrics.evaluate_gini_index(num_rounds=10)
   ```

3. **VEV (Voter Extractable Value):**
   - Simulate how much value a single voter can extract by changing their votes:

   ```python
   vev_results = metrics.evaluate_vev(num_rounds=100)
   ```

4. **Robustness:**
   - Evaluate the robustness of a voting system by measuring the effect of random vote changes:

   ```python
   robustness_results = metrics.evaluate_robustness(num_rounds=100)
   ```

5. **Social Welfare and Egalitarian Scores:**
   - Evaluate how well fund allocation satisfies voter preferences and how evenly distributed allocations are:

   ```python
   social_welfare_results = metrics.evaluate_social_welfare(num_rounds=10)
   egalitarian_results = metrics.evaluate_egalitarian_score(num_rounds=10)
   ```

6. **Cost of Control:**
   - Evaluate the cost of adding or removing voters to manipulate voting outcomes:

   ```python
   control_results = metrics.evaluate_control(num_rounds=10, desired_increase=20)
   ```


## Experiments

For a detailed description of the experiments' key components, simulation steps and simulation output please refer to section ["Experiments"](https://github.com/GovXS/Evaluating-Voting-Design-Tradeoffs-for-Retro-Funding/blob/main/experiments/experiments.md).

## Voting Rule Verification

The **Voting Rule Verification** directory contains code that verifies the implementation of the voting rules in the **GovXS Retro Funding Simulator** by comparing them against historical data from previous RetroPGF/Retro Funding funding rounds. This section provides an explanation of the verification process, which involves cross-checking the outcomes of voting rules in the simulator with actual allocations from past rounds of the Retro Funding process.

#### Purpose

The primary purpose of this directory is to:
1. Ensure that the implemented voting rules (e.g., **quadratic voting**, **mean voting**, **median voting**) in the simulator are producing accurate results.
2. Compare the simulated allocations with the actual allocations from Retro Funding rounds.


### Verification Process by Round

#### Round 3 Verification

In this verification, the script:
1. Generates dummy voting data using a `DummyDataGenerator`.
2. Expands and formats the dummy data to simulate voting behavior.
3. Uses the `ProjectAllocator` to compute initial and scaled fund allocations based on the historic Round 3 voting data.
4. Applies the **median voting rule** (`r3_median`) from the `VotingRules` class to verify that the simulator’s allocation is correct.
5. Compares the scaled allocations from the historic data (`ProjectAllocator`) with the simulated allocations from our own implementation.

##### Key Elements:
- **DummyDataGenerator**: Generates sample voter data (e.g., number of votes, timestamp).
- **ProjectAllocator**: Computes initial and scaled allocations based on dummy voting data.
- **VotingRules (r3_median)**: Applies the median voting rule from our implementation.
- **Comparison**: Outputs a DataFrame that compares allocations from the historical data and our implementation.

```python
# Example comparison of scaled allocations and simulator allocations
comparison_df = pd.DataFrame({
    'Allocation (ProjectAllocator)': scaled_allocation['scaled_amount'].values,
    'Allocation (Our Implementation)': median_allocation
})
```

#### Round 2 Verification

In this round, the script:
1. Constructs a dummy voting matrix.
2. Applies the **mean voting rule** (`r2_mean`) from the `VotingRules` class to calculate allocations.
3. Compares the simulated allocation results to verify that the rule behaves correctly in the simulator.

##### Key Elements:
- **Voting Matrix**: A static matrix representing votes cast by voters across multiple projects.
- **VotingRules (r2_mean)**: Applies the mean voting rule and outputs allocations.

```python
mean_allocation = voting_rules.r2_mean(voting_matrix, total_op_tokens, num_voters)
print(mean_allocation)
```

#### Round 1 Verification

For Round 1, the script:
1. Reads the actual RetroPGF Round 1 data from a CSV file.
2. Cleans and formats the data for use in the simulation.
3. Applies the **quadratic voting rule** (`r1_quadratic`) from the `VotingRules` class to calculate fund allocations.
4. Compares the simulator's calculated allocations with the actual Round 1 allocations from the RetroPGF process.
5. Analyzes the differences between actual and simulated allocations, displaying summary statistics, scatter plots, bar plots, and histograms to visualize discrepancies.

##### Key Elements:
- **Actual Data**: Loaded from historic Round 1 CSV files.
- **VotingRules (r1_quadratic)**: Applies the quadratic voting rule to calculate allocations.
- **Comparison**: Compares actual versus calculated allocations using statistical analysis and visualizations.

```python
allocations_df['Absolute Difference'] = (allocations_df['Actual Allocations'] - allocations_df['Calculated Allocations']).abs()
allocations_df['Percentage Difference'] = (allocations_df['Absolute Difference'] / allocations_df['Actual Allocations']) * 100
```


## Round 4 Voting Rule Comparison: Capped Median Impact Metric vs. Majoritarian Moving Phantoms

In this section, we detail the process and comparison between the **R4 Capped Median Impact Metric** rule used by Optimism for Round 4 of RetroPGF and our proposed **Majoritarian Moving Phantoms** voting rule. The goal of this experiment is to understand how our proposed rule compares with the existing capped median rule, in terms of fund allocation for different projects.

#### Objective

The **Capped Median Impact Metric Rule** (R4) is a modified median-based approach used to distribute funds based on project impact metrics. The **Majoritarian Moving Phantoms** rule, in contrast, employs an iterative process that adds phantom votes to simulate more robust median voting outcomes. This experiment compares the allocations derived from both methods using the same voting and project data.

#### Process

1. **Data Collection**:
   - We used the actual project and badgeholder data from **RetroPGF Round 4**. This data includes badgeholder votes, their impact metric scores, and the total OP tokens allocated to projects.
   - The project data is stored in three primary datasets: `Voting data export final.csv`, `RPGF4_badgeholders.csv`, and `op_rf4_impact_metrics_by_project.csv`.

2. **Capped Median Impact Metric Rule**:
   - This rule caps the number of tokens a voter can allocate to a single project, as well as the median amount that projects can receive. It ensures that no single project dominates the fund distribution and that low-impact projects are eliminated.
   - We calculated the allocation for each project using this rule and scaled the results to ensure that the total allocation did not exceed the available OP tokens.

3. **Majoritarian Moving Phantoms Rule**:
   - Our proposed rule simulates additional "phantom" voters to influence the median of the voting distribution.
   - This method uses an iterative process to converge on a stable allocation, ensuring that the overall token distribution is more robust to vote manipulation.
   - We applied this rule to the same voting matrix and calculated the project allocations.

4. **Comparison**:
   - After applying both rules, we compared the project allocations generated by the **Capped Median Impact Metric Rule** and the **Majoritarian Moving Phantoms Rule**.
   - Several visualization techniques were employed to better understand the differences between the two rules.

#### Results

The following steps were performed to conduct the comparison:

1. **Data Normalization**:
   - The initial badgeholder allocation data was normalized using the capped median approach. This ensured that the total allocation per project did not exceed the allowed limits.
   - The **Majoritarian Moving Phantoms Rule** was applied to the same normalized data.

2. **Aggregating and Comparing Results**:
   - The results from both rules were aggregated into a unified DataFrame, containing the project names, allocations from both rules, and the final scaled allocations.
   - We calculated additional statistics such as **allocation difference** and **percentage change** between the two rules.

3. **Visualizations**:
   - **Bar Plots**: Visualized the difference in allocations for each project under both rules.
   - **Box Plots**: Showed the distribution of allocations for both rules.
   - **Scatter Plots**: Highlighted the correlation between the two allocation methods.
   - **Top Projects Plot**: Focused on the top N projects (by allocation) to understand how they were affected by the change in voting rules.



### Data Directory

The **data** directory contains three subdirectories:

1. **historic_data**:
   - Holds **historical data** from previous Retro Funding rounds used for **voting rule verification**.
   - Includes project funding allocations, badgeholder votes, and impact metrics.

2. **simulation_data**:
   - Contains **data from simulation experiments**, such as control, bribery, robustness, and VEV experiments.
   - Stores simulated fund allocations and experiment results.

3. **vm_data**:
   - An **empty directory** for storing results of **newly run simulations** by users.


# Conclusion

The **GovXS Retro Funding Simulator** offers a flexible and powerful tool for testing and evaluating different voting mechanisms in public goods funding. By using agent-based modeling, it provides detailed insights into how voting behavior and fund allocation change under various rules and metrics. This makes it ideal for exploring new voting systems and understanding their strengths and vulnerabilities.
