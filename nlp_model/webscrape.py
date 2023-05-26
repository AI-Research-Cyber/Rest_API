import requests
from bs4 import BeautifulSoup
from typing import List
import re
CHARACTER_CUT_OFF = 20000

def extract_urls(text):
    url_regex = r"(https?://\S+)"
    urls = re.findall(url_regex, text)
    return urls

def remove_tags(soup: BeautifulSoup) -> str:
    for data in soup(["style", "script"]):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return " ".join(soup.stripped_strings)

def read_webpage(url: str) -> str:
    print(f"Getting the response from url : {url})")
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Get all the text content from the relevant HTML tags
    text_content = remove_tags(soup)

    # for tag in ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div"]:
    #     for element in soup.find_all(tag):
    #         text_content += element.get_text() + " "

    print(text_content)
    return text_content

def process_webpages(urls: List[str]):
    # A set to keep track of visited pages
    visited_pages = set()
    content = []
    try:
      for url in urls:
        aggregated_text = ""
        visited_pages.add(url)
        aggregated_text += f"\nGetting the content of {url}:\n"
        aggregated_text += read_webpage(url)
        content.append(aggregated_text)
    except:
      pass
    return content
