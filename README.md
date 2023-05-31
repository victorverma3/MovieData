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
learning movie recommendation algorithm. 

# Methodology
First, I downloaded all of my Letterboxd ratings from the website. I've 
uploaded the file victorratings.csv as a sample of the Letterboxd ratings 
file that I used. Next, this file is read, and the title, user rating, and 
Letterboxd URI data is pulled. Each movie's Letterboxd URI is then scraped 
using BeautifulSoup in order to get the Letterboxd rating, the Letterboxd 
rating count, the genres, and the country of origin of the movie. These 
data points, along with the title and user rating, for each movie are 
added into a data dictionary with the titles as keys. This data dictionary 
is then output to a CSV file. I've uploaded the file victordata.csv as a 
sample of this CSV output. Finally, some summary statistics of the data 
are calculated and output to a second CSV file. I've uploaded the file 
victorstats.csv as a sample of this CSV output.

# Setup
First, the user must download their Letterboxd data from the website. Go 
to Account Settings --> Import & Export --> Export Your Data. They must 
then rename their ratings.csv file to fit the user's name; for example, I 
renamed ratings.csv to victorratings.csv. Optionally, the user should 
correct the spellings of the movies listed at the top of the moviedata.py 
file; this is because the Letterboxd data incorrectly spells them.

The following Python modules must be installed for this program to run: 
BeautifulSoup, concurrent.futures, json, matplotlib, os, pandas, requests, 
and time (see other tutorials online to install these). 

Next, the user should customize the path variable in the gatherData() 
function in moviedata.py with the local path to their Letterboxd ratings 
CSV (e.g. victorratings.csv). Be sure to not change the user variable in 
this path. For example, my path variable is path = f'./data/{user}ratings.csv'

Lastly, the user should create a folder in the same directory as 
moviedata.py and moviestats.py that shares the name of the user. For 
example, I have a folder called /victor. This is where the output files 
will be stored by the program.

Once all of this is done, the user can compile the moviedata.py file and 
call the gatherData() function with the parameter of the user's name (as a 
string) corresponding to their Letterboxd ratings file. For example, 
because my Letterboxd ratings file is called victorratings.csv, I would 
call gatherData('victor') in order to run the program on my ratings. The 
exact efficiency of my program is unknown because I don't know the runtime 
of the library functions that I am importing, but from personal experience 
I would estimate that it takes the program ~ 1 min per 700 films. Be sure 
to keep the program running uninterrupted (i.e. don't turn off your 
laptop) for the necessary time, or the program will error and you will 
have to run it again.

The gatherData() function also automatically uses the stats() function in 
moviestats.py to calculate some basic statistics about the data. To do so, 
the path variable in the stats() function should be set with the local 
path to the data CSV that was created in the previous step. For example, 
my path variable is path = f'./data/{user}ratings.csv'. Optionally, the user can also independently call the stats() 
function with the parameter of the user's name (as a string) corresponding 
to their Letterboxd data file, if their data has already been compiled. 
For example, because my data file is called victordata.csv, I would call 
stats('victor').

# Fixing Errors

There are some movies/TV shows on Letterboxd that do not display the 
desired data, or the layout of their webpage does not follow the typical 
format of most Letterboxd pages. I have implemented try-except to to catch 
these errors without interrupting the code, and the titles that cause an 
error will be returned as a list by the gatherData() function. Optionally, 
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

I've uploaded my own personal statistics, victorstats.csv, as an example.

Running stats() in moviestats.py also creates 3 pdfs that store histograms 
representing the user's movie data. UR.pdf, LR.pdf, and LRC.pdf store 
histograms displaying the distribution of the user ratings, Letterboxd 
ratings, and Letterboxd rating counts, respectively.

I've uploaded my own personal histograms, victorUR.pdf, victorLR.pdf, and 
victorLRC.pdf as examples.

# Limitations
A small subsection of the movies that I've rated do not have data 
available for all of the datapoints I desired. To keep the consistency of 
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
