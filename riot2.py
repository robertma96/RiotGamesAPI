import requests
import json
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
api_key = config.get('auth', 'api_key')
class Summoner:
    def __init__(self, summonerName, region, accountID, summonerID, leaguePosition, winRate):
        self.summonerName = summonerName
        self.region = region
        self.accountID = accountID
        self.summonerID = summonerID
        self.leaguePosition = leaguePosition
        self.winRate = winRate

def new_summoner():
    region = input('region: ')
    summoner_name = input('summoner name: ')

    def f(region):
        return {
            'eune': 'eun1',
            'EUNE': 'eun1',
            'EUW': 'euw1',
            'NA': 'na1'
        }[region]

    def summonerid():
        link = "https://" + f(region) + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + \
               summoner_name.replace(" ", "%20") + "?api_key=" + api_key
        response = requests.get(link)
        if response.status_code == 200:
            obiect = json.loads(response.content.decode('utf-8'))
            id_simple = obiect['id']
            return id_simple
        else:
            print(response.status_code)


    def accountid():
        link = "https://" + f(region) + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + \
               summoner_name.replace(" ", "%20") + "?api_key=" + api_key
        response = requests.get(link)
        if response.status_code == 200:
            obiect = json.loads(response.content.decode('utf-8'))
            accountId = obiect['accountId']
            return accountId
        else:
            print(response.status_code)

    accountID = accountid()
    summonerID = summonerid()

    def rank():
        global winrate
        my_summoner_id = summonerid()
        link = "https://" + f(region) + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(
            my_summoner_id) + \
               "?api_key=" + api_key
        response = requests.get(link)
        if response.status_code == 200:
            obiect = json.loads(response.content.decode('utf-8'))
            wins = obiect[0]['wins']
            losses = obiect[0]['losses']
            winrate = round((wins / (wins + losses)) * 100, 0)
            return obiect[0]['tier'] + " " + obiect[0]['rank'] + " " + str(obiect[0]['leaguePoints']) + "LP"
        else:
            print(response.status_code)


    leaguePosition = rank()
    winRate = winrate

    summoner = Summoner(summoner_name, region, accountID, summonerID, leaguePosition, winRate)

    return summoner.leaguePosition
    #print(summoner.summonerName + "\n" + str(summoner.leaguePosition) + " " + "\n" + str(int(summoner.winRate)) + "%")

print(new_summoner())