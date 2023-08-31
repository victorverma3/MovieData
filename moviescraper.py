# Imports
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from moviestats import getStats
import json
import os
import pandas as pd
import time

# Setup
errors = []
ratings = {
    '½': 0.5,
    '★': 1,
    '★½': 1.5,
    '★★': 2,
    '★★½': 2.5,
    '★★★': 3,
    '★★★½': 3.5,
    '★★★★': 4,
    '★★★★½': 4.5,
    '★★★★★': 5
}
titles = []
usrratings = []
lrs = []
ratingdiffs = []
lrcs = []
genres = []
countries = []
urls = []

# Program
async def movieCrawl(user, session = None):
    start = time.perf_counter()
    pageNumber = 1 # start scraping from page 1

    # asynchronously gathers the movie data
    while True:
        async with session.get(f'https://letterboxd.com/{user}/films/page/{pageNumber}') as page:
            soup = BeautifulSoup(await page.text(), 'html.parser')
            movies = soup.select('li.poster-container')
            if movies == []: # stops loop on empty page
                break
            tasks = [getData(movie, session) for movie in movies]
            await asyncio.gather(*tasks)
            pageNumber += 1

    # creates a new local directory for user if not already present
    if not os.path.exists(user):
        os.makedirs(user)

    # creates a json file in user directory containing the list of movies causing errors
    with open(f'{user}/{user}_errors.json', 'w') as f:
        errors.sort()
        json.dump(errors, f, indent = 4, ensure_ascii = False)
    
    # creates a csv in user directory containing the movie data
    movies = {
        'Title': titles,
        'User Rating': usrratings,
        'Letterboxd Rating': lrs,
        'Rating Differential': ratingdiffs,
        'Letterboxd Rating Count': lrcs,
        'Genres': genres,
        'Country of Origin': countries,
        'URL': urls,
    }
    df = pd.DataFrame(movies, columns = ['Title', 
                                       'User Rating', 
                                       'Letterboxd Rating',
                                       'Rating Differential', 
                                       'Letterboxd Rating Count', 
                                       'Genres', 
                                       'Country of Origin',
                                       'URL'])
    path = f'./{user}/{user}_data.csv'
    df.to_csv(path, index = 'False')

    await session.close()

    finish = time.perf_counter()
    print(f'\nScraped movie data for {user} in {finish - start} seconds\n')
    print(f'The following movies caused errors (likely due to missing data on Letterboxd):\n{errors}\n')

async def getData(movie, session):
    title = movie.div.img.get('alt')
    print(title)   
    link = f'https://letterboxd.com/{movie.div.get("data-target-link")}'
    LetterboxdData = await getLetterboxdData(title, link, session) # asynchronously gets Letterboxd data for movie
    
    # appends Letterboxd data to movies array
    if LetterboxdData:
        r = ratings[movie.p.span.text]
        lr = LetterboxdData['LR']
        
        titles.append(title)
        usrratings.append(r)
        lrs.append(lr)
        ratingdiffs.append(round(r - lr, 3))
        lrcs.append(LetterboxdData['LRC'])
        genres.append(LetterboxdData['G'])
        countries.append(LetterboxdData['COO'])
        urls.append(link)
        
async def getLetterboxdData(title, link, session):
    async with session.get(link) as page:
        soup = BeautifulSoup(await page.text(), 'html.parser')
        script = str(soup.find('script', {'type': 'application/ld+json'}))
        script = script[52:-20] # trimmed to useful json data
        try:
            webData = json.loads(script)
        except:
            pass

    # scrapes relevant Letterboxd data from each page if possible
    data = {}
    try:
        data['LR'] = webData['aggregateRating']['ratingValue'] # Letterboxd rating
        data['LRC'] = webData['aggregateRating']['ratingCount'] # Letterboxd rating count
        data['G'] = webData['genre'] # genres
        data['COO'] = webData['countryOfOrigin'][0]['name'] # country of origin
    except:
        print(f'{title} is missing data')
        errors.append(title) # appends movies with incomplete data to errors array
        return
    return data

async def main(user):
    async with aiohttp.ClientSession() as session:
        await movieCrawl(user, session)
    getStats(user)

asyncio.run(main(user = input('\nEnter your Letterboxd username: ')))