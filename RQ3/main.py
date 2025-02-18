import tsr_greedy
import tsr_ge
import tsr_gre
import tsr_hgs
import compute_fbdl
import evaluation
import prediction

if __name__ == "__main__":
    print("Running TSR methods and computing FBDL...")

    dataset_file = "data.csv"

    # Run TSR Methods
    tsr_greedy.save_greedy_tsr(dataset_file, "processed_greedy.csv")
    tsr_ge.save_ge_tsr(dataset_file, "processed_ge.csv")
    tsr_gre.save_gre_tsr(dataset_file, "processed_gre.csv")
    tsr_hgs.save_hgs_tsr(dataset_file, "processed_hgs.csv")

    print("TSR methods applied successfully!")

    # Compute FBDL for Each TSR Method
    compute_fbdl.save_fbdl("processed_greedy.csv", "reduced_test_LOC", "fbdl_greedy.csv")
    compute_fbdl.save_fbdl("processed_ge.csv", "reduced_test_LOC_GE", "fbdl_ge.csv")
    compute_fbdl.save_fbdl("processed_gre.csv", "reduced_test_LOC_GRE", "fbdl_gre.csv")
    compute_fbdl.save_fbdl("processed_hgs.csv", "reduced_test_LOC_HGS", "fbdl_hgs.csv")

    print("FBDL computations completed!")

    # Evaluation
    print("Evaluating TSR and FBDL Results...")
    dataframes = evaluation.load_fbdl_results()
    evaluation.display_summary(dataframes)
    evaluation.visualize_fbdl(dataframes)
    best_method = evaluation.find_best_tsr_method(dataframes)

    print(f"\nBest TSR Method: {best_method}")

    # Train ML Models for FBDL Prediction
    print("\nTraining ML Models for All TSR Methods...")
    rf_results, rf_predictions = prediction.train_fbdl_models(dataframes)
    xgb_results, xgb_predictions = prediction.train_xgboost_models(dataframes)

    print("\nGenerating Prediction Comparison Plots...")
    prediction.plot_predictions(rf_predictions, "Random Forest", "fbdl_rf_comparison.png")
    prediction.plot_predictions(xgb_predictions, "XGBoost", "fbdl_xgboost_comparison.png")

    # Print Model Comparison Results
    print("\nModel Comparison:")
    for method in rf_results:
        print(f"\n🔹 {method}")
        print(f"  - Random Forest: MAE={rf_results[method]['MAE']:.4f}, R²={rf_results[method]['R² Score']:.4f}")
        print(f"  - XGBoost: MAE={xgb_results[method]['MAE']:.4f}, R²={xgb_results[method]['R² Score']:.4f}")

    print("\nAll tasks completed successfully!")
