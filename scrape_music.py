from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# Start at the earliest year and first alphabetical reviewer
url = "https://www.albumoftheyear.org/list/280-pitchforks-top-20-albums-of-2000/"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req)
soup = BeautifulSoup(html)


def get_html_text(html):
    try:
        return html.text

    except AttributeError:
        return np.nan

def parse_title(html_title):
    title_text = html_title.text
    pub_end_index = title_text.index("'")

    pub = title_text[:pub_end_index]
    year = title_text[-4:]

    return pub, year


def scrape_page(soup):
    """scrape the html from a page for album of the year and convert to a data frame"""
    rows = soup.findAll(class_="albumListRow")
    list_length = len(rows)

    pub, year = parse_title(soup.find("title"))
    #Get the rank, title, and artist as a list

    page_data = dict()
    collect_terms = ["albumListTitle", "albumListDate", "albumListGenre", "scoreText", "scoreValue"]
    for term in collect_terms:
        page_data[term] = [get_html_text(row.find(class_=term)) for row in rows]

    page_df = pd.DataFrame.from_dict(page_data)

    page_df['listSize'] = list_length
    page_df['publication'] = pub
    page_df['year'] = year

    return page_df

if __name__ == "__main__":
    print(scrape_page(soup))
