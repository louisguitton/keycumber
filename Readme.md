# 🥒keycumber

> A Keyword Combinator to make Inbound Marketer's life better.

## Setup

```sh
pip install keycumber
```

## Example

```sh
keycumber --help
keycumber -d data/destinations.csv -m data/modifiers.csv -o data/output/
```

## Todo

- add nice click descriptions
- add order = pois_first / modifiers_first / both
- add batch
    if not specified, output everything in one file. if specified, default to 700 and creates files of 700 rows in folder
- add checks on files have only 1 column
- add rename on file column to support files with other name
- handle files with no headers
- add check for left and right files not equal
