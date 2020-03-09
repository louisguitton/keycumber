from pathlib import Path

import click
import click_completion
import numpy as np
import pandas as pd

click_completion.init()


def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob("*"):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    if pth.exists():
        pth.rmdir()


def combine_keywords(
    destinations: pd.DataFrame, modifiers: pd.DataFrame, mode: str
) -> pd.Series:
    index = pd.MultiIndex.from_product(
        [destinations.column.tolist(), modifiers.column.tolist()],
        names=["destinations", "modifiers"],
    )
    df = pd.DataFrame(index=index).reset_index()
    if mode == "destination_first":
        df["output"] = df.destinations + " " + df.modifiers
    elif mode == "modifier_first":
        df["output"] = df.modifiers + " " + df.destinations
    elif mode == "both":
        df["destination_first"] = df.destinations + " " + df.modifiers
        df["modifier_first"] = df.modifiers + " " + df.destinations
        df = pd.concat(
            [
                df["destination_first"].rename("output"),
                df["modifier_first"].rename("output"),
            ],
            axis=0,
            ignore_index=True,
        ).to_frame()

    return df.output


def write_keywords(out_df: pd.Series, output: str, max_rows: float,) -> Path:
    # Add batching logic to create files with less rows than max_rows
    number_of_chunks = int(len(out_df) // max_rows)
    if len(out_df) % max_rows:
        number_of_chunks += 1

    output_dir = None
    output_file = None
    if number_of_chunks == 1:
        if not Path(output).suffix:
            output_file = Path(output) / "out.csv"
        else:
            output_file = output

        if not Path(output_file).exists():
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        out_df.to_csv(output_file, index=False, header=False)
    else:
        if Path(output).is_dir():
            output_dir = output
        else:
            output_dir = Path(output).parent / Path(output).stem

        rm_tree(output_dir)
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for id, df_i in enumerate(np.array_split(out_df, number_of_chunks)):
            df_i.to_csv(Path(output_dir) / f"out_{id}.csv", index=False, header=False)

    return Path(output_dir or output_file)


@click.command()
@click.option(
    "--destinations",
    "-d",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    prompt="Path to destination CSV",
    help="Path to the CSV files containing your destination names. It should contain 1 column with no headers.",
)
@click.option(
    "--modifiers",
    "-m",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    prompt="Path to modifiers CSV",
    help="Path to the CSV files containing your modifiers. It should contain 1 column with no headers.",
)
@click.option(
    "--out",
    "-o",
    required=True,
    type=click.Path(dir_okay=True, writable=True),
    prompt="Path to output CSV or directory",
    help="Path where to write the output of the script. It can be a directory or a file. Output will be of CSV format, with 1 column without headers.",
)
@click.option(
    "--max-rows",
    required=False,
    type=float,
    prompt="Max number of rows to include in the output file(s).",
    default=np.inf,
    help="Max number of rows in the output file(s). If total number of rows is greater that max_rows, then the script will create multiple files.",
)
@click.option(
    "--mode",
    required=False,
    type=click.Choice(
        ["destination_first", "modifier_first", "both"], case_sensitive=False
    ),
    prompt="Mode",
    default="destination_first",
    help="Mode in which the script should work: 'destination_first' will put destinations first and modifiers after. 'modifier_first' is the opposite. 'both' will include both combinations one after another.",
)
def cli(destinations, modifiers, out, max_rows, mode):
    """🥒   Combine Keywords from CSV files.

    Can be used in interactive mode without passing any arguments.
    """
    try:
        destinations = pd.read_csv(destinations, header=None).rename(
            columns={0: "column"}
        )
        modifiers = pd.read_csv(modifiers, header=None).rename(columns={0: "column"})

        out_df = combine_keywords(
            destinations=destinations, modifiers=modifiers, mode=mode,
        )
        path = write_keywords(out_df, output=out, max_rows=max_rows,)
        click.secho(
            f"Keywors successfully combined. Output stored in {path}",
            fg="green",
            # https://click.palletsprojects.com/en/7.x/api/#click.style
        )
    except pd.errors.ParserError as e:
        click.secho(
            "Error: Make sure you're passing CSV files to -d and -m",
            fg="red"
            # https://click.palletsprojects.com/en/7.x/api/#click.style
        )
        raise e
    except Exception as e:
        click.secho(
            "Unknown error, please open a ticket https://github.com/louisguitton/keycumber/issues",
            fg="red"
            # https://click.palletsprojects.com/en/7.x/api/#click.style
        )
        raise e
