from sys import argv, stdin, stdout

from requests import get
from tqdm import tqdm
import pandas as pd

URL = argv[1]


def get_raw(row):
    aid, grid, tid = row[['aid', 'grid', 'tid']]
    url = URL.format(aid, grid, tid)
    raw = get(url).text

    return raw


def main():
    tqdm.pandas()

    df = pd.read_csv(stdin, index_col=0, dtype=str)
    df['raw'] = df.progress_apply(get_raw, axis=1)

    df.to_csv(stdout)


if __name__ == '__main__':
    main()
