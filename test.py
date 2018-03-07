import json
import requests

with open('lista_campionilor_jucati.txt', 'r+') as file:
    lista = json.loads(file.readline())

lista.sort(key = lambda x: x[1], reverse = True)
print(lista)

def inlocuire_nume():
    with open('lista_campionilor_jucati.txt', 'r+') as file:
        lista = json.loads(file.readline())
    lista.sort(key=lambda x: x[1], reverse=True)
    with open('champions.txt', 'r+') as file2:
        obiect = json.loads(file2.readline())
    a = list(obiect['data'])
    for i in range(len(lista)):
        id_champ = lista[i][0]
        for champ in a:
            if obiect['data'][str(champ)]['id'] == id_champ:
                lista[i][0] = obiect['data'][str(champ)]['name']
    print(lista)

def more_stats():
    participant_id = None
    kills = None
    deaths = None
    assists = None
    link_match = "https://" + "eun1" + ".api.riotgames.com/lol/match/v3/matches/" + "1923008434" + "?api_key=" \
                             + "RGAPI-34620c42-4420-40b5-93d3-10ad56e8070e"
    response_match = requests.get(link_match)
    print(link_match)
    if response_match.status_code == 200:
        obiect = json.loads(response_match.content.decode('utf-8'))
        if int(obiect['gameDuration']) < 300:
            return "NO"
        else:
            for i in range(10):
                if obiect['participantIdentities'][i]['player']['summonerName'] == "Jon Snow":
                    participant_id = obiect['participantIdentities'][i]['participantId']
            for i in range(10):
                if obiect['participants'][i]['participantId'] == participant_id:
                    kills = obiect['participants'][i]['stats']['kills']
                    deaths = obiect['participants'][i]['stats']['deaths']
                    assists = obiect['participants'][i]['stats']['assists']
    else:
        print(response_match.status_code)
    return "Kills: " + str(kills) + " " + "Deaths: " + str(deaths) + " " + "Assists: " + str(assists)
print(more_stats())
inlocuire_nume()
