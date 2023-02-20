import pandas as pd


def read_csv(file):
    df = pd.read_csv(file, dtype=str)
    return df
