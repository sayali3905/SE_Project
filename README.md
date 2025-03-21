# Optimization of Continuous Integration Pipelines Through Code and Test Complexity Analysis

This project mainly focuses on the following research questions:
1. What is the impact of CI practices on the evolution and maintainability of test code?
2. How is the size of a test case correlated with the number of lines of code and the number of new
features added?
3. How does test suite size impact efficiency in CI pipelines?
4. Analyzing trends before and after the adoption of CI and their correlation with test code ratio and
test coverage. What key factors influence the test code ratio?

DataCollection folder demonstrates the data collection steps and filtering methods.
Final_repositories.csv file contains the dataset of 70 repositories which are used for analysis.

RQ1 folder addresses the research question 1 and contains the following contents:
- /Analysis_Code_Churn_Rate.ipynb - Plots and statistical tests for code churn rate  
- /Analysis_Cyclomatic_Complexity.ipynb - Plots and statistical tests for cyclomatic complexity  
- /Churn_Rate_Calculation.sh - Code Churn Rate calculation for test code evolution  
- /Cyclomatic_Complexity_Calculation.sh - Cyclomatic Complexity for test code maintainability

RQ2 folder addresses the research question 2 and contains the following contents:
- /RQ2 Analysis.ipynb - Analysis of correlations between test LOC and total LOC and test LOC and closed PRs. 
- /RQ2 Final Analysis.ipynb - Advanced analysis incorporating clustering, PCA visualization, and partial correlation analysis for deeper insights.
It is dependent on FINAL_repositiories.csv present in the main folder for data.

RQ3 folder addresses the research question3 and contains the following contents:
- main.py – Runs the full pipeline, applying TSR methods, generating results, and triggering evaluation.
- evaluation.py – Computes FBDL, correlation values, and other performance metrics for each TSR method.
- prediction.py – Trains and evaluates Random Forest and XGBoost models to predict CI execution time.
- More details are available in the RQ3-specific README.

For RQ4 folder that addresses the last research question, please clone this repository and use the files in this folder in the following ways : 
- FINAL DATASET LAST.csv : consists of a comprehensive dataset with the original attributes along with the various factors that are used to analyze the behaviour of test coverage and ratio due to the incorporation of Travis CI for every repository.
- FINAL DATASET LAST DOMAIN : consists of previous dataset with included domain of the software. Used for analysing important factors affecting Test Ratio.
- RQ4_Before vs After CI.ipynb : the actual notebook containing the analysis
- IMPORTANT FACTORS AFFECTING TEST RATIO.ipynb : consists of collection of domain, linear mixed model calculating important factors and their respective coeff. and visualizing it through a graph. 
- commits.ipynb and test_files_and_committers_extraction (1).ipynb : used for cloning and pulling the factor related details for every repository.

