# RQ3: Analysis of Test Suite Reduction (TSR) in CI Pipelines

This RQ investigates the impact of **Test Suite Reduction (TSR)** on **CI efficiency** by evaluating four different TSR techniques. The methods analyzed are:

- **Greedy TSR:** Reduces test suite size by 50%.
- **Greedy Exact (GE):** Removes redundant test cases, retaining ~75% of the test suite.
- **Greedy Random Elimination (GRE):** Randomly eliminates 40-60% of test cases.
- **Hierarchical Greedy Selection (HGS):** Prioritizes highly executed and high-failure tests, reducing suite size by ~35%.

We assess the **Failed-Build Detection Loss (FBDL)** for each method and analyze the correlation between test reduction and CI execution time using **Pearson** and **Spearman** coefficients. Additionally, **Random Forest** and **XGBoost** models are used to predict CI execution time.

---

## Installation

Ensure **Python (>=3.7)** is installed, then install dependencies using:

```sh
pip install -r requirements.txt
```

---

## Usage

To run the analysis, navigate to the project directory and execute:

```sh
python main.py
```

After execution, the following results will be generated:

1. **Processed TSR Data:** CSV files storing reduced test suites:
   - `processed_greedy.csv`
   - `processed_ge.csv`
   - `processed_gre.csv`
   - `processed_hgs.csv`

2. **Performance Metrics:**
   - Summary of execution times
   - Fault-Based Detection Loss (FBDL)

3. **Correlation Analysis:**
   - Pearson and Spearman correlation coefficients.

4. **Machine Learning Predictions:**
   - **Random Forest** and **XGBoost** models trained for CI time prediction.

5. **Visualization Plots:** _(Stored in `/plots` folder)_
   - `fbdl_comparison.png` → Comparison of FBDL across TSR methods.
   - `fbdl_average.png` → Average FBDL for each method.
   - `correlation_scatter.png` → Scatter plot of test reduction vs. CI duration.
   - `correlation_heatmap.png` → Heatmap of correlation values.
   - `fbdl_rf_comparison.png` → Random Forest prediction comparison.
   - `fbdl_xgboost_comparison.png` → XGBoost prediction comparison.

---

## Results Interpretation

- **Best TSR Method:** Greedy Exact (GE) achieved the lowest FBDL (0.2629), balancing test suite reduction and fault detection capability.
- **Correlation Findings:** Weak negative correlation values indicate that reducing the test suite does not necessarily lead to a proportional reduction in CI execution time.
- **Model Performance:** Random Forest consistently outperformed XGBoost in predicting CI execution time.

---