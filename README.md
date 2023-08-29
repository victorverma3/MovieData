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

# Fixing Errors

There are some movies/TV shows on Letterboxd that do not display the
desired data, or the layout of their webpage does not follow the typical
format of most Letterboxd pages. I have implemented try-except to to catch
these errors without interrupting the code, and the titles that cause an
error will be returned as a list by the filmCrawl() function. Optionally,
the user can add these titles to the avoid dictionary at the top of
moviedata.py, if they want to skip over them entirely in future passes of
the program.

# Output Files

Running gatherData() in moviedata.py creates a local csv file with the
following datapoints for the movies the user rated on Letterboxd:

1. Title
2. User Rating (out of 5)
3. Letterboxd Rating (out of 5)
4. Letterboxd Rating Count
5. Country of Origin

I've uploaded my own personal Letterboxd data, victordata.csv, as an
example.

Running stats() in moviestats.py creates a local csv file with the mean
and standard deviation for the user ratings, Letterboxd ratings, and
Letterboxd rating count. It also stores the variation between the user and
Letterboxd ratings (this is NOT to be confused with variance). The
variation of user ratings can be interpreted as the average difference of
(user rating - Letterboxd rating), and the variation of Letterboxd ratings
can be interpreted as the average difference of (Letterboxd rating - user
rating). The main reason I started this project was to calculate my own
variation for user rating - this tells me on average, how I rate a movie
compared to its Letterboxd rating. This is a summary of my personal
statistics:

- The average of my personal ratings of the movies I've watched is 3.622,
  while the Letterboxd rating for those same movies is 3.097.
- The standard deviation of my personal ratings is 0.720, while the
  standard deviation of the Letterboxd ratings is 0.689.
- On average, I tend to rate a movie 0.525 stars higher than the
  Letterboxd community.
- The average number of Letterboxd ratings for a movie I've rated is
  219268, with a standard deviation of 308464.

# Limitations

A small subsection of the movies/tv shows that a user might have rated do not have data
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
