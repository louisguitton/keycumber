# 🥒keycumber

> A Keyword Combinator to make Inbound Marketer's life better.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/keycumber?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/keycumber?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/keycumber?style=flat-square)
![Travis (.org)](https://img.shields.io/travis/louisguitton/keycumber?style=flat-square)
![Code Climate coverage](https://img.shields.io/codeclimate/coverage/louisguitton/keycumber?style=flat-square)

Put your destinations and modifiers into different CSV files.
Run `keycumber` and all keyword combinations will be generated for you and stored in CSV files.

## Installation

```sh
pip install keycumber
```

More info [on Pypi](https://pypi.org/project/keycumber/).

## Usage example

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

- add check that input files are CSVs
- add checks on input files have only 1 column
- add rename on input file column to support files with other names
- handle files with no headers
- add check to make sure for destination file and modifier file are not equal
