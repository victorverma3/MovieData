# MovieData

# Inspiration

I love watching movies, and the Letterboxd app allows me to log and rate
the movies I've watched. Most movies also have a Letterboxd community
rating, a weighted average of all Letterboxd user ratings
for that movie. Initially, I wanted to know how my ratings compared to the
community ratings, so I created this program to facilitate this
comparison. While working, however, I saw the potential to gather more
information, so I expanded the scope to create a dataset of key
metadata about the movies I rated on the Letterboxd app. I plan
to use this dataset one day as the basis for a machine-learning movie recommendation algorithm that uses Letterboxd data as its source.

# Methodology

**moviedata.py**

The program takes a Letterboxd username as its initial input. Based on the username, the program navigates to the user's Letterboxd web profile and then scrapes all of the movies that the user has rated, as well as the URLs to each movie's individual Letterboxd page. Next, the program visits each page, and scrapes the following movie metadata:

1. `Title`
2. `User Rating`
3. `Letterboxd Rating`
4. `Letterboxd Rating Count`
5. `Genres`
6. `Country of Origin`
7. `URL`

Additionally, the `Rating Differential` for each movie is also calculated by `User Rating` - `Letterboxd Rating`. After all of the metadata is gathered, it is stored in a dictionary. This data is then exported to a CSV file with the path `./<user>/<user>data.csv`. Any movies with missing data are appended to a list that is exported to a JSON file with the path `./<user}/<user>errors.json`.

**moviestats.py**

The CSV file containing the user's movie metadata is read, and the mean and standard deviation of the `User Rating` and `Letterboxd Rating` are calculated. Furthermore, the program also finds the mean of the `Rating Differential` and `Letterboxd Rating Count`. These stats are exported as JSON files with the path `./<user>/<user>stats.json`.

Finally, the `User Rating` and `Letterboxd Rating` stats are graphed as kernel density estimate plots, providing the user with a unique and useful visualization of how their movie ratings compare to the Letterboxd ratings. This graph is saved at the path `./<user>/<user>ratings.png`.

# Setup

**Getting Started**

1. Clone the repository to your local machine.
2. Run `pip install -r ./requirements.txt` in the terminal in the main project directory.

**Movie Data and Stats**

1. Run `moviedata.py` and enter your Letterboxd username when prompted.
2. The output files will be created in a folder called `./<username>`, where `<username>` is the Letterboxd username from step 1.

The program should take about n / 10 seconds to complete, where n is the number of movies that the user has rated on Letterboxd.

# Fixing Errors

There are some movies/TV shows on Letterboxd that do not display the
desired data, or the layout of their web pages does not follow the typical
format of most Letterboxd pages. I have implemented try-except to catch
these errors without interrupting the code, and the titles that cause an
error will be returned as a list by the `movieCrawl()` function. Optionally,
the user can add these titles to the avoid dictionary at the top of
`moviedata.py`, if they want to skip over them entirely in future passes of
the program.

# Output Files

Running `moviedata.py` creates/updates the directory containing the user's movie data. This directory is updated with 4 files: `<user>data.csv`, `<user>errors.json`, `<user>ratings.png`, and `<user>stats.json`.

a) `<user>data.csv` contains the following data points for the movies that a user has rated:

1. `Title`
2. `User Rating` (out of 5)
3. `Letterboxd Rating` (out of 5)
4. `Rating Differential` (`User Rating` - `Letterboxd Rating`)
5. `Letterboxd Rating Count`
6. `Genres`
7. `Country of Origin`
8. `URL` (link to movie page on Letterboxd)

I've uploaded my movie data, `victorverma_data.csv`, as an
example.

b) `<user>errors.json` contains the titles of all user entries on Letterboxd that did not have all of the desired data available on their Letterboxd pages.

c) `<user>ratings.png` shows an overlay of the kernel density estimate plots of both the user's movie ratings and the Letterboxd ratings of those same movies. This is a useful visual to aid the user in understanding how they typically rate movies compared to the average Letterboxd user.

d) `<user>stats.json` contains the mean of the user's user ratings, Letterboxd ratings, rating differentials, and Letterboxd rating counts. It also contains the standard deviation of the user ratings and Letterboxd ratings.

# Limitations

A small subsection of the movies that a user might have rated does not have data
available for all of the desired data points. To keep the consistency of
the csv, these movies were omitted from the data collection process. The
number of movies in this category is relatively small, so they likely
won't affect the data as a whole. This is generally more common with less
popular movies, however, so that could be a potential source of bias. It
is also assumed that the data follows a normal distribution for the summary statistics.

# What's Next?

This project will be used to help create a dataset of movie statistics
that will help me create a custom movie recommendation algorithm using
machine learning that is based on the user's Letterboxd data. I plan to use singular value decomposition (SVD).
