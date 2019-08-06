from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def scraper(champion):
    counters_list = []  # Contra caror campioi NU este bun
    goodagainst_list = []  # Contra caror campioni este bun
    summoner_spells_list = []  # Ce summoner spell-uri sa iei
    skill_order_list = []  # Ce abilitate maxezi prima data
    skill_order_table_list = []  # Tabel cu ordinea in care pui skill-urile
    build_list = []  # Lista cu build-urile propuse, numerotate de la 1 la 10/ 1 - 2: Starting Items, 3 - 7: Core Items,
    #  7 - 10: Boots Recommandation
    masteries_header_icons_list = []  # Ceea ce se va vedea deasupra tree-ului efectiv
    primary_masteries_list = []  # Primary masteries
    secondary_masteries_list = []  # Secondary Masteries
    max_q = 0
    max_w = 0
    max_e = 0
    my_url = "http://na.op.gg/champion/" + champion.replace(" ", "") + "/"

    # Grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    # html parser
    page_soup = soup(page_html, "html.parser")

    # html parser for counters
    table_strong = page_soup.find("table", {
        "class": "champion-stats-header-matchup__table champion-stats-header-matchup__table--strong tabItem"})
    champions_strong = table_strong.findAll("td", {"class": "champion-stats-header-matchup__table__champion"})
    champions_winrate_strong = table_strong.findAll("td", {"class": "champion-stats-header-matchup__table__winrate"})

    # html parser for good against
    table_weak = page_soup.find("table", {
        "class": "champion-stats-header-matchup__table champion-stats-header-matchup__table--weak tabItem"})
    champions_weak = table_weak.findAll("td", {"class": "champion-stats-header-matchup__table__champion"})
    champions_winrate_weak = table_weak.findAll("td", {"class": "champion-stats-header-matchup__table__winrate"})

    # html parser for summoner spells
    table_summoner_spells = page_soup.find("table", {
        "class": "champion-overview__table champion-overview__table--summonerspell"
    })

    all_summoner_spells = table_summoner_spells.findAll("ul", {
        "class": "champion-stats__list"
    })

    summoner_spells = all_summoner_spells[0].findAll("li", {
        "class": "champion-stats__list__item"
    })

    max_abilities = all_summoner_spells[2].findAll("li", {
        "class": "champion-stats__list__item"
    })

    table_skill_order = table_summoner_spells.find("table", {
        "class": "champion-skill-build__table"
    })

    # html parser for item build
    table_build = page_soup.findAll("table", {
        "class": "champion-overview__table"
    })
    body_table_build = table_build[1].tbody
    table_build_data = body_table_build.findAll("td", {
        "class": "champion-overview__data champion-overview__border champion-overview__border--first"
    })
    masteries_table = table_build[2]
    masteries_header = masteries_table.find("div", {
        "class": "champion-stats-summary-rune-image"
    })
    masteries_header_icons = masteries_header.findAll("img", {
        "class": "champion-stats-summary-rune__image"
    })

    primary_masteries = masteries_table.findAll("div", {
        "class": "perk-page"
    })

    primary_masteries_rows = primary_masteries[0].findAll("div", {
        "class": "perk-page__row"
    })

    secondary_masteries_rows = primary_masteries[1].findAll("div", {
        "class": "perk-page__row"
    })

    for i in range(len(primary_masteries_rows)):
        masteries_tuple_primary = ()
        primary_row = primary_masteries_rows[i].findAll("div", {
            "class": "perk-page__item"
        })
        for j in range(len(primary_row)):
            masteries_tuple_primary = masteries_tuple_primary + (primary_row[j].img['src'],)
        primary_masteries_list.append(masteries_tuple_primary)

    for i in range(len(secondary_masteries_rows)):
        masteries_tuple_secondary = ()
        secondary_row = secondary_masteries_rows[i].findAll("div", {
            "class": "perk-page__item"
        })
        for j in range(len(secondary_row)):
            masteries_tuple_secondary = masteries_tuple_secondary + (secondary_row[j].img['src'],)
        secondary_masteries_list.append(masteries_tuple_secondary)

    for i in range(len(masteries_header_icons)):
        masteries_header_icons_list.append(masteries_header_icons[i]['src'])

    for i in range(len(table_build_data)):
        item_tuple = ()
        a = table_build_data[i].findAll("ul")[0].findAll("li", {
            "class": "champion-stats__list__item"
        })
        for j in range(len(a)):
            item = a[j].img['src']
            item_tuple = item_tuple + (item,)
        build_list.append(item_tuple)

    for i in range(len(table_skill_order.findAll('tr')[1]('td'))):
        a = table_skill_order.findAll('tr')[1]('td')[i].text
        if str(a).strip() == "Q":
            max_q += 1
        elif str(a).strip() == "W":
            max_w += 1
        elif str(a).strip() == "E":
            max_e += 1
        if max_q == 5:
            skill_order_table_list.append(table_skill_order.findAll('tr')[1]('td')[i].img['src'])
            max_q = 0
        elif max_w == 5:
            skill_order_table_list.append(table_skill_order.findAll('tr')[1]('td')[i].img['src'])
            max_w = 0
        elif max_e == 5:
            skill_order_table_list.append(table_skill_order.findAll('tr')[1]('td')[i].img['src'])
            max_e = 0
        else:
            skill_order_table_list.append(str(a).strip())

    for i in range(len(summoner_spells)):
        summoner_spells_list.append(summoner_spells[i].img['src'])

    for i in range(len(max_abilities)):
        max_spell_img = max_abilities[i].img['src']
        max_spell_key = max_abilities[i].span.text
        skill_order_list_tuple = (max_spell_img, max_spell_key)
        skill_order_list.append(skill_order_list_tuple)

    for i in range(len(champions_strong)):
        champion_name_strong = champions_strong[i].text.strip()
        champion_icon_strong = champions_strong[i].img['src']
        champion_winrate_strong = champions_winrate_strong[i].b.text

        champion_name_weak = champions_weak[i].text.strip()
        champion_icon_weak = champions_weak[i].img['src']
        champion_winrate_weak = champions_winrate_weak[i].b.text

        t_strong = (champion_name_strong, champion_icon_strong, champion_winrate_strong)
        t_weak = (champion_name_weak, champion_icon_weak, champion_winrate_weak)
        counters_list.append(t_strong)
        goodagainst_list.append(t_weak)
    return counters_list, goodagainst_list, summoner_spells_list, skill_order_list, skill_order_table_list, \
           build_list, masteries_header_icons_list, primary_masteries_list, secondary_masteries_list
