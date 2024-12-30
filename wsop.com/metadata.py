from collections import defaultdict
from sys import stdout

from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
import pandas as pd

COMPETITIONS_URL = 'https://www.wsop.com/tournaments/results/'
TOURNAMENTS_URL = 'https://www.wsop.com/tournaments/GetTournaments.aspx?aid={}'
EVENTS_URL = 'https://www.wsop.com/tournaments/GetEvents.aspx?grid={}'


def get_competitions():
    html = get(COMPETITIONS_URL).text
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('.competition > select option')
    competitions = []

    for element in elements:
        competition = {'aid': element['value'], 'competition': element.text}

        competitions.append(competition)

    return competitions


def get_options(url, value_key, text_key):
    html = get(url).text.replace('</options>', '</option>')
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('option')
    options = []

    for element in elements:
        option = {value_key: element['value'], text_key: element.text}

        options.append(option)

    return options


def get_tournaments(aid):
    return get_options(TOURNAMENTS_URL.format(aid), 'grid', 'tournament')


def get_events(aid):
    return get_options(EVENTS_URL.format(aid), 'tid', 'event')


def update(data, *args):
    for arg in args:
        for key, value in arg.items():
            data[key].append(value)


def main():
    data = defaultdict(list)
    competitions = get_competitions()

    for competition in tqdm(competitions):
        tournaments = get_tournaments(competition['aid'])

        for tournament in tqdm(tournaments, leave=False):
            events = get_events(tournament['grid'])

            for event in tqdm(events, leave=False):
                update(data, competition, tournament, event)

    df = pd.DataFrame(data)

    df.to_csv(stdout)


if __name__ == '__main__':
    main()
