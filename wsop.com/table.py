from collections import defaultdict
from sys import stdin, stdout

from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


def expand(row):
    html = row['raw']
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('#maincontents > div ul li')

    if not elements:
        elements = soup.select('ul li')

    expansion = defaultdict(list)

    for element in elements:
        classes = set()

        for class_ in element['class']:
            classes.add(class_)

        title = 'titlebg' in classes

        classes.discard('titlebg')
        classes.discard('cellbg')

        assert len(classes) == 1

        if not title:
            class_ = classes.pop()
            expansion[class_].append(element.text.strip())

    df = pd.DataFrame(expansion)

    return df


def main():
    tqdm.pandas()

    df = pd.read_csv(stdin, index_col=0, dtype=str)
    expansions = df.progress_apply(expand, axis=1)
    indices = df.index.repeat(list(map(len, expansions)))
    df = df.loc[indices].reset_index(drop=True)
    df = pd.concat(
        [
            df.drop(columns='raw'),
            pd.concat(list(expansions), ignore_index=True),
        ],
        axis=1,
    )

    df.to_csv(stdout)


if __name__ == '__main__':
    main()
