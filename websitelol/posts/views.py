from django.shortcuts import render, redirect
from .forms import PostsForm
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import time
from .models import Posts
from configparser import ConfigParser
from . import analytica
from decimal import getcontext, Decimal

config = ConfigParser()
config.read('config.ini')
api_key = config.get('auth', 'api_key')


def getversion():
    link = "https://ddragon.leagueoflegends.com/api/versions.json"
    response = requests.get(link)
    if response.status_code == 200:
        obiect = json.loads(response.content.decode('utf-8'))
        version = obiect[0]
        return version
    else:
        print(response.status_code)


def summonerid(summoner_name, region):
    global profileIcon, summonerlevel, summoner_name_real
    link = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + \
           summoner_name.replace(" ", "%20") + "?api_key=" + api_key
    response = requests.get(link)
    if response.status_code == 200:
        obiect = json.loads(response.content.decode('utf-8'))
        accountId = obiect['accountId']
        id_simple = obiect['id']
        profileIcon = obiect['profileIconId']
        summonerlevel = obiect['summonerLevel']
        summoner_name_real = obiect['name']
        return id_simple, accountId
    else:
        print(response.status_code)


def getIDMatches(reg, accountid):
    lista_match_id = []
    beginIndex = 0
    endIndex = 100
    link = "https://" + \
           reg + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(accountid) + "?beginIndex=" + str(
        beginIndex) + "&endIndex=" + str(endIndex) + "&queue=420&season=11&api_key=" + api_key
    response_link = requests.get(link)
    if response_link.status_code == 200:
        obiect = json.loads(response_link.content.decode('utf-8'))
        for i in range(len(obiect['matches'])):
            lista_match_id.append(obiect['matches'][i]['gameId'])

    while len(lista_match_id) == endIndex:
        beginIndex = endIndex
        endIndex = endIndex + 100
        link = "https://" + \
               reg + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(accountid) + "?beginIndex=" + str(
            beginIndex) + "&endIndex=" + str(endIndex) + "&queue=420&season=11&api_key=" + api_key
        response_link = requests.get(link)
        if response_link.status_code == 200:
            obiect = json.loads(response_link.content.decode('utf-8'))
            for i in range(len(obiect['matches'])):
                lista_match_id.append(obiect['matches'][i]['gameId'])
    return lista_match_id


def rank(reg, summoner_id):
    work_with = 0
    link = "https://" + reg + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(summoner_id) + \
           "?api_key=" + api_key
    response = requests.get(link)
    if response.status_code == 200:
        obiect = json.loads(response.content.decode('utf-8'))
        for i in range(len(obiect)):
            try:
                if obiect[i]['queueType'] == "RANKED_SOLO_5x5":
                    work_with = i
            except IndexError:
                continue
        wins = obiect[work_with]['wins']
        losses = obiect[work_with]['losses']
        winrate = round((wins / (wins + losses)) * 100, 0)
        return obiect[work_with]['tier'], obiect[work_with]['rank'], obiect[work_with]['leaguePoints'], obiect[work_with]['wins'],obiect[work_with]['losses'],\
               winrate
    else:
        print(response.status_code)

def inlocuire_nume(campion):
    with open('champions.txt', 'r+') as file:
        obiect = json.loads(file.readline())
    a = list(obiect['data'])
    id_champ = campion
    for champ in a:
        if obiect['data'][str(champ)]['id'] == id_champ:
            nume = obiect['data'][str(champ)]['name']
            nume_splashart = champ
            return nume, nume_splashart


