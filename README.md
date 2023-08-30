# MovieData

# Inspiration

I love watching movies, and the Letterboxd app allows me to log and rate
the movies I've watched. Most movies also have a Letterboxd community
rating, which is approximately the average of all Letterboxd user ratings
for that movie. Initially, I wanted to know how my ratings compared to the
community ratings, so I created this program in order to facilitate this
comparison. While working, however, I saw the potential to gather more
information, so I expanded the scope to ultimately create a dataset of key
metadata about the movies that I have rated on the Letterboxd app. I hope
to use this dataset one day as the basis for my own personal machine
learning movie recommendation algorithm that uses Letterboxd data as its source.

# Methodology

# Setup

The following libraries are required:

a. asyncio
b. aiohttp
c. Beautiful Soup
d. json
e. Matplotlib
f. os
g. pandas
h. seaborn
i. time

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

1. Title
2. User Rating (out of 5)
3. Letterboxd Rating (out of 5)
4. Rating Differential (User Rating - Letterboxd Rating)
5. Letterboxd Rating Count
6. Genres
7. Country of Origin
8. URL (link to movie page on Letterboxd)

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
