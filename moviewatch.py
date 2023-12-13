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
    async def fetch_watchlist_page(page_number):
        async with session.get(
            f"https://letterboxd.com/{user}/watchlist/page/{page_number}"
        ) as page:
            soup = BeautifulSoup(await page.text(), "html.parser")
            movies = soup.select("li.poster-container")
            return [getName(movie) for movie in movies]

    print("\nScraping random watchlist...")
    watchlist = []
    page_number = 1

    while True:
        titles = await fetch_watchlist_page(page_number)
        if not titles:  # Stop loop on empty page
            break
        watchlist.extend(await asyncio.gather(*titles))
        page_number += 1

    if not watchlist:
        raise Exception(
            f"The watchlist for {user} was empty. Please check the username."
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