def last20games(lista_meciuri, regiune):
    lista_winrate_campioni = []
    participant_id = None
    kills = None
    deaths = None
    assists = None
    for match in lista_meciuri:
        print(match)
        lista = [None, None]
        champID = None
        games = 0
        win = 0
        k = 0
        WON = None
        link_match = "https://" + regiune + ".api.riotgames.com/lol/match/v3/matches/" + str(match) + \
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
                    if obiect['participantIdentities'][i]['player']['accountId'] == a_id:
                        participant_id = obiect['participantIdentities'][i]['participantId']
                    if obiect['participants'][i]['participantId'] == participant_id:
                        kills = obiect['participants'][i]['stats']['kills']
                        deaths = obiect['participants'][i]['stats']['deaths']
                        assists = obiect['participants'][i]['stats']['assists']
                    if obiect['participantIdentities'][i]['player']['accountId'] == a_id:
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
                lista_de_adaugat = [champID, games, win, kills, deaths, assists]
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
                            lista_winrate_campioni[i][3] += lista_de_adaugat[3]
                            lista_winrate_campioni[i][4] += lista_de_adaugat[4]
                            lista_winrate_campioni[i][5] += lista_de_adaugat[5]
                            if WON == True:
                                lista_winrate_campioni[i][2] += 1
                                WON = None
        else:
            print(response_match.status_code)
    return lista_winrate_campioni


def championwinrate(lista_meciuri, a, regiune, listacampionijucati):
    lista_winrate_campioni = []
    update = None
    participant_id = None
    kills = None
    deaths = None
    assists = None
    meciuri_de_adaugat = []
    matchID = lista_meciuri
    contor = 0
    if len(matchID) != len(a):
        print('Am intrat')
        update = True
        if len(a) != 0:
            print('Am intrat aici?')
            lista_de_comparat = a
            lista_winrate_campioni = listacampionijucati
            for j in range(len(matchID)):
                if lista_meciuri[j] not in lista_de_comparat:
                    meciuri_de_adaugat.append(lista_meciuri[j])
        else:
            meciuri_de_adaugat = lista_meciuri
    if update == True:
        print(meciuri_de_adaugat)
        for match in meciuri_de_adaugat:
            print(match)
            lista = [None, None]
            champID = None
            games = 0
            win = 0
            k = 0
            WON = None
            link_match = "https://" + regiune + ".api.riotgames.com/lol/match/v3/matches/" + str(match) + \
                         "?api_key=" \
                         + api_key
            response_match = requests.get(link_match)
            if response_match.status_code == 200:
                obiect = json.loads(response_match.content.decode('utf-8'))
                if int(obiect['gameDuration']) < 300:
                    print("REMAKEEEEEEEEEEEEEEEEEEEEEEEEE " + str(obiect['gameDuration']))
                    continue
                else:
                    gametime = int(obiect['gameDuration'])
                    totalcs = 0
                    for i in range(2):
                        lista[i] = obiect['teams'][i]['win']
                    for i in range(0, 10):
                        if obiect['participantIdentities'][i]['player']['accountId'] == a_id:
                            participant_id = obiect['participantIdentities'][i]['participantId']
                        if obiect['participants'][i]['participantId'] == participant_id:
                            kills = obiect['participants'][i]['stats']['kills']
                            deaths = obiect['participants'][i]['stats']['deaths']
                            assists = obiect['participants'][i]['stats']['assists']
                            totalcs = int(obiect['participants'][i]['stats']['neutralMinionsKilled']) + int(obiect['participants'][i]['stats']['totalMinionsKilled'])
                        if obiect['participantIdentities'][i]['player']['accountId'] == a_id:
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
                    csperminute = (totalcs/gametime)*60
                    lista_de_adaugat = [champID, games, win, kills, deaths, assists, csperminute, totalcs]
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
                                lista_winrate_campioni[i][3] += lista_de_adaugat[3]
                                lista_winrate_campioni[i][4] += lista_de_adaugat[4]
                                lista_winrate_campioni[i][5] += lista_de_adaugat[5]
                                lista_winrate_campioni[i][6] += lista_de_adaugat[6]
                                lista_winrate_campioni[i][7] += lista_de_adaugat[7]
                                if WON == True:
                                    lista_winrate_campioni[i][2] += 1
                                    WON = None
            else:
                print(response_match.status_code)
    else:
        print("No new Updates")
    return lista_winrate_campioni


