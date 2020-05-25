import requests
from bs4 import BeautifulSoup
import time
import random
import re
# import pandas as pd
# from urllib.parse import urlsplit

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/16.0',
    }
)

movies = {}

for page_num in range(1,2):
    reference_page_url = "http://www.allocine.fr/films/?page=" + str(page_num)
    print("> Page:", reference_page_url)
    page_request = requests.get(reference_page_url, headers=headers)
    if page_request.status_code == 200:

        page = page_request.content
        soup = BeautifulSoup(page, "html.parser")

        for movie_zone in soup.find_all('div', {"class": "card entity-card entity-card-list cf"}):

            id = re.sub("\D", "", movie_zone.find("div", {"class": "content-title"}).a["href"])
            title = movie_zone.find('a', {"class": "meta-title-link"}).get_text()
            movies[id] = {"title": title}
            
            release = movie_zone.find('span', {"class": "date"})
            if release:
                movies[id]["release_date"] = release.get_text()

            meta = movie_zone.find('div', {"class": "meta-body-item meta-body-info"}).find_all('span', class_= re.compile(r".*==$"))
            if meta:
                movies[id]["genre"] = [e.text for e in meta]
            
            revs = movie_zone.find_all('span', {"class": "stareval-note"})
            if len(revs) == 3:
                movies[id]["press"] = revs[0].text
                movies[id]["spect"] = revs[1].text
            elif len(revs) == 2:
                movies[id]["spect"] = revs[0].text
            
            print(f"{title}", movies[id])
            print()
            print(movies)

    time.sleep(random.randrange(5, 12))

with open('./results.txt', 'w') as f:
    f.write(str(movies))
    print("Created 'results.txt'.")