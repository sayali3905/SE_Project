import pandas as pd

def compute_fbdl(df, column_name):
    """
    Computes Failed-Build Detection Loss (FBDL) based on test_LOC reduction.

    Formula: FBDL = (test_LOC - reduced_test_LOC) / test_LOC

    Args:
        df (DataFrame): Dataset with test_LOC and reduced test suite.
        column_name (str): Name of the column containing reduced test cases.

    Returns:
            DataFrame: Dataset with computed FBDL.
    """
    df = df.copy()
    df['FBDL'] = ((df['test_LOC'] - df[column_name]) / df['test_LOC']).round(2)
    return df

def save_fbdl(input_file, column_name, output_file):
    df = pd.read_csv(input_file)
    df = compute_fbdl(df, column_name)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    save_fbdl("processed_greedy.csv", "reduced_test_LOC", "fbdl_greedy.csv")
    save_fbdl("processed_ge.csv", "reduced_test_LOC_GE", "fbdl_ge.csv")
    save_fbdl("processed_gre.csv", "reduced_test_LOC_GRE", "fbdl_gre.csv")
    save_fbdl("processed_hgs.csv", "reduced_test_LOC_HGS", "fbdl_hgs.csv")
