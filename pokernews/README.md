# PokerNews

A dataset of tournaments on [PokerNews](https://www.pokernews.com/). This dataset was last updated on December 30, 2024.

To contribute, please create a pull request or an issue at the accompanying [GitHub repository](https://github.com/uoftcprg/pt-dataset).

Contents:

- Chip counts of 3,610 events.
- Payouts of 4,024 events.

## Instructions

Get metadata.

```console
python metadata.py > data/metadata.csv
python metadata2.py < data/metadata.csv > data/metadata2.csv
```

Get chip counts.

```console
python raw.py "day_href" "chips.htm" < data/metadata2.csv > data/raw-chips.csv
python table.py < data/raw-chips.csv > data/chips.csv
```

Get payouts.

```console
python raw.py "event_href" "payouts.htm" < data/metadata.csv > data/raw-payouts.csv
python table.py < data/raw-payouts.csv > data/payouts.csv
```
