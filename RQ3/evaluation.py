import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os

plot_folder = "plots"
os.makedirs(plot_folder, exist_ok=True)

def load_fbdl_results():
    """Loads FBDL results from all TSR methods into a dictionary of DataFrames."""
    files = {
        "Greedy TSR": "fbdl_greedy.csv",
        "Greedy Exact (GE)": "fbdl_ge.csv",
        "Greedy Random Elimination (GRE)": "fbdl_gre.csv",
        "Hierarchical Greedy Selection (HGS)": "fbdl_hgs.csv"
    }
    dataframes = {method: pd.read_csv(file) for method, file in files.items()}
    return dataframes

def visualize_fbdl(dataframes):
    """Generates boxplot comparing FBDL distributions across TSR methods with short labels."""
    short_labels = ["Greedy", "GE", "GRE", "HGS"]
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(
        [df["FBDL"] for df in dataframes.values()],
        labels=short_labels  
    )
    
    plt.ylabel("FBDL")
    plt.title("Comparison of FBDL Across TSR Methods")
    plt.xticks(rotation=15) 
    plt.grid(True)
    
    plot_path = os.path.join(plot_folder, "fbdl_comparison.png")
    plt.savefig(plot_path)
    plt.show()

def find_best_tsr_method(dataframes):
    """Finds the TSR method with the lowest average FBDL"""
    
    avg_fbdl = {method: df["FBDL"].mean() for method, df in dataframes.items()}
    best_method = min(avg_fbdl, key=avg_fbdl.get)
    short_labels = ["Greedy", "GE", "GRE", "HGS"]

    plt.figure(figsize=(8, 5))
    plt.bar(short_labels, avg_fbdl.values(), color=['blue', 'green', 'red', 'purple'])
    
    plt.ylabel("Average FBDL")
    plt.title("Average FBDL Across Different TSR Methods")
    plt.xticks(rotation=15)  
    plt.grid(axis='y', linestyle="--", alpha=0.7)

    plot_path = os.path.join(plot_folder, "fbdl_average.png")
    plt.savefig(plot_path)
    plt.show()
    
    print("\nAverage FBDL for Each TSR Method:")
    for method, fbdl in avg_fbdl.items():
        print(f"{method}: {fbdl:.4f}")

    return best_method

def compute_correlations(dataframes, execution_times):
    """Computes pearson and spearman correlations between test reduction and CI duration."""
    correlation_results = []

    for method, df in dataframes.items():
        df = df.copy()
        df["ci_duration"] = df["travis_duration_days"]

        # Ensure variation exists in CI duration
        if df["ci_duration"].nunique() == 1:
            print(f"Constant CI duration for {method}, setting correlation to 0.")
            pearson_corr, spearman_corr = 0.0, 0.0
        else:
            pearson_corr, _ = stats.pearsonr(df["FBDL"], df["ci_duration"])
            spearman_corr, _ = stats.spearmanr(df["FBDL"], df["ci_duration"])

        correlation_results.append({
            "TSR Method": method,
            "Pearson Correlation": pearson_corr,
            "Spearman Correlation": spearman_corr
        })

    correlation_df = pd.DataFrame(correlation_results)
    return correlation_df

def plot_correlation_scatter(dataframes, execution_times):
    """Plots test reduction % vs CI duration."""
    plt.figure(figsize=(12, 8))
    has_data = False

    column_map = {
        "Greedy TSR": "reduced_test_LOC",
        "Greedy Exact (GE)": "reduced_test_LOC_GE",
        "Greedy Random Elimination (GRE)": "reduced_test_LOC_GRE",
        "Hierarchical Greedy Selection (HGS)": "reduced_test_LOC_HGS"
    }

    for method, df in dataframes.items():
        if method not in execution_times or execution_times[method] is None:
            continue

        reduced_col = column_map.get(method)

        df["test_reduction_%"] = 100 * (df["test_LOC"] - df[reduced_col]) / df["test_LOC"]
        df["ci_duration"] = execution_times[method]

        plt.scatter(df["test_reduction_%"], df["ci_duration"], label=method, alpha=0.6)
        has_data = True

    plt.xlabel("Test Reduction (%)")
    plt.ylabel("Travis CI Duration (Days)")
    plt.title("Test Reduction vs. CI Duration")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(plot_folder, "correlation_scatter.png"))
    plt.show()


def plot_correlation_heatmap(correlation_df):
    """Plots a heatmap of Pearson and Spearman correlation coefficients."""

    correlation_df.set_index("TSR Method", inplace=True)

    # Ensure numeric data 
    numeric_data = correlation_df.select_dtypes(include=['float64', 'int64'])

    plt.figure(figsize=(10, 7))
    sns.heatmap(numeric_data, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f")
    plt.title("Correlation Heatmap: Test Reduction vs. CI Duration")

    plot_path = os.path.join(plot_folder, "correlation_heatmap.png")
    plt.savefig(plot_path)
    plt.show()

if __name__ == "__main__":
    dataframes = load_fbdl_results()
    visualize_fbdl(dataframes)
    find_best_tsr_method(dataframes)
    execution_times = {
    method: df["travis_duration_days"] if "travis_duration_days" in df.columns else None
    for method, df in dataframes.items()
    }

    correlation_df = compute_correlations(dataframes, execution_times)
    plot_correlation_scatter(dataframes, execution_times)
    plot_correlation_heatmap(correlation_df)
