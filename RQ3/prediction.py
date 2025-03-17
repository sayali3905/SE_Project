import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

plot_folder = "plots"
os.makedirs(plot_folder, exist_ok=True)

def load_ml_data():
    """Loads FBDL datasets for all TSR methods and returns them as a dictionary."""
    files = {
        "Greedy TSR": "fbdl_greedy.csv",
        "Greedy Exact (GE)": "fbdl_ge.csv",
        "Greedy Random Elimination (GRE)": "fbdl_gre.csv",
        "Hierarchical Greedy Selection (HGS)": "fbdl_hgs.csv"
    }
    return {method: pd.read_csv(file) for method, file in files.items()}

def train_fbdl_models(dataframes):
    """Trains and evaluates Random Forest models for all TSR methods."""
    results = {}
    predictions = {}

    for method, df in dataframes.items():
        print(f"\nTraining Random Forest Model for {method}...")

        features = ['stars', 'issues', 'open_prs', 'closed_prs', 'total_prs', 'size_mb', 'travis_duration_days', 'total_LOC', 'test_LOC']
        target = 'FBDL'

        X = df[features].copy()
        y = df[target].copy()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

        model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        results[method] = {"MAE": mae, "R² Score": r2}
        predictions[method] = (y_test.values, y_pred)

        print(f"{method} Random Forest Performance: MAE={mae:.4f}, R² Score={r2:.4f}")

    return results, predictions

def train_xgboost_models(dataframes):
    """Trains and evaluates XGBoost models for all TSR methods."""
    results = {}
    xgb_predictions = {}

    for method, df in dataframes.items():
        print(f"\nTraining XGBoost Model for {method}..")

        features = ['stars', 'issues', 'open_prs', 'closed_prs', 'total_prs', 'size_mb', 'travis_duration_days', 'total_LOC', 'test_LOC']
        target = 'FBDL'

        X = df[features]
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

        model = XGBRegressor(n_estimators=50, learning_rate=0.05, max_depth=4, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        results[method] = {"MAE": mae, "R² Score": r2}
        xgb_predictions[method] = (y_test.values, y_pred)

        print(f"{method} XGBoost Performance: MAE={mae:.4f}, R² Score={r2:.4f}")

    return results, xgb_predictions

def plot_predictions(predictions, model_name, filename):
    """Plots actual vs. predicted FBDL values for a given ML model."""
    plt.figure(figsize=(10, 6))

    bright_colors = ["deepskyblue", "lime", "red", "gold"]  # Brighter colors
    for (method, (y_test, y_pred)), color in zip(predictions.items(), bright_colors):
        plt.scatter(y_test, y_pred, label=method, color=color, alpha=0.7, edgecolors="black")

    plt.plot([0, 1], [0, 1], "--", color="black", label="Perfect Prediction")
    plt.xlabel("Actual FBDL")
    plt.ylabel("Predicted FBDL")
    plt.title(f"Actual vs. Predicted FBDL for {model_name}")
    plt.legend()

    plot_path = os.path.join(plot_folder, filename)
    plt.savefig(plot_path)
    plt.show()

def rank_tsr_methods(rf_results, xgb_results):
    """Ranks TSR methods based on model performance and efficiency"""
    ranking = []

    for method in rf_results:
        rf_mae, rf_r2 = rf_results[method]["MAE"], rf_results[method]["R² Score"]
        xgb_mae, xgb_r2 = xgb_results[method]["MAE"], xgb_results[method]["R² Score"]
        best_model = "Random Forest" if rf_mae < xgb_mae else "XGBoost"

        ranking.append({
            "TSR Method": method,
            "RF MAE": rf_mae, "RF R²": rf_r2,
            "XGB MAE": xgb_mae, "XGB R²": xgb_r2,
            "Best Model": best_model
        })

    return pd.DataFrame(ranking).sort_values(by=["XGB MAE", "RF MAE"])

if __name__ == "__main__":
    dataframes = load_ml_data()

    # Train Random Forest
    rf_results, rf_predictions = train_fbdl_models(dataframes)
    plot_predictions(rf_predictions, "Random Forest", "fbdl_rf_comparison.png")

    # Train XGBoost
    xgb_results, xgb_predictions = train_xgboost_models(dataframes)
    plot_predictions(xgb_predictions, "XGBoost", "fbdl_xgboost_comparison.png")

    print("\nModel Comparison:")
    for method in rf_results:
        print(f"\n  {method}")
        print(f"  - Random Forest: MAE={rf_results[method]['MAE']:.4f}, R²={rf_results[method]['R² Score']:.4f}")
        print(f"  - XGBoost: MAE={xgb_results[method]['MAE']:.4f}, R²={xgb_results[method]['R² Score']:.4f}")

    ranking_df = rank_tsr_methods(rf_results, xgb_results)
    print(ranking_df)