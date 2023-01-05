import requests
# base_url = 'https://api.the-odds-api.com'
API_KEY = '457674bb226d52b275f1a999d064b41a'
SPORT = 'upcoming'
REGIONS = 'au'  # uk | us | eu | au. Multiple can be specified if comma delimited
# h2h | spreads | totals. Multiple can be specified if comma delimited
MARKETS = 'h2h', 'spreads'
ODDS_FORMAT = 'decimal'  # decimal | american
DATE_FORMAT = 'iso'  # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code != 200:
    print(
        f'Failed to get odds: status_code{odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    print('Number of events:', len(odds_json))
    for x in odds_json:
        print(x)
    for x in odds_json:
        a = f"league: {x['sport_key']}"
        b = f"sport title: {x['sport_title']}"
        c = f"commence time: {x['commence_time']}"

        print(a, b, c)

        for bookmaker in range(len(x['bookmakers'])):
            print(f"bookmaker: {x['bookmakers'][bookmaker]['title']}")
            print(f"market: {x['bookmakers'][bookmaker]['markets'][0]['key']}")
            print(
                f"team1: {x['bookmakers'][bookmaker]['markets'][0]['outcomes'][0]['name']}")
            print(
                f"odds: {x['bookmakers'][bookmaker]['markets'][0]['outcomes'][0]['price']}")
            print(
                f"team2: {x['bookmakers'][bookmaker]['markets'][0]['outcomes'][1]['name']}")
            print(
                f"odds: {x['bookmakers'][bookmaker]['markets'][0]['outcomes'][1]['price']}")

            try:
                draw = f"{x['bookmakers'][bookmaker]['markets'][0]['outcomes'][2]['name']}"
                odd = f"{x['bookmakers'][bookmaker]['markets'][0]['outcomes'][2]['price']}"
            except:  # pylint: disable=W0702
                draw = "null"
                odd = "null"

            print(draw)
            print("odd: " + odd)

    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])
