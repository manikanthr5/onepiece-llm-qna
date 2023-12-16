"""
This script is used to scrape data from the website "https://onepiece.fandom.com/wiki/Chapters_and_Volumes".
It retrieves the webpage content using the requests library and parses it using BeautifulSoup.
The scraping logic can be implemented in the TODO section.
"""

from markdownify import markdownify as md
from .utils import collect_soup_util


def collect_headers(soup):
    title = soup.find("h1").text.strip()


def scrape_chapters_and_volumes():
    """ Scrape data from the website "https://onepiece.fandom.com/wiki/Chapters_and_Volumes" """

    url = "https://onepiece.fandom.com/wiki/Chapters_and_Volumes"
    soup = collect_soup_util(url)


def main():
    pass


if __name__ == "__main__":
    main()
