import json
from pathlib import Path
import pandas as pd
from typing import List, Dict, Any


############################################
# Statbotics Matches
############################################
def download_statbotics_matches(event: str, output_path: Path, quals_only=True):
    """
    Queries the statbotics api for event info, and saves the json file to disk.
    :param event: The event key (i.e. 2024paca)
    :param output_path: The path to save the json to
    :param quals_only: If true, only data from qualification matches will be saved
    """
    import statbotics

    sb = statbotics.Statbotics()

    elims = False if quals_only else None
    data = sb.get_matches(event=event, elims=elims)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)


def load_statbotics_matches(filename: Path) -> pd.DataFrame:
    """
    Loads the match information from a file on disk, potentially pre-calculating helpful aggregate data
    :param filename: The filename to load
    :return: The data in the form of a dataframe
    """
    with open(filename, "r") as f:
        json_data = json.load(f)

    return statbotics_matches_json_to_dataframe(json_data)


def statbotics_matches_json_to_dataframe(json_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Converts the json data into a dataframe
    :param json_data: The json dictionary
    :return: The data frame
    """

    # There is nothing intersting to precalculate, so we just shove the json into a dataframe
    return pd.DataFrame(json_data)


############################################
# Statbotics Events
############################################
def download_statbotics_event_teams(event: str, output_path: Path):
    """
    Queries the API and downloads event data and saves the json response to disk.
    :param event: The event key (i.e. 2024paca)
    :param output_path: The location on disk to save the file
    """
    # import statbotics

    # sb = statbotics.Statbotics()
    # data = sb.get_event(event=event)
    #
    # with open(output_path, "w") as f:
    #     json.dump(data, f, indent=4)

    import requests

    url = f"https://api.statbotics.io/v3/team_events?event={event}"

    response = requests.get(url)

    with open(output_path, "w") as f:
        as_json = response.json()
        json.dump(as_json, f, indent=4)


def load_statbotics_teams(filename: Path):
    """
    Loads the json data for teams at an event from disk
    :param filename: The path to the cached json file.
    :return: The dataframe representing the json and some helpful precalculated aggregate data
    """
    with open(filename, "r") as f:
        json_data = json.load(f)

    return statbotics_teams_json_to_dataframe(json_data)


def statbotics_teams_json_to_dataframe(json_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Converts teams into a dataframe, adding in some helpful precalculated aggregate data.
    :param json_data: The json dictionary
    :return: The data frame
    """
    output = pd.DataFrame(json_data)
    output["Auto+Endgame EPA"] = output["endgame_epa_end"] + output["auto_epa_end"]

    return output


############################################
# Utilities
############################################
def __get_alliance_teams_in_match(
        match_data: pd.DataFrame, alliance_color: str, num_teams: int
) -> List[int]:
    """
    Zips the teams on an alliance into a single list.

    The dataframe contains (likely) contains 3 columns for the alliance, ie
        Match Number | R1 | R2 | R3, ... |

    It can be helpful to have these teams zipped into a list, i.e. [R1, R2, R3]. This
    function runs this zipping and pulls out the data for an alliance in the match

    :param match_data: A dataframe representing a single match
    :param num_teams: The number of teams expected on an alliance.
    :return: The list of teams, as integers
    """
    teams = []

    for i in range(num_teams):
        x = match_data[f"{alliance_color}_{i + 1}"].values[0]
        teams.append(x)

    return teams


def get_red_teams_in_match(match_data: pd.DataFrame, num_teams=3) -> List[int]:
    """
    Zips red alliance teams into a list. See :func:`__get_alliance_teams_in_match`

    :param match_data: A dataframe representing a single match
    :param num_teams: The number of teams expected on an alliance.
    :return: The list of teams, as integers
    """
    return __get_alliance_teams_in_match(match_data, "red", num_teams)


def get_blue_teams_in_match(match_data: pd.DataFrame, num_teams: int = 3) -> List[int]:
    """
    Zips red alliance teams into a list. See :func:`__get_alliance_teams_in_match`

    :param match_data: A dataframe representing a single match
    :param num_teams: The number of teams expected on an alliance.
    :return: The list of teams, as integers
    """
    return __get_alliance_teams_in_match(match_data, "blue", num_teams)


def get_matches_for_team(event_data: pd.DataFrame, team_number: int) -> pd.DataFrame:
    """
    Queries the data frame for all matches that a given team is in.

    :param event_data: The dataframe for a whole event
    :param team_number: The team number to search for
    :return: A dataframe containing this teams matches
    """
    output = event_data[
        (event_data["red_1"] == team_number)
        | (event_data["red_2"] == team_number)
        | (event_data["red_3"] == team_number)
        | (event_data["blue_1"] == team_number)
        | (event_data["blue_2"] == team_number)
        | (event_data["blue_3"] == team_number)
        ]
    return output
