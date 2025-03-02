import os
import pathlib

from utils.statbotics_utils import (
    download_statbotics_matches,
    download_statbotics_event_teams,
)
from utils.tba_utils import download_tba_event_matches


def download_external_data(event):
    """
    Downloads the external data (Statbotics, TBA, etc) for a specific event
    :param event: The event key
    """
    script_directory = pathlib.Path(__file__).resolve().parent

    data_directory = script_directory / "data" / event

    statbotics_matches_file = data_directory / "statbotics_matches.json"
    download_statbotics_matches(event, statbotics_matches_file)

    statbotics_teams_file = data_directory / "statbotics_teams.json"
    download_statbotics_event_teams(event, statbotics_teams_file)

    tba_matches_file = data_directory / "tba_matches.json"
    download_tba_event_matches(event, tba_matches_file)


if __name__ == "__main__":

    download_external_data("2025txwac")
