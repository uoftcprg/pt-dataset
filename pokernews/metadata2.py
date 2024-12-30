from collections import defaultdict
from itertools import chain
from sys import stdin, stdout
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
import pandas as pd

URL = 'https://www.pokernews.com'


def get_html(url_path):
    url = urljoin(URL, url_path)
    html = get(url).text

    return html


def expand(row):
    url_path = row['event_href']
    html = get_html(url_path)
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('.nextDay')

    if not elements:
        return [{'day': '1', 'day_href': url_path}]

    days = []

    for element in elements:
        day = {'day': element.text, 'day_href': element.get('href', url_path)}

        days.append(day)

    return days


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

    df = pd.concat([df, pd.DataFrame(data)], axis=1)

    df.to_csv(stdout)


if __name__ == '__main__':
    main()
