import requests
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd
from datetime import datetime

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
                movies[id]["genres"] = ", ".join([e.text for e in meta])
            
            movie_directors = [
                link.text
                for link in movie_zone.find("div", {"class": "meta-body-item meta-body-direction light"}
                ).find_all(["a", "span"], class_=re.compile(r".*blue-link$"))
            ]
            movies[id]["directors"] = ", ".join(movie_directors)


            revs = movie_zone.find_all('span', {"class": "stareval-note"})
            if len(revs) == 3:
                movies[id]["press"] = revs[0].text.replace(",", ".")
                movies[id]["spect"] = revs[1].text.replace(",", ".")
            elif len(revs) == 2:
                movies[id]["spect"] = revs[0].text.replace(",", ".")
            
    time.sleep(random.randrange(2, 5))

df = pd.DataFrame.from_dict(movies, orient="index")
df["allocine_id"] = df.index
df.columns = ["TITLE", "RELEASE", "GENRES", "DIRECTORS", "PRESS_RATING", "PUB_RATING", "ALLOCINE_ID"]
# print(df)

now = datetime.now()
dt_string = now.strftime("%Y%m%d_%H:%M:%S")

df.to_csv("scraping-results" + dt_string + ".csv")
