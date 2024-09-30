import string
import requests
from bs4 import BeautifulSoup
from http import HTTPStatus

# URL of the page to scrape
url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"

# Send the request to the website
response = requests.get(url)

# Check if the response status is OK
if response.status_code == HTTPStatus.OK:
    # Parse the webpage content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all article elements
    articles = soup.find_all('article')

    # Dictionary to store article titles and their URLs
    details = {}
    
    # Loop through all articles and filter for News articles
    for article in articles:
        # Check if the article type is News
        if article.find("span", class_="c-meta__type").get_text() == 'News':
            # Find the link to the article
            link_tag = article.find("a", attrs={"data-track-action": "view article"})
            if link_tag:
                title = link_tag.get_text().strip()
                url = link_tag.get("href")
                details[title] = url

    # List to store the names of saved articles
    saved_articles = []

    # Loop through the filtered articles to save their content
    for title, relative_url in details.items():
        # Create a sanitized filename by replacing non-alphabetic characters with underscores
        sanitized_title = "".join([letter if letter in string.ascii_letters else "_" for letter in title])

        # Construct the full article URL
        article_url = "https://www.nature.com" + relative_url

        # Send request to get article content
        article_response = requests.get(article_url)
        
        # Check if the article page loads successfully
        if article_response.status_code == HTTPStatus.OK:
            article_soup = BeautifulSoup(article_response.content, 'html.parser')

            # Extract the teaser paragraph from the article page
            teaser = article_soup.find("p", class_="article__teaser")
            if teaser:
                # Open a file to write the teaser content
                with open(sanitized_title + ".txt", "w", encoding='utf-8') as file:
                    file.write(teaser.get_text())
                
                # Add the filename to the list of saved articles
                saved_articles.append(sanitized_title + ".txt")

    # Print the list of saved articles
    print(f"Saved articles: {saved_articles}")

else:
    print(f"The URL returned {response.status_code}!")