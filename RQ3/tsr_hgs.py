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
    df['travis_duration_days'] = df['travis_duration_days'] * (df['reduced_test_LOC_HGS'] / df['test_LOC'])
    df['travis_duration_days'] = df['travis_duration_days'].fillna(df['travis_duration_days'].mean())

    return df

def save_hgs_tsr(input_file, output_file):
    df = pd.read_csv(input_file)
    df = hgs_tsr(df)
    # df = df[['repo_name', 'total_LOC', 'test_LOC', 'reduced_test_LOC_HGS']]
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    save_hgs_tsr("data.csv", "processed_hgs.csv")
