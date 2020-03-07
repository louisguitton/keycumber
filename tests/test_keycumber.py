from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from keycumber import combine_keywords, write_keywords


@pytest.fixture
def destinations():
    return pd.DataFrame(["Uluru", "Sydney"], columns=["destination"])


@pytest.fixture
def modifiers():
    return pd.DataFrame(["vol", "hotel"], columns=["kw"])


@pytest.mark.parametrize(
    "mode,expected",
    [
        (
            "destination_first",
            pd.Series(
                ["Uluru vol", "Uluru hotel", "Sydney vol", "Sydney hotel"],
                name="output",
            ),
        ),
        (
            "modifier_first",
            pd.Series(
                ["vol Uluru", "hotel Uluru", "vol Sydney", "hotel Sydney"],
                name="output",
            ),
        ),
        (
            "both",
            pd.Series(
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
    "max_rows,expected_path,expected_file_count",
    [(np.inf, "data/output.csv", 1), (2, "data/output", 4), (3, "data/output", 3)],
)
def test_write_keywords(max_rows, expected_path, expected_file_count):
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
    output = write_keywords(out_df=out_df, output="data/output.csv", max_rows=max_rows)
    # Assert
    assert Path(expected_path) == output
    assert expected_file_count == len(list(Path(expected_path).glob("*"))) + Path(expected_path).is_file()
