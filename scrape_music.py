from urllib.request import Request, urlopen
import json
from bs4 import BeautifulSoup

# Start at the earliest year and first alphabetical reviewer
url = "https://www.albumoftheyear.org/list/280-pitchforks-top-20-albums-of-2000/"
#req = Request(url, data=bytes(json.dumps({'User-Agent': 'Mozilla/5.0'}), 'utf-8'))
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req)
soup = BeautifulSoup(html)

def scrape_page(soup):
    "scrape the html from a page for album of the year and convert to a data frame"
    rows = soup.findAll(class_="albumListRow")
    list_length = len(rows)

    #Get the rank, title, and artist as a list
    albums = [row.find(_class="albumListTitle").text for row in rows]

    sample = rows[0]

    for row in rows:
        print(row.find(class_ = "albumListTitle").text)


    return albums


print(scrape_page(soup))
