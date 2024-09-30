import string
import requests
import os
from bs4 import BeautifulSoup
from http import HTTPStatus

# Input number of pages and article type
pages = input()
art_class = input()

for page in range(int(pages)):
    os.mkdir(f"Page_{page + 1}")

    # URL of the page to scrape
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=" + str(page + 1)

    # Request the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all articles on the page
        articles = soup.find_all('article')

        # Store article titles and URLs
        details = {}

        # Filter articles by type
        for article in articles:
            article_type_tag = article.find("span", class_="c-meta__type")
            if article_type_tag.get_text() == art_class:
                link_tag = article.find("a", attrs={"data-track-action": "view article"})
                if link_tag:
                    title = link_tag.get_text().strip()
                    relative_url = link_tag.get("href")
                    details[title] = relative_url

        # Store saved articles' filenames
        saved_articles = []

        # Save each filtered article's content
        for title, relative_url in details.items():
            sanitized_title = "".join(
                [letter if letter in (string.ascii_letters + string.digits) else "_" for letter in title])
            article_url = "https://www.nature.com" + relative_url

            # Request the article page
            article_response = requests.get(article_url)

            # Check if the article page was loaded successfully
            if article_response.status_code == HTTPStatus.OK:
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract and save the teaser content
                teaser = article_soup.find("p", class_="article__teaser")
                if teaser:
                    with open(f"Page_{page + 1}/" + sanitized_title + ".txt", "w", encoding='utf-8') as file:
                        file.write(teaser.get_text())
                    saved_articles.append(sanitized_title + ".txt")

        # Print saved articles' filenames
        print(f"Saved articles: {saved_articles}")

    else:
        print(f"The URL returned {response.status_code}!")

print("Saved all articles.")