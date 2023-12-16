""" Scrape content from One Piece Wiki Chapter Pages"""

import re
import time
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
        soup = BeautifulSoup(response.content, "html.parser")
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
    return BeautifulSoup(str(table).replace("\n", ""))


def clean_markdown(elements):
    """ Clean markdown content """
    for i in range(len(elements)):
        if elements[i].name == "table":
            elements[i] = clean_markdown_table_util(elements[i])
        elif elements[i].name == "dl":
            elements[i] = BeautifulSoup("<p>" + str(elements[i]) + "</p>")
    return elements


def scrap_chapter(chapter_number):
    """ Scrape data from the website "https://onepiece.fandom.com/wiki/Chapter_1" """

    url = f"https://onepiece.fandom.com/wiki/Chapter_{chapter_number}"
    soup = collect_soup_util(url)

    header_content = "# " + md(str(soup.find("h1"))).strip()
    try:
        header_content += "\n\n" + md(str(soup.find(id='toc').find_previous_sibling('p')), strip=['a', 'img']).strip() + "\n\n"
    except:
        pass

    # Find the main content element
    ids = ["Cover_Page", "Short_Summary", "Long_Summary", "Characters", "References", "Site_Navigation"]
    start_element = None
    for cid in ids:
        start_element = soup.find(id=cid)
        if start_element is not None:
            start_element = start_element.parent
            break
    if start_element is None:
        return header_content
    end_element = soup.find(id="Characters").parent
    chapter = find_siblings_between_elements(start_element, end_element)
    chapter = clean_markdown(chapter)

    # Convert the HTML content to markdown
    content = "\n".join([md(str(arc), strip=['a', 'img']) for arc in chapter])
    content = header_content + "## " + md(str(start_element)) + "\n" + content
    content = re.sub('\n\n+', '\n\n', content)

    return content


def main():

    for chapter_number in range(1, 2):
        time.sleep(2)
        chapter_content = scrap_chapter(chapter_number)
        chapter_content = chapter_content.replace("[]", "")
        with open('chapter_' + str(chapter_number) + '.md', 'w') as f:
            f.write(chapter_content)


if __name__ == "__main__":
    main()
