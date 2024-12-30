# WSOP.com

A dataset of WSOP-affiliated tournaments on [WSOP.com](https://www.wsop.com/). This dataset was last updated on December 26, 2024.

To contribute, please create a pull request or an issue at the accompanying [GitHub repository](https://github.com/uoftcprg/pt-dataset).

Contents:

- [Results](https://www.wsop.com/tournaments/results/) of 9,958 events.
- [Prize pool (payouts)](https://www.wsop.com/tournaments/payouts/) of 5,018 events.
- [Chip counts](https://www.wsop.com/tournaments/chipcounts/) of 1,809 events.

## Instructions

Get metadata.

```console
python metadata.py > data/metadata.csv
```

Get results.

```console
python raw.py "https://www.wsop.com/tournaments/results/printresults.aspx?aid={}&grid={}&tid={}" < data/metadata.csv > data/raw-results.csv
python table.py < data/raw-results.csv > data/results.csv
```

Get prize pools (payouts).

```console
python raw.py "https://www.wsop.com/tournaments/payouts/print/?aid={}&grid={}&tid={}" < data/metadata.csv > data/raw-payouts.csv
python table.py < data/raw-payouts.csv > data/payouts.csv
```

Get chip counts. 

```console
python raw.py "https://www.wsop.com/tournaments/chipcounts/?aid={}&grid={}&tid={}" < data/metadata.csv > data/raw-chipcounts.csv
python raw2.py "https://www.wsop.com/tournaments/chipcounts/?aid={}&grid={}&tid={}&dayof={}&curpage={}" < data/raw-chipcounts.csv > data/raw2-chipcounts.csv
python table.py < data/raw2-chipcounts.csv > data/chipcounts.csv
```
