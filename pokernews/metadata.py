from collections import defaultdict
from sys import stdout
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
import pandas as pd

URL = 'https://www.pokernews.com'
TOURS_URL_PATH = '/tours/'
SCHEDULE_URL_PATH = 'schedule.htm'


def get_html(url_path):
    url = urljoin(URL, url_path)
    html = get(url).text

    return html


def get_links(html, selector, key):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select(selector)
    links = []

    for element in elements:
        link = {
            key: element.text.strip(),
            f'{key}_href': element['href'],
        }

        links.append(link)

    return links


def get_tours():
    html = get_html(TOURS_URL_PATH)
    links = get_links(html, '.tourList > a', 'tour')

    assert links

    return links


def get_years(tour):
    html = get_html(tour['tour_href'])
    links = get_links(html, '.tourHub__years > dd a', 'year')

    assert links

    return links


def get_tournaments(year):
    html = get_html(year['year_href'])
    links = get_links(html, 'a.tourTitle', 'tournament')

    return links


def get_events(tournament):
    url_path = tournament['tournament_href']
    html = get_html(url_path)
    url_path = urljoin(url_path, SCHEDULE_URL_PATH)

    if url_path in html:
        tournament['tournament_href'] = url_path
        html = get_html(tournament['tournament_href'])

    links = get_links(html, 'a.tourTitle', 'event')

    return links


def update(data, *args):
    for arg in args:
        for key, value in arg.items():
            data[key].append(value)


def main():
    data = defaultdict(list)

    for tour in tqdm(get_tours()):
        for year in tqdm(get_years(tour), leave=False):
            for tournament in tqdm(get_tournaments(year), leave=False):
                for event in tqdm(get_events(tournament), leave=False):
                    update(data, tour, year, tournament, event)

    df = pd.DataFrame(data)

    df.to_csv(stdout)


if __name__ == '__main__':
    main()
