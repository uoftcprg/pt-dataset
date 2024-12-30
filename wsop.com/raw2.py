from collections import defaultdict
from itertools import chain
from sys import argv, stdin, stdout

from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
import pandas as pd

URL = argv[1]


def expand(row):
    aid, grid, tid = row[['aid', 'grid', 'tid']]
    html = row['raw']
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('#selectDay > select option')
    days = []

    for element in elements:
        day = {'dayof': element['value'], 'day': element.text}

        days.append(day)

    expansion = []

    for day in tqdm(days, leave=False):
        dayof = day['dayof']
        curpage = '1'
        url = URL.format(aid, grid, tid, dayof, curpage)
        html = get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.select('#PagingNav > div a')
        curpages = [curpage]

        for element in elements:
            curpage = element.text

            curpages.append(curpage)

        for curpage in tqdm(curpages, leave=False):
            url = URL.format(aid, grid, tid, dayof, curpage)
            raw = get(url).text

            expansion.append(day | {'curpage': curpage, 'raw': raw})

    return expansion


def main():
    tqdm.pandas()

    df = pd.read_csv(stdin, index_col=0, dtype=str)
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
