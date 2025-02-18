import pandas as pd
import numpy as np

def gre_tsr(df):
    """
    Greedy Random Elimination (GRE) Test-Suite Reduction.
    - Randomly removes test cases, leading to potential loss in coverage.

    Args:
        df (DataFrame): Input dataset.

    Returns:
        DataFrame: Dataset with a new column 'reduced_test_LOC_GRE'.
    """
    df = df.copy()
    np.random.seed(42)
    df['reduced_test_LOC_GRE'] = df['test_LOC'].apply(lambda x: int(x * np.random.uniform(0.4, 0.6)))
    return df

def save_gre_tsr(input_file, output_file):
    df = pd.read_csv(input_file)
    df = gre_tsr(df)
    df.to_csv(output_file, index=False)
    print(f"GRE TSR applied and saved to {output_file}")

if __name__ == "__main__":
    save_gre_tsr("data.csv", "processed_gre.csv")
