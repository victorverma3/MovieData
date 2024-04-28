# Imports
import pandas as pd
import sqlite3


# stores a user's data in the database
def store_data(data_dictionary):

    try:
        with sqlite3.connect("letterboxd_data.db") as conn:
            for user in data_dictionary:
                data_dictionary[user].to_sql(
                    user, conn, if_exists="replace", index=False
                )
    except Exception as e:
        print(e)


# gets a user's data from the database
def get_user_data(user):

    query = f"SELECT * FROM {user}"

    with sqlite3.connect("letterboxd_data.db") as conn:
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except:
            raise ValueError("failed to get user data from database")


# gets a list of all users in the database
def get_users_in_db():

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        users = sorted([table[0] for table in tables])

    return users


# deletes a user's data from the database
def delete_data(db, user):

    if db == "main":
        db = "letterboxd_data.db"

    with sqlite3.connect(f"{db}") as conn:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {user}")


# stores the user rating data in the database
def update_user_ratings(user, user_df):

    with sqlite3.connect("users.db") as conn:
        user_df.to_sql(user, conn, if_exists="replace", index=False)


# gets the table of movie urls in the database
def get_movie_urls():

    query = f"SELECT * FROM movie_urls"

    with sqlite3.connect("data.db") as conn:
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except:
            raise ValueError("failed to get missing urls from database")


# updates the table of movie urls in the database
def update_movie_urls(urls_df):

    with sqlite3.connect("data.db") as conn:

        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='movie_urls'"
        )
        table_exists = cursor.fetchone()

        if table_exists:
            current_urls = pd.read_sql("SELECT * FROM movie_urls", conn)
        else:
            current_urls = pd.DataFrame(columns=["movie_id", "title", "url"])

        updated_urls = pd.concat([current_urls, urls_df], ignore_index=True)
        updated_urls.drop_duplicates(subset="movie_id", inplace=True)
        updated_urls = updated_urls.sort_values(by="title").reset_index(drop=True)

        updated_urls.to_sql("movie_urls", conn, if_exists="replace", index=False)

        conn.commit()


# gets the movie data from the database
def get_movie_data():

    query = f"SELECT * FROM movie_data"

    try:
        with sqlite3.connect("data.db") as conn:
            movie_data = pd.read_sql_query(query, conn)
            return movie_data
    except Exception as e:
        print(e)


# updates the movie data in the database
def update_movie_data(movie_df):

    try:
        with sqlite3.connect("data.db") as conn:
            movie_df.to_sql("movie_data", conn, if_exists="replace", index=False)
    except Exception as e:
        print(e)


# updates the table of missing movie data in the database
def update_missing_urls(missing_df):

    with sqlite3.connect("data.db") as conn:

        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='missing_urls'"
        )
        table_exists = cursor.fetchone()

        if table_exists:
            current_missing = pd.read_sql("SELECT * FROM missing_urls", conn)
        else:
            current_missing = pd.DataFrame(columns=["movie_id", "title", "url"])

        updated_urls = pd.concat([current_missing, missing_df], ignore_index=True)
        updated_urls.drop_duplicates(subset="movie_id", inplace=True)
        updated_urls = updated_urls.sort_values(by="title").reset_index(drop=True)

        updated_urls.to_sql("missing_urls", conn, if_exists="replace", index=False)

        conn.commit()


# updates the table of error movie data in the database
def update_error_urls(errors_df):

    with sqlite3.connect("data.db") as conn:

        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='error_urls'"
        )
        table_exists = cursor.fetchone()

        if table_exists:
            current_errors = pd.read_sql("SELECT * FROM error_urls", conn)
        else:
            current_errors = pd.DataFrame(columns=["movie_id", "title", "url"])

        updated_urls = pd.concat([current_errors, errors_df], ignore_index=True)
        updated_urls.drop_duplicates(subset="movie_id", inplace=True)
        updated_urls = updated_urls.sort_values(by="title").reset_index(drop=True)

        updated_urls.to_sql("error_urls", conn, if_exists="replace", index=False)

        conn.commit()
