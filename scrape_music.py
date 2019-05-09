from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


def get_html_text(html):
    try:
        return html.text

    except AttributeError:
        return np.nan


def parse_title(html_title):
    title_text = html_title.text
    try:
        pub_end_index = title_text.index("'")
        pub = title_text[:pub_end_index]

    except ValueError:
        pub = np.nan

    year = title_text[-4:]

    return pub, year


def scrape_page(soup):
    """scrape the html from a page for album of the year and convert to a data frame"""
    rows = soup.findAll(class_="albumListRow")
    list_length = len(rows)

    title = soup.find("title")

    # Exclude non year-end lists
    if "so far" in title.text.lower():
        return None

    else:
        pub, year = parse_title(title)

        #Get the rank, title, and artist as a list
        page_data = dict()
        collect_terms = ["albumListTitle", "albumListDate", "albumListGenre", "scoreText", "scoreValue"]
        for term in collect_terms:
            page_data[term] = [get_html_text(row.find(class_=term)) for row in rows]

        page_df = pd.DataFrame.from_dict(page_data)

        page_df[["albumRank", "albumTitleArtist"]] = page_df.albumListTitle.str.split(".", n=1, expand=True)
        page_df[["albumArtist", "albumTitle"]] = page_df.albumTitleArtist.str.rsplit("-", n=1, expand=True)
        page_df.drop(columns=["albumListTitle", "albumTitleArtist"], inplace=True)

        page_df['listSize'] = list_length
        page_df['publication'] = pub
        page_df['year'] = year

        return page_df


def get_year_links(year_soup):
    """returns the links to all year end lists for a given year's html"""
    base_page = "https://www.albumoftheyear.org"

    return [base_page + child.a.attrs["href"] for child in year_soup.findAll(class_="criticListBlockTitle")]


def scrape_year(year):
    """scrapes all data for a year and returns a single df"""
    url = "https://www.albumoftheyear.org/lists.php?y={}".format(year)

    year_req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    year_soup = BeautifulSoup(urlopen(year_req))
    list_links = get_year_links(year_soup)

    all_year_df = []
    for link in list_links:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(urlopen(req))
        all_year_df.append(scrape_page(soup))

    return pd.concat(all_year_df)


def scrape_years(year_range):
    """Performs scrape_year across multiple years

    Returns a pandas DF
    """
    all_year_df = []
    for year in year_range:
        all_year_df.append(scrape_year(year))
        print(year)

    return pd.concat(all_year_df)


if __name__ == "__main__":
    # Start at the earliest year and first alphabetical reviewer
    year_range = range(2000, 2018)
    scrape_years(year_range).to_csv("test_df.csv")