def index(request):
    global s_id, a_id, region, summoner_name
    if request.method == "POST":
        form = PostsForm(request.POST)
        if form.is_valid():
            summoner_name = request.POST['summoner_name']
            region = request.POST['region']
            s_id, a_id = summonerid(summoner_name, region)
            post_item = form.save(commit=False)
            post_item.summonerID = s_id
            post_item.accountID = a_id
            search = Posts.objects.filter(summoner_name=summoner_name, region=region)
            if not search:
                post_item.save()
            listofgames = getIDMatches(region, a_id)    #Din API, actualizata
            searchgamesplayed = Posts.objects.filter(summoner_name=summoner_name, region=region).values('gamesPlayed')[0]['gamesPlayed']
            searchchampsplayed = Posts.objects.filter(summoner_name=summoner_name, region=region).values('championsPlayed')[0]['championsPlayed']
            currentid = Posts.objects.filter(summoner_name=summoner_name, region=region).values('id')[0]['id']
            t = Posts.objects.get(id=int(currentid))
               #from DB
            if len(searchchampsplayed) != 0:
                champslist = json.loads(searchchampsplayed)
            else:
                champslist = []
            if len(searchgamesplayed) != 0:
                gameslist = json.loads(searchgamesplayed)
            else:
                gameslist = []
            champ = championwinrate(listofgames, gameslist, region, champslist)
            if len(champ) != 0:
                t.championsPlayed = champ
                t.save()
            if len(searchgamesplayed) == 0:
                t.gamesPlayed = listofgames
                t.save()
            elif len(searchgamesplayed) != 0:
                gameslist = json.loads(searchgamesplayed)
                if len(gameslist) != len(listofgames):
                    t.gamesPlayed = listofgames
                    t.save()
                else:
                    pass
            return redirect('/stats/')
    else:
        form = PostsForm()
    return render(request, 'posts/index.html', {
        'form': form,
        'title': 'Please enter your summoner name and select your region',
    })


