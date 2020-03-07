import click
import click_completion
import pandas as pd

click_completion.init()


def combine_keywords(
    destinations="../data/destinations.csv",
    modifiers="../data/modifiers.csv",
    output="../data/output.csv",
):
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
    df.to_csv(output, index=False)
    pass


@click.command()
@click.option("--destinations", "-d", type=click.Path(exists=True, dir_okay=False))
@click.option("--modifiers", "-m", type=click.Path(exists=True, dir_okay=False))
@click.option("--out", "-o", type=click.Path(dir_okay=False, writable=True))
def cli(destinations, modifiers, out):
    """🥒   Combine Keywords from files"""
    combine_keywords(destinations=destinations, modifiers=modifiers, output=out)
