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

  Can be used in interactive mode without passing any arguments.

Options:
  -d, --destinations FILE         Path to the CSV files containing your
                                  destination names. It should contain 1
                                  column called destination.  [required]
  -m, --modifiers FILE            Path to the CSV files containing your
                                  modifiers. It should contain 1 column called
                                  kw.  [required]
  -o, --out PATH                  Path where to write the output of the
                                  script. It can be a directory or a file.
                                  Output will be of CSV format.  [required]
  --max-rows INTEGER              Max number of rows in the output file(s). If
                                  total number of rows is greater that
                                  max_rows, then the script will create
                                  multiple files.
  --mode [destination_first|modifier_first|both]
                                  Mode in which the script should work:
                                  'destination_first' will put destinations
                                  first and modifiers after. 'modifier_first'
                                  is the opposite. 'both' will include both
                                  combinations one after another.
  --help                          Show this message and exit.
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

- add check for CSVs
- add checks on files have only 1 column
- add rename on file column to support files with other name
- handle files with no headers
- add check for left and right files not equal
- add github pages with docs and link to pypi
