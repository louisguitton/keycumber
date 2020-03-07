from pathlib import Path

import click
import click_completion
import numpy as np
import pandas as pd

click_completion.init()


def combine_keywords(destinations: str, modifiers: str, output: str, max_rows: int):
    destinations = pd.read_csv(destinations)
    modifiers = pd.read_csv(modifiers)

    # TODO: add checks on files have only one column
    # TODO: add rename on file column to conform with expectations

    index = pd.MultiIndex.from_product(
        [destinations.destination.tolist(), modifiers.kw.tolist()],
        names=["destinations", "modifiers"],
    )
    df = pd.DataFrame(index=index).reset_index()
    df["output"] = df.destinations + " " + df.modifiers
    # df['output_2'] = df.modifiers + ' ' + df.destinations
    out_df = df[["output"]]

    Path(output).mkdir(parents=True, exist_ok=True)

    # Add batching logic to create files with less rows than max_rows
    if max_rows:
        number_of_chunks = len(df) // max_rows + 1
    else:
        number_of_chunks = 1

    output_dir = None
    output_file = None
    if number_of_chunks == 1:
        if Path(output).is_dir():
            output_file = Path(output) / "out.csv"
        else:
            output_file = output

        out_df.to_csv(output_file, index=False)
    else:
        if Path(output).is_dir():
            output_dir = output
        else:
            output_dir = Path(output).parent / Path(output).stem

        for id, df_i in enumerate(np.array_split(out_df, number_of_chunks)):
            df_i.to_csv(Path(output_dir) / f"out_{id}.csv", index=False)

    click.secho(
        "Keywors successfully combined. Output stored in {}".format(output_dir or output_file),
        fg="green",
        # https://click.palletsprojects.com/en/7.x/api/#click.style
    )


@click.command()
@click.option(
    "--destinations",
    "-d",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    prompt="Path to destination CSV",
    help="Path to the CSV files containing your destination names. It should contain 1 column called destination.",
)
@click.option(
    "--modifiers",
    "-m",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    prompt="Path to modifiers CSV",
    help="Path to the CSV files containing your modifiers. It should contain 1 column called kw.",
)
@click.option(
    "--out",
    "-o",
    required=True,
    type=click.Path(dir_okay=True, writable=True),
    prompt="Path to output CSV or directory",
    help="Path where to write the output of the script. It can be a directory or a file. Output will be of CSV format.",
)
@click.option(
    "--max-rows",
    required=False,
    type=int,
    prompt="Max number of rows to include in the output file(s).",
    default=None,
    help="Max number of rows in the output file(s). If total number of rows is greater that max_rows, then the script will create multiple files.",
)
def cli(destinations, modifiers, out, max_rows):
    """🥒   Combine Keywords from CSV files."""
    combine_keywords(destinations=destinations, modifiers=modifiers, output=out, max_rows=max_rows)
