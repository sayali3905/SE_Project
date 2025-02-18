import pandas as pd
import matplotlib.pyplot as plt
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

def display_summary(dataframes):
    """Prints summary statistics for each TSR method's FBDL."""
    for method, df in dataframes.items():
        print(f"\n🔹 {method} Results:")
        print(df[['repo_name', 'test_LOC', 'FBDL']].head())  # Show first few rows
        print(df.describe()) 

# Generate and save comparative FBDL visualizations
def visualize_fbdl(dataframes):
    """Generates and saves a boxplot comparing FBDL distributions across TSR methods with short labels."""
    
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

    print(f"FBDL comparison plot saved to {plot_path}")


def find_best_tsr_method(dataframes):
    """Finds the TSR method with the lowest average FBDL and saves bar plot with short labels."""
    
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

    print(f"\nBest TSR Method: {best_method} (Lowest FBDL)")
    return best_method


if __name__ == "__main__":
    print("Evaluating TSR and FBDL Results...")
    dataframes = load_fbdl_results()
    display_summary(dataframes)
    visualize_fbdl(dataframes)
    find_best_tsr_method(dataframes)
