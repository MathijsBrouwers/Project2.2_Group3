#pip install sentence-transformers
#pip install googlesearch-python beautifulsoup4 requests

from openai import OpenAI
from sentence_transformers import SentenceTransformer
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

def get_google_search_titles(query):
        # Perform a Google search and retrieve the titles of the top 10 results
        search_results = search(query, num_results=10)
        titles = []
        for url in search_results:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('title').get_text()
                titles.append(title)
            except Exception as e:
                # In case of any error, skip to the next result
                continue
        print(titles)
        return titles

get_google_search_titles("donald trump is a criminal")
