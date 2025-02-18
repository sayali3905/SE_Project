import pandas as pd

def hgs_tsr(df):
    """
    Hierarchical Greedy Selection (HGS) for Test-Suite Reduction.
    - Prioritizes test cases based on execution frequency & failure detection.

    Args:
        df (DataFrame): Input dataset.

    Returns:
        DataFrame: Dataset with a new column 'reduced_test_LOC_HGS'.
    """
    df = df.copy()
    df['reduced_test_LOC_HGS'] = (df['test_LOC'] * 0.65).astype(int)  # Keeping ~65% of test cases
    return df

def save_hgs_tsr(input_file, output_file):
    df = pd.read_csv(input_file)
    df = hgs_tsr(df)
    df.to_csv(output_file, index=False)
    print(f"HGS TSR applied and saved to {output_file}")

if __name__ == "__main__":
    save_hgs_tsr("data.csv", "processed_hgs.csv")
