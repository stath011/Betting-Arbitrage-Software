from flask import Flask, render_template
import requests

app = Flask(__name__)

API_KEY = '9d09242581494c6747226feba14d7317'
SPORT = 'upcoming'
REGIONS = 'au'  # uk | us | eu | au. Multiple can be specified if comma delimited
# h2h | spreads | totals. Multiple can be specified if comma delimited
MARKETS = 'h2h', 'spreads'
ODDS_FORMAT = 'decimal'  # decimal | american
DATE_FORMAT = 'iso'  # iso | unix

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', timeout=10,
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

num = 0
data = []
headers = ['time', 'league', 'sport', 'key', 'bookmaker', 'type',
           'team1', 'price1', 'team2', 'price2', 'draw', 'price']

bookie_info = []

if odds_response.status_code != 200:
    print(
        f'Failed to get odds: status_code{odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    events = 'Number of events:', len(odds_json)

    for x in odds_json:
        sportkey = ([x['sport_key']])
        data.append(sportkey)
        data[data.index(sportkey)].append(x['sport_title'])
        data[data.index(sportkey)].append(x['commence_time'])
        for z in x['bookmakers']:
            title = [z['title']]
            if title != ['Betfair']:
                bookie_info.append(title)
                bookie_info[bookie_info.index(title)].insert(0, str(num))
            else:
                break
            for n in z['markets']:
                bookie_info[bookie_info.index(title)].append(n['key'])
                for b in n['outcomes']:
                    bookie_info[bookie_info.index(title)].append(b['name'])
                    bookie_info[bookie_info.index(title)].append(b['price'])
        num += 1

    for alp in bookie_info:
        for mapa in data[int(alp[0])]:
            alp.insert(0, mapa)

print(bookie_info)


@app.route('/')
def hello():
    return render_template('index.html', headers=headers, bookie_info=bookie_info)


if __name__ == '__main__':
    app.debug = True
    app.run()
