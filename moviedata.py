# Imports
import ast
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from moviestats import getStats
import os
import pandas as pd
import re
import time

# Setup
unrated = []
errors = []
ratings = {
    "½": 0.5,
    "★": 1,
    "★½": 1.5,
    "★★": 2,
    "★★½": 2.5,
    "★★★": 3,
    "★★★½": 3.5,
    "★★★★": 4,
    "★★★★½": 4.5,
    "★★★★★": 5,
}
titles = []
years = []
runtimes = []
usrratings = []
lrs = []
ratingdiffs = []
lrcs = []
genres = []
countries = []
urls = []


# Program
async def movieCrawl(user, session=None):
    start = time.perf_counter()
    pageNumber = 1  # start scraping from page 1

    # asynchronously gathers the movie data
    while True:
        async with session.get(
            f"https://letterboxd.com/{user}/films/page/{pageNumber}"
        ) as page:
            soup = BeautifulSoup(await page.text(), "html.parser")
            movies = soup.select("li.poster-container")
            if movies == []:  # stops loop on empty page
                break
            tasks = [getData(movie, session, user) for movie in movies]
            await asyncio.gather(*tasks)
            pageNumber += 1

    # creates a new local directory for user if not already present
    if not os.path.exists(user):
        os.makedirs(user)

    # creates a json file in user directory containing the list of movies not rated by the user
    with open(f"{user}/{user}_unrated.json", "w") as f:
        unrated.sort()
        json.dump(unrated, f, indent=4, ensure_ascii=False)

    # creates a json file in user directory containing the list of movies causing errors
    with open(f"{user}/{user}_missing_data.json", "w") as f:
        errors.sort()
        json.dump(errors, f, indent=4, ensure_ascii=False)

    # creates a csv in user directory containing the movie data
    movies = {
        "Title": titles,
        "Release Year": years,
        "Runtime": runtimes,
        "User Rating": usrratings,
        "Letterboxd Rating": lrs,
        "Rating Differential": ratingdiffs,
        "Letterboxd Rating Count": lrcs,
        "Genres": genres,
        "Country of Origin": countries,
        "URL": urls,
    }
    df = pd.DataFrame(
        movies,
        columns=[
            "Title",
            "Release Year",
            "Runtime",
            "User Rating",
            "Letterboxd Rating",
            "Rating Differential",
            "Letterboxd Rating Count",
            "Genres",
            "Country of Origin",
            "URL",
        ],
    )
    path = f"./{user}/{user}_data.csv"
    df.sort_values(by="Title", ascending=True, inplace=True)
    df.to_csv(path, index=False)

    await session.close()

    finish = time.perf_counter()
    print(f"\nScraped {user}'s movie data in {finish - start} seconds\n")
    print(f"The following movies were not rated by {user}:\n{unrated}\n")
    print(f"The following movies were missing data on Letterboxd:\n{errors}\n")


async def getData(movie, session, user):
    title = movie.div.img.get("alt")
    print(title)
    link = f'https://letterboxd.com/{movie.div.get("data-target-link")}'

    # asynchronously gets Letterboxd data for movie
    LetterboxdData = await getLetterboxdData(title, link, session)

    # appends Letterboxd data to movies array
    if LetterboxdData:
        try:
            r = ratings[movie.p.span.text]
        except:
            # appends unrated movies to unrated array
            print(f"{title} is not rated by {user}")
            unrated.append(title)
            return
        lr = LetterboxdData["LR"]
        titles.append(title)
        years.append(LetterboxdData["YR"])
        runtimes.append(LetterboxdData["RT"])
        usrratings.append(r)
        lrs.append(lr)
        ratingdiffs.append(round(r - lr, 3))
        lrcs.append(LetterboxdData["LRC"])
        genres.append(LetterboxdData["G"])
        countries.append(LetterboxdData["COO"])
        urls.append(link)


async def getLetterboxdData(title, link, session):
    async with session.get(link) as page:
        soup = BeautifulSoup(await page.text(), "html.parser")
        script = str(soup.find("script", {"type": "application/ld+json"}))
        script = script[52:-20]  # trimmed to useful json data
        try:
            webData = json.loads(script)
        except:
            # appends movies causing error to errors array
            print(f"error while scraping {title}")
            errors.append(title)

            return

    # scrapes relevant Letterboxd data from each page if possible
    data = {}
    try:
        data["YR"] = int(webData["releasedEvent"][0]["startDate"])
        data["RT"] = re.search(
            r"(\d+)\s+mins", soup.find("p", {"class": "text-footer"}).text
        ).group(1)
        data["LR"] = webData["aggregateRating"]["ratingValue"]  # Letterboxd rating
        data["LRC"] = webData["aggregateRating"][
            "ratingCount"
        ]  # Letterboxd rating count
        data["G"] = webData["genre"]  # genres
        data["COO"] = webData["countryOfOrigin"][0]["name"]  # country of origin
    except:
        # appends movies with incomplete data to errors array
        print(f"{title} is missing data")
        errors.append(title)

        return
    return data


async def main(users):
    for user in users:
        async with aiohttp.ClientSession() as session:
            await movieCrawl(user, session)
        getStats(user)


if __name__ == "__main__":
    users = []
    while True:
        users.append(str(input("\nEnter a Letterboxd username: ")))
        moreUsers = str(input("\nAre there more users to scrape (y or n): "))
        if moreUsers == "n":
            break
    asyncio.run(main(users))
