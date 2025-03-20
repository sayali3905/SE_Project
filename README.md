# Optimization of Continuous Integration Pipelines Through Code and Test Complexity Analysis

This project mainly addresses the following research questions:
1. What is the impact of CI practices on the evolution and maintainability of test code?
2. How is the size of a test case correlated with the number of lines of code and the number of new
features added?
3. How does test suite size impact efficiency in CI pipelines?
4. Analyzing trends before and after the adoption of CI and their correlation with test code ratio and
test coverage. What key factors influence the test code ratio?

DataCollection folder demonstrates the data collection steps and filtering methods.
Final_repositories.csv file contains the dataset of 70 repositories which are used for analysis.

RQ1 folder answers the research question 1 and contains the following contents:
- /Analysis_Code_Churn_Rate.ipynb - Plots and statistical tests for code churn rate  
- /Analysis_Cyclomatic_Complexity.ipynb - Plots and statistical tests for cyclomatic complexity  
- /Churn_Rate_Calculation.sh - Code Churn Rate calculation for test code evolution  
- /Cyclomatic_Complexity_Calculation.sh - Cyclomatic Complexity for test code maintainability  



