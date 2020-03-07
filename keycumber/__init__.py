from pathlib import Path

import click
import click_completion
import pandas as pd

click_completion.init()


def combine_keywords(destinations, modifiers, output):
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

    # TODO: only one column, batch by 700 rows maximum

    Path(output).mkdir(parents=True, exist_ok=True)
    if Path(output).is_dir():
        output_path = Path(output) / "out.csv"
    else:
        output_path = output
    df[["output"]].to_csv(output_path, index=False)
    click.secho(
        "Keywors successfully combined. Output stored in {}".format(output_path),
        fg="green",
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
def cli(destinations, modifiers, out):
    """🥒   Combine Keywords from CSV files."""
    combine_keywords(destinations=destinations, modifiers=modifiers, output=out)
