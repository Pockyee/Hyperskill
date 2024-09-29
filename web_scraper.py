from http.client import responses

import requests
from bs4 import BeautifulSoup
from http import HTTPStatus
input_url = input("Input the URL:\n")
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
response = requests.get(input_url)
page_content = response.content
file = open('source.html', 'wb')
file.write(page_content)

print(response.ok)

if response.ok:
    print("Content saved.")
else:
    print(f"The URL returned {response.status_code}!")