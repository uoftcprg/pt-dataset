from collections import defaultdict
from itertools import chain
from json import loads
from sys import stdin, stdout

from tqdm import tqdm
import numpy as np
import pandas as pd


def expand(row):
    data = loads(row['raw'])
    rows = []

    for datum in data['players']:
        row = {}

        if 'currency' in data:
            row['currency'] = data['currency']

        row['place'] = datum.get('place', '')
        row['player'] = datum['player'].get('title', '')
        row['country'] = datum['player'].get('country', {}).get('title', '')

        if 'chipcounts' in datum:
            row['progress'] = datum['chipcounts'].get('progress', '0')
            row['chips'] = datum['chipcounts']['chips']

        if 'payouts' in datum:
            row['winning'] = datum['payouts']['winning']

        rows.append(row)

    return rows


def main():
    tqdm.pandas()

    df = pd.read_csv(stdin, index_col=0, dtype=str)
    df['raw'] = df['raw'].str.strip().replace('', np.nan)
    df = df[df['raw'].notnull()]
    expansions = df.progress_apply(expand, axis=1)
    indices = df.index.repeat(list(map(len, expansions)))
    df = df.loc[indices].reset_index(drop=True)
    data = defaultdict(list)

    for expansion in chain.from_iterable(expansions):
        for key, value in expansion.items():
            data[key].append(value)

    df = pd.concat([df.drop(columns='raw'), pd.DataFrame(data)], axis=1)

    df.to_csv(stdout)


if __name__ == '__main__':
    main()
