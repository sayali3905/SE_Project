import pandas as pd

def greedy_tsr(df, reduction_ratio=0.5):
    """
    Greedy Test-Suite Reduction (TSR) by reducing test_LOC based on a given ratio.
    
    Args:
        df (DataFrame): Input dataset.
        reduction_ratio (float): Percentage of test cases to remove.

    """
    df = df.copy()
    df['reduced_test_LOC'] = (df['test_LOC'] * (1 - reduction_ratio)).astype(int)
    df['travis_duration_days'] = df['travis_duration_days'] * (df['reduced_test_LOC'] / df['test_LOC'])
    df['travis_duration_days'] = df['travis_duration_days'].fillna(df['travis_duration_days'].mean())

    return df

def save_greedy_tsr(input_file, output_file):
    df = pd.read_csv(input_file)
    df = greedy_tsr(df)
    # df = df[['repo_name', 'total_LOC', 'test_LOC', 'reduced_test_LOC']]
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    save_greedy_tsr("data.csv", "processed_greedy.csv")
