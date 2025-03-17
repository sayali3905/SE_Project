import tsr_greedy
import tsr_ge
import tsr_gre
import tsr_hgs
import compute_fbdl
import evaluation
import prediction
import scipy.stats as stats
import pandas as pd

if __name__ == "__main__":
    dataset_file = "data.csv"

    # Run TSR Methods
    tsr_greedy.save_greedy_tsr(dataset_file, "processed_greedy.csv")
    tsr_ge.save_ge_tsr(dataset_file, "processed_ge.csv")
    tsr_gre.save_gre_tsr(dataset_file, "processed_gre.csv")
    tsr_hgs.save_hgs_tsr(dataset_file, "processed_hgs.csv")

    # Compute FBDL for Each TSR Method
    compute_fbdl.save_fbdl("processed_greedy.csv", "reduced_test_LOC", "fbdl_greedy.csv")
    compute_fbdl.save_fbdl("processed_ge.csv", "reduced_test_LOC_GE", "fbdl_ge.csv")
    compute_fbdl.save_fbdl("processed_gre.csv", "reduced_test_LOC_GRE", "fbdl_gre.csv")
    compute_fbdl.save_fbdl("processed_hgs.csv", "reduced_test_LOC_HGS", "fbdl_hgs.csv")

    dataframes = evaluation.load_fbdl_results()
    evaluation.visualize_fbdl(dataframes)
    best_method = evaluation.find_best_tsr_method(dataframes)

    execution_times = {}

    for method, file in {
    "Greedy TSR": "processed_greedy.csv",
    "Greedy Exact (GE)": "processed_ge.csv",
    "Greedy Random Elimination (GRE)": "processed_gre.csv",
    "Hierarchical Greedy Selection (HGS)": "processed_hgs.csv"
    }.items():
        df = pd.read_csv(file)

        if "travis_duration_days" in df.columns:
            max_ci_duration = df["travis_duration_days"].max()
            df["ci_reduction_%"] = 100 * (max_ci_duration - df["travis_duration_days"]) / max_ci_duration
            execution_times[method] = df["ci_reduction_%"].mean()

            if method in dataframes:
                dataframes[method] = dataframes[method].merge(df[["repo_name", "ci_reduction_%"]], on="repo_name", how="left")

    for method, df in dataframes.items():
        if "ci_reduction_%" in df.columns and not df["ci_reduction_%"].isnull().all():
            pearson_corr, _ = stats.pearsonr(df["ci_reduction_%"].dropna(), df["test_LOC"].dropna())
            spearman_corr, _ = stats.spearmanr(df["ci_reduction_%"].dropna(), df["test_LOC"].dropna())
            print(f"{method} - Pearson: {pearson_corr:.4f}, Spearman: {spearman_corr:.4f}")

    correlation_df = evaluation.compute_correlations(dataframes, execution_times)
    evaluation.plot_correlation_scatter(dataframes, execution_times)
    evaluation.plot_correlation_heatmap(correlation_df)

    # Identify the best TSR method based on FBDL
    best_method = evaluation.find_best_tsr_method(dataframes)
    print(f"\nBest TSR Method: {best_method}")

    # Train ML Models for FBDL Prediction
    rf_results, rf_predictions = prediction.train_fbdl_models(dataframes)
    xgb_results, xgb_predictions = prediction.train_xgboost_models(dataframes)

    prediction.plot_predictions(rf_predictions, "Random Forest", "fbdl_rf_comparison.png")
    prediction.plot_predictions(xgb_predictions, "XGBoost", "fbdl_xgboost_comparison.png")

    print("\nModel Comparison:")
    for method in rf_results:
        print(f"\n {method}")
        print(f"  - Random Forest: MAE={rf_results[method]['MAE']:.4f}, R²={rf_results[method]['R² Score']:.4f}")
        print(f"  - XGBoost: MAE={xgb_results[method]['MAE']:.4f}, R²={xgb_results[method]['R² Score']:.4f}")

    ranking_df = prediction.rank_tsr_methods(rf_results, xgb_results)
    print("\nFinal TSR Rankings:")
    print(ranking_df)