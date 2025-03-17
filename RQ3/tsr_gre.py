import pandas as pd
import numpy as np

def gre_tsr(df):
    """
    Greedy Random Elimination (GRE) Test-Suite Reduction.
    - Randomly removes test cases, leading to potential loss in coverage.

    Args:
        df (DataFrame): Input dataset.

    """
    df = df.copy()
    np.random.seed(42)
    df['reduced_test_LOC_GRE'] = df['test_LOC'].apply(lambda x: int(x * np.random.uniform(0.4, 0.6)))
    df['travis_duration_days'] = df['travis_duration_days'] * (df['reduced_test_LOC_GRE'] / df['test_LOC'])
    df['travis_duration_days'] = df['travis_duration_days'].fillna(df['travis_duration_days'].mean())

    return df

def save_gre_tsr(input_file, output_file):
    df = pd.read_csv(input_file)
    df = gre_tsr(df)
    # df = df[['repo_name', 'total_LOC', 'test_LOC', 'reduced_test_LOC_GRE']]
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    save_gre_tsr("data.csv", "processed_gre.csv")
