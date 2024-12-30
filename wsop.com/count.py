from sys import stdin

import pandas as pd


def main():
    df = pd.read_csv(stdin, index_col=0, dtype=str)

    print(df['tid'].nunique())


if __name__ == '__main__':
    main()
