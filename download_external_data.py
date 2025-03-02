import os
import pathlib
import requests


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

    # statbotics_matches_file =
    # download_statbotics_matches(event, data_directory / "statbotics_matches.json")
    #
    # statbotics_teams_file =
    # download_statbotics_event_teams(event, data_directory / "statbotics_teams.json")
    #
    # tba_matches_file =
    # download_tba_event_matches(event, data_directory / "tba_matches.json")

    org_key = "frc8749"
    download_scout_radioz(org_key, data_directory / "scouted.csv")


if __name__ == "__main__":

    download_external_data("2025txwac")
