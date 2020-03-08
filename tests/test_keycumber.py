from pathlib import Path

from click.testing import CliRunner
import numpy as np
import pandas as pd
import pytest

from keycumber import cli, combine_keywords, write_keywords


@pytest.fixture
def destinations():
    return pd.read_csv("data/destinations.csv", header=None, names=["column"])


@pytest.fixture
def modifiers():
    return pd.read_csv("data/modifiers.csv", header=None, names=["column"])


@pytest.mark.parametrize(
    "mode,expected",
    [
        (
            "destination_first",
            pd.read_csv(
                "data/output_destination_first.csv",
                squeeze=True,
                header=None,
                names=["output"],
            ),
        ),
        (
            "modifier_first",
            pd.read_csv(
                "data/output_modifier_first.csv",
                squeeze=True,
                header=None,
                names=["output"],
            ),
        ),
        (
            "both",
            pd.read_csv(
                "data/output_both.csv", squeeze=True, header=None, names=["output"]
            ),
        ),
    ],
)
def test_combine_keywords_destination_first(destinations, modifiers, mode, expected):
    # Exercise
    out_series = combine_keywords(destinations, modifiers, mode=mode)
    # Assert
    pd.testing.assert_series_equal(expected, out_series)


@pytest.mark.parametrize(
    "max_rows,given_path,expected_path,expected_file_count",
    [
        (np.inf, "data/output.csv", "data/output.csv", 1),
        (np.inf, "data/output/", "data/output/out.csv", 1),
        (np.inf, "data/output/deep/", "data/output/deep/out.csv", 1),
        (2, "data/output.csv", "data/output", 4),
        (3, "data/output/", "data/output", 3),
    ],
)
def test_write_keywords(max_rows, given_path, expected_path, expected_file_count):
    # Prepare
    out_df = pd.Series(
        [
            "Uluru vol",
            "Uluru hotel",
            "Sydney vol",
            "Sydney hotel",
            "vol Uluru",
            "hotel Uluru",
            "vol Sydney",
            "hotel Sydney",
        ],
        name="output",
    )
    # Exercise
    output = write_keywords(out_df=out_df, output=given_path, max_rows=max_rows)
    # Assert
    assert Path(expected_path) == output
    assert (
        expected_file_count
        == len(list(Path(expected_path).glob("*"))) + Path(expected_path).is_file()
    )


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_cli(cli_runner):
    result = cli_runner.invoke(
        cli,
        [
            "-d",
            "data/destinations.csv",
            "-m",
            "data/modifiers.csv",
            "-o",
            "data/output.csv",
        ],
    )

    assert result.exit_code == 0
    assert "Keywors successfully combined" in result.output


def test_not_csv_is_caught(cli_runner):
    result = cli_runner.invoke(
        cli,
        [
            "-d",
            "data/wrong_input.json",
            "-m",
            "data/modifiers.csv",
            "-o",
            "data/output.csv",
        ],
    )

    assert type(result.exception) == pd.errors.ParserError
