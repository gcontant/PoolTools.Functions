import logging
import requests
import json
import datetime
import bs4
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    today = datetime.date.today().strftime("%m%d%Y")
    date = req.params.get('date')
    if not date:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            date = req_body.get('date')

    if not date:
        date = today

    url = f"https://www.capfriendly.com/ajax/trades?season=2023&min-players=1&date={date}-{today}"

    response = requests.request("GET", url, headers={}, data={})

    data = json.loads(response.text)
    resultCount = data["data"]["result_count"]
    
    if resultCount > 0:
        teams = {
            "Anaheim Ducks": "ANA",
            "Arizona Coyotes": "ARI",
            "Boston Bruins": "BOS",
            "Buffalo Sabres": "BUF",
            "Calgary Flames": "CGY",
            "Carolina Hurricanes": "CAR",
            "Chicago Blackhawks": "CHI",
            "Colorado Avalanche": "COL",
            "Columbus Blue Jackets": "CBJ",
            "Dallas Stars": "DAL",
            "Detroit Red Wings": "DET",
            "Edmonton Oilers": "EDM",
            "Florida Panthers": "FLA",
            "Los Angeles Kings": "LAK",
            "Minnesota Wild": "MIN",
            "Montreal Canadiens": "MTL",
            "Nashville Predators": "NAS",
            "New Jersey Devils": "NJD",
            "New York Islanders": "NYI",
            "New York Rangers": "NYR",
            "Ottawa Senators": "OTT",
            "Philadelphia Flyers": "PHI",
            "Pittsburgh Penguins": "PIT",
            "San Jose Sharks": "SJS",
            "Seattle Kraken": "SEA",
            "St. Louis Blues": "STL",
            "Tampa Bay Lightning": "TBL",
            "Toronto Maple Leafs": "TOR",
            "Vancouver Canucks": "VAN",
            "Vegas Golden Knights": "VGK",
            "Washington Capitals": "WSH",
            "Winnipeg Jets": "WIN"
        }
        content = bs4.BeautifulSoup(data["data"]["html"])

        links = content.find_all("a",attrs={'class': "hid_anc"})
        spans = content.find_all("span",attrs={'class': None})

        for i in range(0,len(spans)-1,2):
            x=links[i].text.find("Acquire")
            team1=links[i].text[0:x-1]
            x=links[i+1].text.find("Acquire")
            team2=links[i+1].text[0:x-1]

            logging.info(f"{team1} trade {spans[i].text} to {team2}, for {spans[i+1].text}")

            logging.info(f"{spans[i].text}{teams[team1]} becomes {spans[i].text}{teams[team2]}")
            logging.info(f"{spans[i+1].text}{teams[team2]} becomes {spans[i+1].text}{teams[team1]}")
            # TODO Send request to trade player
    return func.HttpResponse(
        f"Found {resultCount} new trade",
        status_code=200
    )
