import pandas as pd
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import mplcursors

page = requests.get("https://en.wikipedia.org/wiki/Pichichi_Trophy")

soup = BeautifulSoup(page.content,"html.parser")
print("Cookies: " + str(page.cookies))

# getting the table from wiki
table = soup.find(class_=["wikitable", "sortable", "jquery-tablesorter"])

# getting header labels of the table
headers = []
for headerTag in table.find("tr").find_all("th"):
    header = headerTag.get_text().replace("\n","")
    headers.append(header)

# sanitizing each text: strip, remove \n, e.g.
def sanitize(text):
    text = text.strip()
    text.replace("\n", "")

    while "[" in text or "(" in text:
        if "[" in text:
            brackets = True
            start = list(text).index("[")
            end = list(text).index("]")
        elif "(" in text:
            brackets = True
            start = list(text).index("(")
            end = list(text).index(")")
        text = list(text)
        new = ""
        for i in range(len(text)):
            if start <= i <= end:
                continue
            new += text[i]
        text = new

    return text


# looping over the table body to get the data
seasons, players, teams, goals, games, ratios = [], [], [], [], [], []
table_body = table.find("tbody")
for row in table_body.find_all("tr"):
    row_data = row.find_all("td")
    try:
        try:
            season = sanitize(row.find("th").get_text())
        except:
            season = seasons[-1]
        player = sanitize(row_data[0].get_text())
        team = sanitize(row_data[1].get_text())
        goal = int(sanitize(row_data[2].get_text()))
        game = int(sanitize(row_data[3].get_text()))
        ratio = float(sanitize(row_data[4].get_text()))
    except:
        print(f"Missing data on {season}")
        with open("scrapelog.txt","a") as f:
            pass
            # f.write(str(row.prettify()))
            # f.write("\n\n\n\n\n")
    else:
        seasons.append(season)
        players.append(player)
        teams.append(team)
        goals.append(goal)
        games.append(game)
        ratios.append(ratio)

# combining all the list into a dataframe shape
data = list(map(lambda a,b,c,d,e,f: [a,b,c,d,e,f],seasons,players,teams,goals,games,ratios))

# creating a Pandas dataframe
pichichiData = pd.DataFrame(data, columns=headers)

# sorting all the years in ascending order
sortedGames = list(pichichiData["Games"])

# insertion sort algorithm for sorting years
def insertionSort(arr):
    for i in range(len(arr)):
        key = arr[i]
        j = i - 1
        while j>=0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

insertionSort(sortedGames)

years = []
# getting a single year for each season
for i in pichichiData["Season"]:
    try:
        year = str(i).split(i[4])
    except:
        year = int(i)
        years.append(year)
    else:
        year = int(year[0])+1
        years.append(year)

plt.style.use("dark_background")

fig, ax = plt.subplots()
# plotting both a scatter and a plot for the poitns
goals = ax.plot(years,list(pichichiData["Goals"]),color="red",label="Goals",marker="2")

# creating a new y axis for games
ax2 = ax.twinx()

games = ax2.plot(years,list(pichichiData["Games"]),color="green",label="Games",marker="1")

# plt.style.use("ggplot")
plt.fill_between(years,pichichiData["Goals"],pichichiData["Games"],color="yellow",alpha=0.55)
# setting the labels for the graph
ax.set_title("Each Years Pichici Award Winners")
ax.set_xlabel("Years")
ax.set_ylabel("Number of Goals",color="red")
ax2.set_ylabel("Number of Games",color="green")

# styling the tick colors
ax.tick_params(axis="y",color="red",labelcolor="red")
ax2.tick_params(axis="y",color="green",labelcolor="green")

# dates will display in a slanting manner
fig.autofmt_xdate()
# formatting all the axis
plt.tight_layout()

ax.legend(loc="upper left")
ax2.legend(loc="upper right")
# push the data to a csv file
pichichiData.to_csv("data/pichici.csv")

# on click
cursor = mplcursors.cursor(games)
cursor2 = mplcursors.cursor(goals)
print(pichichiData.head(20))

def onHover(sel):
    fig.canvas.toolbar.set_message(
        sel.annotation.set_text(list(pichichiData["Player"])
                                [int(round(sel.target.index))] +
                                "\n" +
                                list(pichichiData["Club"])
                                [int(round(sel.target.index))] +
                                ", " +
                                list(map(str,pichichiData["Ratio"]))
                                [int(round(sel.target.index))]
                                )
    )

cursor.connect(
    "add", onHover
)
cursor2.connect(
    "add",onHover
)

plt.show()