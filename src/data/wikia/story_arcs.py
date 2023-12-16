""" Scrape data from the website "https://onepiece.fandom.com/wiki/Story_Arcs" """
# from data.wikia.utils import collect_soup, find_siblings_between_elements
import re
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def collect_soup_util(url):
    """ Collects the soup object of the given URL """
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, features="html.parser")
        return soup
    else:
        print("Failed to retrieve the webpage")


def find_siblings_between_elements(first_element, second_element):
    """ Finds the siblings between the first and second element """

    siblings = []
    current_sibling = first_element.find_next_sibling()

    while current_sibling and current_sibling != second_element:
        siblings.append(current_sibling)
        current_sibling = current_sibling.find_next_sibling()

    return siblings


def clean_markdown_table_util(table):
    return BeautifulSoup(str(table).replace("\n", ""), features="html.parser")


def clean_markdown(elements):
    """ Clean markdown content """
    for i in range(len(elements)):
        if elements[i].name == "table":
            elements[i] = clean_markdown_table_util(elements[i])
        elif elements[i].name == "dl":
            elements[i] = BeautifulSoup("<p>" + str(elements[i]) + "</p>", features="html.parser")
    return elements


def scrap_page_title():
    """ Scrape the page title from the website "https://onepiece.fandom.com/wiki/Story_Arcs" """
    # URL of the page to scrape
    url = "https://onepiece.fandom.com/wiki/Story_Arcs"

    soup = collect_soup_util(url)

    # Find the main content element
    page_title = md(str(soup.find("h1"))).strip()
    descriptions = soup.find(id="mw-content-text").find("div").find_all("p")[1:3]
    content = "\n".join([md(str(description), strip=['a', 'img']) for description in descriptions])
    content = "# " + md(str(page_title)) + "\n\n" + content

    return content


def scrape_story_arcs():
    """ Scrape data from the website "https://onepiece.fandom.com/wiki/Story_Arcs" """
    # URL of the page to scrape
    url = "https://onepiece.fandom.com/wiki/Story_Arcs"

    soup = collect_soup_util(url)

    # Find the main content element
    start_element = soup.find(id="Main_Story_Arcs").parent
    end_element = soup.find(id="Short-Term_Focused_Cover_Page_Serials").parent
    main_story_arcs = find_siblings_between_elements(start_element, end_element)
    main_story_arcs = clean_markdown(main_story_arcs)

    # Convert the HTML content to markdown
    content = "\n".join([md(str(arc), strip=['a', 'img']) for arc in main_story_arcs])
    content = "## " + md(str(start_element)) + "\n" + content

    return content


def scrape_cover_page_serials():
    """ Scrape data from the website "https://onepiece.fandom.com/wiki/Story_Arcs" """
    # URL of the page to scrape
    url = "https://onepiece.fandom.com/wiki/Story_Arcs"

    soup = collect_soup_util(url)

    # Find the main content element
    start_element = soup.find(id="Short-Term_Focused_Cover_Page_Serials").parent
    end_element = soup.find(id="Anime-Only_Arcs").parent
    cover_page_serials = find_siblings_between_elements(start_element, end_element)
    cover_page_serials = clean_markdown(cover_page_serials)

    # Convert the HTML content to markdown
    content = "\n".join([md(str(arc), strip=['a', 'img']) for arc in cover_page_serials])
    content = "## " + md(str(start_element)) + "\n" + content

    return content


def scrape_anime_only_story_arcs():
    """ Scrape data from the website "https://onepiece.fandom.com/wiki/Story_Arcs" """
    # URL of the page to scrape
    url = "https://onepiece.fandom.com/wiki/Story_Arcs"

    soup = collect_soup_util(url)

    # Find the main content element
    start_element = soup.find(id="Anime-Only_Arcs").parent
    end_element = soup.find(id="References").parent
    non_canon_story_arcs = find_siblings_between_elements(start_element, end_element)
    non_canon_story_arcs = clean_markdown(non_canon_story_arcs)

    # Convert the HTML content to markdown
    content = "\n".join([md(str(arc), strip=['a', 'img']) for arc in non_canon_story_arcs])
    content = "## " + md(str(start_element)) + "\n" + content

    return content


def main():
    page_title = scrap_page_title()
    story_arcs = scrape_story_arcs()
    cover_page_serials = scrape_cover_page_serials()
    non_canon_story_arcs = scrape_anime_only_story_arcs()
    content = "\n\n".join([page_title, story_arcs, cover_page_serials, non_canon_story_arcs])
    content = re.sub('\n\n+', '\n\n', content)
    content = re.sub('==+', "", content)
    content = re.sub('-----+', "", content)
    with open("story_arcs.md", "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
