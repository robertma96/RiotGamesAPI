import json
import requests
import time
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
api_key = config.get('auth', 'api_key')

region = 'EUNE'
summoner_name = 'Jon Snow'

lista_campioni = []
lista_winrate_campioni = []
lista_champs_id = []
update = None


def f(region):
    return {
        'EUNE': 'eun1',
        'EUW': 'euw1',
        'NA': 'na1'
    }[region]


def summonerid():
    global accountId, id_simple
    link = "https://" + f(region) + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + \
           summoner_name.replace(" ", "%20") + "?api_key=" + api_key
    response = requests.get(link)
    if response.status_code == 200:
        obiect = json.loads(response.content.decode('utf-8'))
        accountId = obiect['accountId']
        id_simple = obiect['id']
        return obiect['id']
    else:
        print(response.status_code)


def rank():
    global winrate
    my_summoner_id = summonerid()
    link = "https://" + f(region) + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(my_summoner_id) + \
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


my_rank = rank()
print(my_rank)
my_winrate = "Win Ratio " + str(int(winrate)) + "%"
print(my_winrate)
print("accountId: " + str(accountId))
print("id: " + str(id_simple))
accountID = str(accountId)


def getIDMatches():
    lista_match_id = []
    beginIndex = 0
    endIndex = 100
    link = "https://" + f(
        region) + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + accountID + "?beginIndex=" + str(
        beginIndex) + "&endIndex=" + str(endIndex) + "&queue=420&season=11&api_key=" + api_key
    response_link = requests.get(link)
    if response_link.status_code == 200:
        obiect = json.loads(response_link.content.decode('utf-8'))
        for i in range(len(obiect['matches'])):
            lista_match_id.append(obiect['matches'][i]['gameId'])

    while len(lista_match_id) == endIndex:
        beginIndex = endIndex
        endIndex = endIndex + 100
        link = "https://" + f(
            region) + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + accountID + "?beginIndex=" + str(
            beginIndex) + "&endIndex=" + str(endIndex) + "&queue=420&season=11&api_key=" + api_key
        response_link = requests.get(link)
        if response_link.status_code == 200:
            obiect = json.loads(response_link.content.decode('utf-8'))
            for i in range(len(obiect['matches'])):
                lista_match_id.append(obiect['matches'][i]['gameId'])
    return lista_match_id

lista_meciuri = getIDMatches()


with open('lista_meciuri.txt', 'r+') as file:
    a = file.readlines()
    if len(a) == 0:
        for i in range(len(lista_meciuri)):
            file.write(str(lista_meciuri[i]) + "\n")


def championwinrate():
    global lista_winrate_campioni
    global update
    meciuri_de_adaugat = []
    matchID = lista_meciuri
    contor = 0
    if len(matchID) != len(a):
        update = True
        if len(a) != 0:
            for i in range(len(set(a))):
                a[i] = a[i].strip('\n')
            lista_de_comparat = list(set(a))
            file2 = open('lista_campionilor_jucati.txt')
            lista_winrate_campioni = json.loads(file2.readline())
            for j in range(len(matchID)):
                if str(lista_meciuri[j]) not in lista_de_comparat:
                    meciuri_de_adaugat.append(str(lista_meciuri[j]))
                    file_lista_meciuri = open('lista_meciuri.txt', 'r+')
                    file_lista_meciuri.readlines()
                    file_lista_meciuri.write(str(lista_meciuri[j]) + "\n")
        else:
            meciuri_de_adaugat = matchID
    if update == True:
        # print(meciuri_de_adaugat)
        for match in meciuri_de_adaugat:
            # print(match)
            lista = [None, None]
            champID = None
            games = 0
            win = 0
            k = 0
            WON = None
            link_match = "https://" + f(region) + ".api.riotgames.com/lol/match/v3/matches/" + str(match) + \
                         "?api_key=" \
                         + api_key
            response_match = requests.get(link_match)
            if response_match.status_code == 200:
                obiect = json.loads(response_match.content.decode('utf-8'))
                if int(obiect['gameDuration']) < 300:
                    print("REMAKEEEEEEEEEEEEEEEEEEEEEEEEE " + str(obiect['gameDuration']))
                    continue
                else:
                    for i in range(2):
                        lista[i] = obiect['teams'][i]['win']
                    for i in range(0, 10):
                        if obiect['participantIdentities'][i]['player']['summonerName'] == summoner_name:
                            if i + 1 <= 5 and lista[0] == 'Win':
                                champID = obiect['participants'][i]['championId']
                                games = 1
                                win = 1
                                WON = True
                                print("WIN " + str(champID))
                            elif i + 1 > 5 and lista[1] == 'Win':
                                champID = obiect['participants'][i]['championId']
                                games = 1
                                win = 1
                                WON = True
                                print("WIN " + str(champID))
                            else:
                                champID = obiect['participants'][i]['championId']
                                games = 1
                                WON = False
                                print("LOSS " + str(champID))
                    lista_de_adaugat = [champID, games, win]
                    contor = contor + 1
                    if contor == 30:
                        time.sleep(30)
                        contor = 0
                    if len(lista_winrate_campioni) == 0:
                        lista_winrate_campioni.append(lista_de_adaugat)
                    else:
                        for i in range(len(lista_winrate_campioni)):
                            if champID != lista_winrate_campioni[i][0]:
                                k = k + 1
                                if k == len(lista_winrate_campioni):
                                    lista_winrate_campioni.append(lista_de_adaugat)
                            elif champID == lista_winrate_campioni[i][0]:
                                lista_winrate_campioni[i][1] += 1
                                if WON == True:
                                    lista_winrate_campioni[i][2] += 1
                                    WON = None
            else:
                print(response_match.status_code)
    else:
        print("No new updates")


championwinrate()

with open('lista_campionilor_jucati.txt', 'r+') as file3:
    if update == True:
        file3.truncate()
        file3.write(str(lista_winrate_campioni))
    elif update == False:
        print(file3.readline())
file.close()
file3.close()
