
import requests

def __make_request(url: str, org_key: str) -> bytes:

    cookies = {
        "org_key": org_key,
    }
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7",
    }

    response = requests.get(url, cookies=cookies, headers=headers)

    return response.content


def request_scout_radioz_match_scouting(org_key):
    url = "https://scoutradioz.com/reports/exportdata?type=matchscouting"

    return __make_request(url, org_key)


def download_scout_radioz_match_scouting(org_key, output_file):
    content = request_scout_radioz_match_scouting(org_key)

    with open(output_file, 'wb') as f:
        f.write(content)


def request_scout_radioz_pit_scouting(org_key):
    url = "https://scoutradioz.com/reports/exportdata?type=pitscouting"

    return __make_request(url, org_key)


def download_scout_radioz_pit_scouting(org_key, output_file):
    content = request_scout_radioz_pit_scouting(org_key)

    with open(output_file, 'wb') as f:
        f.write(content)
