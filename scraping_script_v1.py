import requests
from bs4 import BeautifulSoup
import time
import random
# import pandas as pd
# from urllib.parse import urlsplit

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/16.0',
    }
)

movie_num = 0
movies = {}

for page_num in range(2,3):
    reference_page_url = "http://www.allocine.fr/films/?page=" + str(page_num)
    print(reference_page_url)
    page_request = requests.get(reference_page_url, headers=headers)
    if page_request.status_code == 200:

        page = page_request.content
        soup = BeautifulSoup(page, "html.parser")

        for movie_zone in soup.find_all('div', {"class": "card entity-card entity-card-list cf"}):

            title = movie_zone.find('a', {"class": "meta-title-link"}).get_text()
            movies[title] = {"title": title}
            
            release = movie_zone.find('span', {"class": "date"})
            if release:
                movies[title]["release_date"] = release.get_text()
            
            revs = movie_zone.find_all('span', {"class": "stareval-note"})
            if len(revs) == 3:
                movies[title]["press"] = revs[0].text
                movies[title]["spect"] = revs[1].text
            elif len(revs) == 2:
                movies[title]["spect"] = revs[0].text
            
            print(f"{title}", movies[title])

    time.sleep(random.randrange(1, 4))

with open('./results.txt', 'w') as f:
    f.write(str(movies))
    print("Created 'results.txt'.")