def stats(request):
    tier, mrank, leaguepoints, wins, losses, winrate = rank(region, s_id)
    icon = "http://ddragon.leagueoflegends.com/cdn/" + str(getversion()) + "/img/profileicon/" + str(profileIcon) + ".png"
    tier_icon = tier.lower() + "_" + mrank.lower() + ".png"
    listapentruhtml = []
    tuplelast20games = ()
    winslast20games = 0
    gameslast20games = 0
    killslast20games = 0
    assistslast20games = 0
    deathslast20games = 0
    listapentruhtml_last20games = []


    a = getIDMatches(region, a_id)
    list_of_last20games = last20games(a[0:20], region)


    if len(list_of_last20games) != 0:
        list_of_last20games.sort(key=lambda x: x[1], reverse=True)
        for j in range(len(list_of_last20games)):
            winslast20games = winslast20games + list_of_last20games[j][2]
            gameslast20games = gameslast20games + list_of_last20games[j][1]
            killslast20games = killslast20games + list_of_last20games[j][3]
            deathslast20games = deathslast20games + list_of_last20games[j][4]
            assistslast20games = assistslast20games + list_of_last20games[j][5]
        losseslast20games = gameslast20games - winslast20games
        avgkillslast20games = round(killslast20games/gameslast20games, 1)
        avgdeathslast20games = round(deathslast20games/gameslast20games, 1)
        avgassistslast20games = round(assistslast20games/gameslast20games, 1)
        kdalast20games = round((avgkillslast20games + avgassistslast20games)/avgdeathslast20games, 1)
        getcontext().prec = 3
        # winratelast20games = str(round(winslast20games/gameslast20games, 3) * 100) + "%"
        winratelast20games = str((Decimal(winslast20games)/Decimal(gameslast20games))*100) + "%"
        for i in range(len(list_of_last20games[0:3])):
            try:
                t = []
                numecampion_last20games, splash_art_last20games = inlocuire_nume(list_of_last20games[i][0])
                k = list_of_last20games[i][3]
                d = list_of_last20games[i][4]
                a = list_of_last20games[i][5]
                try:
                    kdacampion_last20games = round((k + a)/d,2)
                except ZeroDivisionError:
                    kdacampion_last20games = "Perfect KDA"
                # winratecampionlast20games = str(round(list_of_last20games[i][2]/list_of_last20games[i][1], 3) * 100) + "%"
                winratecampionlast20games = str( (Decimal(list_of_last20games[i][2])/Decimal(list_of_last20games[i][1]))*100 ) + "%"
                winscampionlast20games = list_of_last20games[i][2]
                lossescampionlast20games = list_of_last20games[i][1] - winscampionlast20games
                splash_art_last20 = "http://ddragon.leagueoflegends.com/cdn/" + str(
                    getversion()) + "/img/champion/" + splash_art_last20games + ".png"
                t = (numecampion_last20games, splash_art_last20, kdacampion_last20games, winratecampionlast20games,
                     winscampionlast20games, lossescampionlast20games)
                listapentruhtml_last20games.append(t)
            except IndexError:
                continue
        tuplelast20games = (gameslast20games, winslast20games, losseslast20games, avgkillslast20games,
                           avgdeathslast20games, avgassistslast20games, kdalast20games, winratelast20games)

    searchchampsplayed = Posts.objects.filter(summoner_name=summoner_name, region=region).values('championsPlayed')[0][
        'championsPlayed']
    if len(searchchampsplayed) != 0:
        listadinBDD = json.loads(searchchampsplayed)
        listadinBDD.sort(key=lambda x: x[1], reverse=True)
        for i in range(len(listadinBDD)):
            campion = listadinBDD[i][0]
            numar_jocuri = listadinBDD[i][1]
            numar_winuri = listadinBDD[i][2]
            numar_killuri = listadinBDD[i][3]
            numar_deaths = listadinBDD[i][4]
            numar_assists = listadinBDD[i][5]
            avgcs = round(int(listadinBDD[i][7])/int(numar_jocuri), 1)
            avgcsperminute = round(int(listadinBDD[i][6]) / int(numar_jocuri), 1)
            avgkills = round(int(numar_killuri)/int(numar_jocuri), 1)
            avgdeaths = round(int(numar_deaths)/int(numar_jocuri), 1)
            avgassists = round(int(numar_assists)/int(numar_jocuri), 1)
            nume, nume_splash = inlocuire_nume(campion)
            splah_art = "http://ddragon.leagueoflegends.com/cdn/" + str(getversion()) + "/img/champion/" + nume_splash + ".png"
            winratepentruhtml = int(numar_winuri)/int(numar_jocuri)
            winrate_int = round((int(numar_winuri)/int(numar_jocuri))*100)
            winrate_campion = str(winrate_int) + "%"
            try:
                kda = round((int(numar_killuri) + int(numar_assists)) / int(numar_deaths), 2)
            except ZeroDivisionError:
                kda = 'Perfect KDA'
            tulp = (nume, splah_art, numar_jocuri, winrate_campion, kda, avgkills, avgdeaths, avgassists,
                    winratepentruhtml, avgcs, avgcsperminute)
            listapentruhtml.append(tulp)
    print(listapentruhtml_last20games)
    return render(request, 'posts/stats.html', {
        'name': summoner_name_real,
        'summonerlevel': summonerlevel,
        'icon': icon,
        'tier': tier.title() + " " + mrank,
        'leaguepoints': str(leaguepoints) + 'LP',
        'wins': str(wins) + 'W',
        'losses': str(losses) + 'L',
        'winrate': str(round(winrate)) + '%',
        'tier_icon': tier_icon,
        'listapentruhtml': listapentruhtml,
        'listapentruhtml_last20games': listapentruhtml_last20games,
        'tuplelast20games': tuplelast20games,
        'title': 'Aici o sa vezi statsurile',
    })

@csrf_exempt
def recommandations(request):
    champ = json.loads(request.body)['nume']
    champgood = ''.join(c for c in champ if c.isalpha())
    counters, goodagainst, summoner_spells, skill_order, skill_order_table, build, masteries_header_icons, \
    primary_masteries, secondary_masteries = analytica.scraper(champgood)
    return render(request, 'posts/recommandations.html', {
        'champ': champ.title(),
        'counters': counters,
        'goodagainst': goodagainst,
        'summoner_spells': summoner_spells,
        'skill_order': skill_order,
        'skill_order_table': skill_order_table,
        'build': build,
        'masteries_header_icons': masteries_header_icons,
        'primary_masteries': primary_masteries,
        'secondary_masteries': secondary_masteries
    })
