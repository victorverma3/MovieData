# Imports
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import random

# Setup
errors = []


# Program
async def getMovieSuggestion(u, session, overlap):
    if overlap == "Y":
        watchlists = []

        # asynchronously scrapes the user watchlists
        async def fetch_watchlist(user):
            print(f"\nScraping {user}'s watchlist...")
            watchlist = await getWatchlist(user, session)
            return watchlist

        tasks = [fetch_watchlist(user) for user in u]
        watchlists = await asyncio.gather(*tasks)

        # finds a random movie in common
        print(f"\nFinding movies in common across all watchlists...")
        common_watchlist = set(watchlists[0]).intersection(*watchlists[1:])
        if len(common_watchlist) == 0:
            raise Exception("No movies in common across all watchlists")
        common_watchlist = list(common_watchlist)
        print("\nRandomly choosing movie from common watchlist...")
        suggestion = random.choice(common_watchlist)
        print(f"\nThe suggested movie is {suggestion}")

    # scrapes a random watchlist and chooses a random movie from it
    elif overlap == "N":
        print("\nScraping random watchlist...")
        watchlist = await getWatchlist(u, session)
        print("\nRandomly choosing movie...")
        suggestion = random.choice(watchlist)
        print(f"\nThe suggested movie is {suggestion} from {u}'s watchlist\n")


async def getWatchlist(user, session=None):
    async def fetch_watchlist_page(page_number):
        async with session.get(
            f"https://letterboxd.com/{user}/watchlist/page/{page_number}"
        ) as page:
            soup = BeautifulSoup(await page.text(), "html.parser")
            movies = soup.select("li.poster-container")
            return [getName(movie) for movie in movies]

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
    title = movie.div.img.get("alt")  # gets movie title
    return title


async def main():
    print(
        "\nThis program will take a group of Letterboxd usernames as input, and then randomly suggest a movie from the watchlists"
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

    overlap = input(
        "\nDo you only want to consider movies on all watchlists (Y or N): "
    )
    if overlap not in ["Y", "N"]:
        raise Exception("Input must be Y or N")

    if overlap == "Y":
        async with aiohttp.ClientSession() as session:
            await getMovieSuggestion(users, session, overlap)
    elif overlap == "N":
        user = random.choice(users)
        async with aiohttp.ClientSession() as session:
            await getMovieSuggestion(user, session, overlap)


asyncio.run(main())
