# Imports
import pandas as pd
import sqlite3


# SQLite Database Operations
def store_data(data_dictionary):

    with sqlite3.connect("letterboxd_data.db") as conn:
        for user in data_dictionary:
            data_dictionary[user].to_sql(user, conn, if_exists="replace", index=False)


# gets the specified user's data from the database
def get_user_data(user):
    query = f"SELECT * FROM {user}"
    with sqlite3.connect("letterboxd_data.db") as conn:
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except:
            raise ValueError


# gets a list of all users in the database
def get_users_in_db():
    with sqlite3.connect("letterboxd_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        users = sorted([table[0] for table in tables])

    return users


# deletes a user's data from the database
def delete_data(user):
    with sqlite3.connect("letterboxd_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {user}")


if __name__ == "__main__":
    delete_data("test")
