# 🥒keycumber

> A Keyword Combinator to make Inbound Marketer's life better.

## Setup

```sh
pip install keycumber
```

## Usage

Get help

```sh
$ keycumber --help
Usage: keycumber [OPTIONS]

  🥒   Combine Keywords from CSV files.

Options:
  -d, --destinations FILE  Path to the CSV files containing your destination
                           names. It should contain 1 column called
                           destination.  [required]
  -m, --modifiers FILE     Path to the CSV files containing your modifiers. It
                           should contain 1 column called kw.  [required]
  -o, --out PATH           Path where to write the output of the script. It
                           can be a directory or a file. Output will be of CSV
                           format.  [required]
  --max-rows INTEGER       Max number of rows in the output file(s). If total
                           number of rows is greater that max_rows, then the
                           script will create multiple files.
  --help                   Show this message and exit.
```

Interactive mode

```sh
keycumber
```

Pass the filepaths directly

```sh
keycumber -d data/destinations.csv -m data/modifiers.csv -o data/output/
```

## Todo

- add order = pois_first / modifiers_first / both
- add check for CSVs
- add checks on files have only 1 column
- add rename on file column to support files with other name
- handle files with no headers
- add check for left and right files not equal
- add github pages with docs and link to pypi
