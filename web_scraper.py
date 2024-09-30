import string
from http.client import responses
from os import close
from re import findall

import requests
from bs4 import BeautifulSoup
from http import HTTPStatus

url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
# headers = {"Accept": "text/plain"}
# response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
# if response and "nature.com" in url:
#     soup = BeautifulSoup(response.content, 'html.parser')
#     titles = soup.head.find('title')
#     summary = soup.find('meta',{'name': 'description'})
#     dictionary = {"title":titles.get_text(), "description":summary.get('content')}
#     print(dictionary)
# else:
#     print("Invalid page!")
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
articles = soup.find_all("article")

details = {}
for detail in articles:
    if detail.find("span", class_="c-meta__type").contents == ["News"]:
        x = detail.find("a", attrs={"data-track-action": "view article"})
        details[x.contents[0]] = x.get("href")
saved_articles = []
for title in details:
    new_title = ""
    for letter in title:
        if letter not in string.ascii_letters:
            new_title += "_"
        else:
            new_title += letter
    article_url = "https://www.nature.com" + details[title]
    article_soup = BeautifulSoup(requests.get(article_url).content, "html.parser")
    file = open(new_title + ".txt", "w")
    file.write(article_soup.find("p", class_="article__teaser").contents[0])
    file.close()
    saved_articles.append(new_title + ".txt")
print(f"Saved articles: {saved_articles}")
# page_content = response.content
# file = open('source.html', 'wb')
# file.write(page_content)
#
# print(response.ok)
#
# if response.ok:
#     print("Content saved.")
# else:
#     print(f"The URL returned {response.status_code}!")
