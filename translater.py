import requests
from bs4 import BeautifulSoup
from http import HTTPStatus

input_lang = input(
    'Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:\n'
)
word = input("Type the word you want to translate:\n")
print(f'You chose "{input_lang}" as the language to translate "{word}".')

convert={"en":"french-english","fr":"english-french"}
url = f"https://context.reverso.net/translation/{convert[input_lang]}/{word}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == HTTPStatus.OK:
    print(response.status_code,"OK")
    soup = BeautifulSoup(response.content, 'html.parser')
    example = soup.find(id="examples-content")
    print("Translations")
    tags = soup.find_all("span",class_="display-term")
    words=[]
    for tag in tags:
        word=tag.get_text().strip()
        words.append(word)
    print(words)
    sen_tags= example.find_all("span",class_="text")
    sens=[]
    for sen_tag in sen_tags:
        sen=sen_tag.get_text().strip()
        sens.append(sen)
    print(sens)

else:
    print(response.status_code)