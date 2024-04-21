# Imports
import ast
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from xgboost import XGBRegressor


# Data Processing
def create_genre_columns(row):
    # performs one-hot encoding for genres
    genres = [
        genre.lower().replace(" ", "_") for genre in ast.literal_eval(row["genres"])
    ]
    genre_options = [
        "action",
        "adventure",
        "animation",
        "comedy",
        "crime",
        "documentary",
        "drama",
        "family",
        "fantasy",
        "history",
        "horror",
        "music",
        "mystery",
        "romance",
        "science_fiction",
        "tv_movie",
        "thriller",
        "war",
        "western",
    ]

    for genre in genre_options:
        row[f"is_{genre}"] = 1 if genre in genres else 0

    return row


def assign_countries(row):
    # maps countries to numerical values
    country_map = {
        "USA": 0,
        "UK": 1,
        "China": 2,
        "France": 3,
        "Japan": 4,
        "Germany": 5,
        "South Korea": 6,
        "Canada": 7,
        "India": 8,
        "Austrailia": 9,
        "Hong Kong": 10,
        "Italy": 11,
        "Spain": 12,
        "Brazil": 13,
    }

    row["country_of_origin"] = (
        country_map[row["country_of_origin"]]
        if row["country_of_origin"] in country_map
        else len(country_map)
    )

    return row


def process(data):
    df = pd.read_csv(data)

    # renames all features for consistency
    df.rename(
        columns={column: column.lower().replace(" ", "_") for column in df.columns},
        inplace=True,
    )

    # creates boolean features for each genre
    df = df.apply(create_genre_columns, axis=1)

    # maps popular countries to numerical values
    df = df.apply(assign_countries, axis=1)

    # drops unnecessary features
    df.drop(
        columns=["rating_differential", "genres", "url"],
        inplace=True,
    )

    return df


# Model Training
def train_model(user_df, verbose=False):

    # creates user feature data
    X = user_df.drop(columns=["title", "user_rating"])

    # creates user target data
    y = user_df["user_rating"]

    # creates train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    # creates test-validation split
    X_test, X_val, y_test, y_val = train_test_split(
        X_test, y_test, test_size=0.5, random_state=0
    )

    # initializes XGBoost model
    model = XGBRegressor(enable_categorical=True)

    # performs k-fold cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    cv_results = cross_val_score(
        model, X_train, y_train, cv=kf, scoring="neg_mean_squared_error"
    )
    mse_cv = -cv_results.mean()

    # fits recommendation model on user training data
    model.fit(X_train, y_train)

    # prints accuracy evaluation values
    if verbose:
        print("Mean Squared Error with 5-fold Cross Validation:", mse_cv)

        y_pred_test = model.predict(X_test)
        mse_test = mean_squared_error(y_test, y_pred_test)
        print("Mean Squared Error on Test Set:", mse_test)

        y_pred_val = model.predict(X_val)
        mse_val = mean_squared_error(y_val, y_pred_val)
        print("Mean Squared Error on Validation Set:", mse_val)

        results_df = pd.DataFrame(
            {"actual_user_rating": y_val, "predicted_user_rating": y_pred_val.flatten()}
        )

        print(results_df)

    return model


# Recommendations
def recommend_n_movies(user, n):

    # defines people for whom there is data
    possible_users = [
        "chels33",
        "harryzielinski",
        "hgrosse",
        "jconn8",
        "juliamassey",
        "obiravioli",
        "pbreck",
        "rohankumar",
        "tmarro13",
        "victorverma",
    ]

    # defines other people (all those besides the user)
    other_users = [u for u in possible_users if u != user]

    # processes the user data
    data = f"./{user}/{user}_data.csv"
    user_df = process(data)
    print(f"\nprocessed user data")

    # trains recommendation model on processed user data
    model = train_model(user_df)
    print(f"\ncreated recommendation model")

    # creates df containing all movie data besides the user's
    other_dfs = []
    for u in other_users:
        other_dfs.append(process(f"./{u}/{u}_data.csv"))
    other_dfs_combined = pd.concat(other_dfs, ignore_index=True)

    # finds movies not seen by the user
    unseen = other_dfs_combined[
        ~other_dfs_combined["title"].isin(user_df["title"])
    ].copy()

    # creates unseen feature data
    X_unseen = unseen.drop(columns=["title", "user_rating"])

    # predicts user ratings for unseen movies
    predicted_ratings = model.predict(X_unseen)

    # trims prediction values to acceptable range
    unseen["predicted_rating"] = np.clip(predicted_ratings, 0.5, 5)

    # sorts predictions from highest to lowest user rating
    recommendations = unseen.sort_values(by="predicted_rating", ascending=False)[
        ["title", "release_year", "predicted_rating"]
    ].drop_duplicates(subset="title")

    return recommendations.iloc[:n]


if __name__ == "__main__":
    user = str(input(f"\nEnter a Letterboxd username: "))
    n = int(input(f"\nEnter the number of recommendations: "))
    if n < 1:
        raise Exception("number of recommendations must be an integer greater than 0")
    elif n > 100:
        raise Exception("number of recommendations cannot exceed 100")
    print(f"\nRecommendations:\n", recommend_n_movies(user, n).to_string(index=False))
