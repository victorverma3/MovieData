# Imports
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from itertools import chain
import random

# Setup
errors = []


# Program
async def get_movie_suggestion(u, session, overlap, num_suggestions):

    # asynchronously scrapes the user watchlists
    async def fetch_watchlist(user):
        print(f"\nScraping {user}'s watchlist...")
        watchlist = await get_watchlist(user, session)
        return watchlist

    watchlists = []
    tasks = [fetch_watchlist(user) for user in u]
    watchlists = await asyncio.gather(*tasks)

    if overlap == "y":
        # finds a random movie in common
        print(f"\nFinding movies in common across all watchlists...")
        common_watchlist = set(watchlists[0]).intersection(*watchlists[1:])
        if len(common_watchlist) == 0:
            raise Exception("No movies in common across all watchlists")
        common_watchlist = list(common_watchlist)
        print("\nRandomly choosing movie from common watchlist...")
        while num_suggestions > 0:
            try:
                suggestions = random.sample(common_watchlist, num_suggestions)
                break
            except ValueError:
                print("Not enough movies in common across all watchlists...")
                num_suggestions -= 1
                print(f"Trying {num_suggestions} suggestions instead...")
    elif overlap == "n":
        all_watchlists = list(chain(*watchlists))
        while num_suggestions > 0:
            try:
                suggestions = random.sample(all_watchlists, num_suggestions)
                break
            except ValueError:
                print("Not enough movies across all watchlists...")
                num_suggestions -= 1
                print(f"Trying {num_suggestions} suggestions instead...")

    if num_suggestions == 1:
        print(f"\nThe suggested movie is {suggestions}")
    else:
        print(f"\nThe {num_suggestions} suggested movies are {suggestions}")


async def get_watchlist(user, session=None):
    async def fetch_watchlist_page(page_number):
        async with session.get(
            f"https://letterboxd.com/{user}/watchlist/page/{page_number}"
        ) as page:
            soup = BeautifulSoup(await page.text(), "html.parser")
            movies = soup.select("li.poster-container")
            return [get_name(movie) for movie in movies]

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


async def get_name(movie):
    if not movie:
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
        more = input("\nAre there more users to consider (y or n): ")
        if more not in ["y", "n"]:
            raise ValueError("Input must be y or n")
        if more == "n":
            moreUsers = False

    overlap = input(
        "\nDo you only want to consider movies on all watchlists (y or n): "
    )
    if overlap not in ["y", "n"]:
        raise ValueError("Input must be y or n")

    num_suggestions = int(input("\nHow many suggestions do you want: "))
    if num_suggestions < 1:
        raise ValueError("Input must be greater than 0")

    if overlap == "y":
        async with aiohttp.ClientSession() as session:
            await get_movie_suggestion(users, session, overlap, num_suggestions)
    elif overlap == "n":
        async with aiohttp.ClientSession() as session:
            await get_movie_suggestion(users, session, overlap, num_suggestions)


if __name__ == "__main__":
    asyncio.run(main())
