# Imports
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import random

# Setup
errors = []


# Program
async def getMovieSuggestion(user, session):
    watchlist = await getWatchlist(user, session)
    print("\nRandomly choosing movie from watchlist...")
    suggestion = random.choice(watchlist)
    print(f"\nThe suggested movie is {suggestion} from {user}'s watchlist\n")


async def getWatchlist(user, session=None):
    print("\nScraping random watchlist...")
    watchlist = []
    pageNumber = 1  # start scraping from page 1

    # asynchronously gathers the watchlist data
    while True:
        async with session.get(
            f"https://letterboxd.com/{user}/watchlist/page/{pageNumber}"
        ) as page:
            soup = BeautifulSoup(await page.text(), "html.parser")
            movies = soup.select("li.poster-container")
            if movies == []:  # stops loop on empty page
                break
            tasks = [getName(movie) for movie in movies]
            titles = await asyncio.gather(*tasks)
            watchlist.extend(titles)
            pageNumber += 1

    await session.close()
    if watchlist == []:
        raise Exception(
            f"The watchlist for {user} was empty. Please check for typos in the usernames and try again."
        )
    return watchlist


async def getName(movie):
    if movie == None:
        return None
    title = movie.div.img.get("alt")
    return title


async def main():
    print(
        "\nThis program will take a group of Letterboxd usernames as input, and then randomly suggest a movie from any of the watchlists"
    )
    users = []
    moreUsers = True
    while moreUsers:
        username = input("\nEnter Letterboxd username: ")
        users.append(username)
        print(f"\nUsers currently in consideration: {users}")
        more = input("\nAre there more users to consider (Y or N): ")
        if more not in ["Y", "N"]:
            raise Exception("Input must be Y or N")
        if more == "N":
            moreUsers = False
    user = random.choice(users)
    async with aiohttp.ClientSession() as session:
        await getMovieSuggestion(user, session)


asyncio.run(main())
