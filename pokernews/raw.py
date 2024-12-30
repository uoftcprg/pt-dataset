from sys import argv, stdin, stdout
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
import pandas as pd

URL = 'https://www.pokernews.com'
HREF_KEY = argv[1]
URL_PATH = argv[2]


def get_html(url_path):
    url = urljoin(URL, url_path)
    html = get(url).text

    return html


def get_raw(row):
    url_path = urljoin(row[HREF_KEY], URL_PATH)
    html = get_html(url_path)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find('script', {'data-chipcountsreact-target': 'jsonData'})
    raw = element.text

    return raw


def main():
    tqdm.pandas()

    df = pd.read_csv(stdin, index_col=0, dtype=str)
    raws = df.progress_apply(get_raw, axis=1)
    df['raw'] = raws

    df.to_csv(stdout)


if __name__ == '__main__':
    main()
