
import requests
from bs4 import BeautifulSoup
from itertools import chain
import sys
import re


def get_results(language, word):

    if language == "en":
        lang_to, lang_from = "english", "french"
    else:
        lang_to, lang_from = "french", "english"
    url = f"https://context.reverso.net/translation/{lang_from}-{lang_to}/{word}"
    user_agent = 'Mozilla/5.0'
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': user_agent})
    except requests.exceptions.ReadTimeout:
        return "Connection error", "Connection error"
    except requests.exceptions.ConnectionError:
            return "Connection error", "Connection error"

    raw_contents = BeautifulSoup(response.content, 'html.parser')
    # translate words
    translations = raw_contents.find_all('span', {'class': 'display-term'})
    # example sentences
    sentences_src, sentences_target = \
        raw_contents.find_all('div', {"class": "src ltr"}), raw_contents.find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})

    translations = set([translation.get_text().strip() for translation in translations])
    sentences = set([sentence.get_text().strip() for sentence in
                    list(chain(*[sentence_pair for sentence_pair in zip(sentences_src, sentences_target)]))])

    return translations, sentences

print(get_results("fr","hello"))