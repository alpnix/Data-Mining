import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from bs4 import BeautifulSoup
import requests


domain = "https://www.imdb.com"
top250 = "/chart/top/?ref_=nv_mv_250"
url = domain + top250

page = requests.get(url)

soup = BeautifulSoup(page.content,"html.parser")

lister = soup.find(class_="lister")
movies_table = lister.find("table")

table_head = movies_table.find("thead")
table_body = movies_table.find("tbody")

# getting the year between the brackets
def get_year(text):
    new = ""
    for chr in text:
        if chr != ")" and chr != "(":
            new += chr

    return int(new)

# getting the table headers
for index, header_data in enumerate(table_head.find("tr").find_all("th")):
    print(index, header_data.get_text().upper())

headers = ["Title","Year","Rating","URL"]
# looping over the rows in the table
names, years, rates, urls = [], [], [], []
for row in table_body.find_all("tr"):
    movie_name = row.find(class_="titleColumn").find("a").get_text()
    try:
        # try to get the data
        movie_year = get_year(row.find(class_="secondaryInfo").get_text())
        movie_rate = float(row.find(class_="imdbRating").get_text())
        movie_url = domain
        movie_url += row.find(class_="titleColumn").find("a")["href"]
    except:
        print(f"Missing data for {movie_name}")
    else:
        names.append(movie_name)
        years.append(movie_year)
        rates.append(movie_rate)
        urls.append(movie_url)


# creating the dataframe
movies_df = pd.DataFrame((zip(names,years,rates,urls)),columns=headers)

# sorting the years and rates in the same order
for i in range(1,len(years)):
    key = years[i]
    name_key = names[i]
    rate_key = rates[i]
    j = i - 1

    while j >= 0 and years[j] > key:
        years[j+1] = years[j]
        rates[j+1] = rates[j]
        names[j+1] = names[j]
        j -= 1

    years[j+1] = key
    names[j+1] = name_key
    rates[j+1] = rate_key


# styling the plot
plt.xkcd(1,1,1)
# plt.rcdefaults()
plt.style.use("fivethirtyeight")

# plotting the figure
fig, ax = plt.subplots()
plot = ax.plot(years,rates,color="#0000FF",label="Rates",linewidth=3)
ax.fill_between(years,min(movies_df["Rating"]),rates,color="yellow",alpha=0.1)

# setting the label
ax.set_xlabel("Years",fontsize=18)
ax.set_ylabel("Rates",fontsize=18)
ax.set_title("IMDB Top 250 Movie Rates Over Years",fontsize=22)

# adding some hover functionality to the plot

cursor = mplcursors.cursor(plot,hover=True)

cursor.connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f"{names[int(sel.target.index)]}\n{rates[int(sel.target.index)]}"
    )
)

# formatting the plot
fig.autofmt_xdate()
plt.tight_layout()
plt.legend(loc="upper left")

# dataframe methods
df = movies_df
print(df.head())
print(df.count(0))
# print(df.set_index(["Title","Rating"]).count(level="Rating"))
print(df.set_index(["Title","Rating","Year"])["URL"])

plt.show()
