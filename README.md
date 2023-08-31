# MovieData

# Inspiration

I love watching movies, and the Letterboxd app allows me to log and rate
the movies I've watched. Most movies also have a Letterboxd community
rating, which is a weighted average of all Letterboxd user ratings
for that movie. Initially, I wanted to know how my ratings compared to the
community ratings, so I created this program in order to facilitate this
comparison. While working, however, I saw the potential to gather more
information, so I expanded the scope to ultimately create a dataset of key
metadata about the movies that I have rated on the Letterboxd app. I hope
to use this dataset one day as the basis for my own personal machine
learning movie recommendation algorithm that uses Letterboxd data as its source.

# Methodology

**moviedata.py**

The program takes a Letterboxd username as its initial input. Based on the username, the program navigates to the user's Letterboxd web profile, and then scrapes all of the movies that the user has rated, as well as the URLs to each movie's individual Letterboxd page. Next, the program visits each page, and scrapes the following movie metadata:

1. _Title_
2. _User Rating_
3. _Letterboxd Rating_
4. _Letterboxd Rating Count_
5. _Genres_
6. _Country of Origin_
7. _URL_

Additionally, the _Rating Differential_ for each movie is also calculated by _User Rating_ - _Letterboxd Rating_. After all of the the metadata is gathered, it is stored in a dictionary. This data is then exported to a CSV file with the path _f./{user}/{user}\_data.csv'_. Any movies with missing data are appended to a list that is exported to a JSON file with the path _f.'{user}/{user}\_errors.json'_.

**moviestats.py**
The CSV file containing the user's movie metadata is read, and the mean and standard deviation of the _User Rating_ and _Letterboxd Rating_ is calculated. Furthermore, the program also finds the mean of the _Rating Differential_ and _Letterboxd Rating Count_. These stats are exported as JSON file with the path _f'{user}/{user}\_stats.json'_.

Finally, the _User Rating_ and _Letterboxd Rating_ stats are graphed as kernel density estimate plots, providing the user with a unique and useful visualization of how their movie ratings compare to the Letterboxd ratings. This graph is saved at the path _f'{user}/{user}\_ratings.png'_.

# Setup

**Running the Program on a Local Machine**

1. Ensure the following libraries are installed in your Python environment:

- asyncio
- aiohttp
- Beautiful Soup
- json
- Matplotlib
- os
- pandas
- seaborn
- time

2. Copy moviedata.py and moviestats.py into the same local directory.

3. Run moviedata.py and enter your Letterboxd username when prompted.

The program should take about n / 10 seconds to complete, where n is the number of movies that the user has rated on Letterboxd.

# Fixing Errors

There are some movies/TV shows on Letterboxd that do not display the
desired data, or the layout of their webpage does not follow the typical
format of most Letterboxd pages. I have implemented try-except to to catch
these errors without interrupting the code, and the titles that cause an
error will be returned as a list by the movieCrawl() function. Optionally,
the user can add these titles to the avoid dictionary at the top of
moviedata.py, if they want to skip over them entirely in future passes of
the program.

# Output Files

Running moviedata.py creates/updates the directory containing the user's movie data. This directory is updated with 4 files: {user}\_data.csv, {user}\_errors.json, {user}\_ratings.png, and {user}\_stats.json.

a) {user}\_data.csv contains the following data points for the movies that a user has rated:

1. _Title_
2. _User Rating_ (out of 5)
3. _Letterboxd Rating_ (out of 5)
4. _Rating Differential_ (User Rating - Letterboxd Rating)
5. _Letterboxd Rating Count_
6. _Genres_
7. _Country of Origin_
8. _URL_ (link to movie page on Letterboxd)

I've uploaded my own personal movie data, victorverma_data.csv, as an
example.

b) {user}\_errors.json contains the titles of all user entries on Letterboxd that did not have all of the desired data available on their Letterboxd pages.

c) {user}\_ratings.png shows an overlay of the kernel density estimate plots of both the user's movie ratings and the Letterboxd ratings of those same movies. This is a useful visual to aid the user in understanding how they typically rate movies compared to the average Letterboxd user.

d) {user}\_stats.json contains the mean of the user's user ratings, Letterboxd ratings, rating differentials, and Letterboxd rating counts. It also contains the standard deviation of the user ratings and Letterboxd ratings.

# Limitations

A small subsection of the movies that a user might have rated do not have data
available for all of the desired datapoints. To keep the consistency of
the csv, these movies were omitted from the data collection process. The
number of movies in this category are relatively small, so they likely
won't affect the data as a whole. This is generally more common with less
popular movies, however, so that could be a potential source of bias. It
is also assumed that the data follows a normal distibution for the purpose
of the summary statistics.

# What's Next?

This project will be used to help create a dataset of movie statistics
that will help me to create a custom movie recommendation algorithm using
machine learning that is based upon the user's Letterboxd data. As of
right now I plan to use cosine similarity and content-based filtering, but
this may change in the future. The project will be started at some point
in the future, likely after I take some university courses about machine
learning.
