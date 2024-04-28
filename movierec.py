# Imports
import aiohttp
import asyncio
import database
from moviedata import movie_crawl
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from xgboost import XGBRegressor


# Model Training
def train_model(user_df, modelType="RF", verbose=False):

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

    # initializes model
    if modelType == "XG":
        model = XGBRegressor(
            enable_categorical=True, n_estimators=200, max_depth=3, learning_rate=0.05
        )
    elif modelType == "RF":
        model = RandomForestRegressor(
            random_state=0, max_depth=20, min_samples_split=10, n_estimators=100
        )

    # performs k-fold cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    cv_results = cross_val_score(
        model, X_train, y_train, cv=kf, scoring="neg_mean_squared_error"
    )
    mse_cv = -cv_results.mean()

    # fits recommendation model on user training data
    model.fit(X_train, y_train)

    # calculates mse on test data
    y_pred_test = model.predict(X_test)
    mse_test = mean_squared_error(y_test, y_pred_test)

    # calculates mse on validation data
    y_pred_val = model.predict(X_val)
    mse_val = mean_squared_error(y_val, y_pred_val)

    results_df = pd.DataFrame(
        {"actual_user_rating": y_val, "predicted_user_rating": y_pred_val.flatten()}
    )

    # prints accuracy evaluation values
    if verbose:
        print("Mean Squared Error with 5-fold Cross Validation:", mse_cv)
        print("Mean Squared Error on Test Set:", mse_test)
        print("Mean Squared Error on Validation Set:", mse_val)
        print(results_df)

    return model, mse_cv, mse_test, mse_val


# Recommendations
async def recommend_n_movies(user, n, update):
    # verifies parameters
    if n < 1 or n > 100:
        raise ValueError(
            "number of recommendations must be an integer between 1 and 100"
        )
    if update not in ["y", "n"]:
        raise ValueError("input must be y or n")

    # get a list of users with data in the database
    all_users = database.get_users_in_db()

    # defines other users (all those besides the current user)
    other_users = [u for u in all_users if u != user and u != "film_urls"]

    # gets the user data
    if update == "y":
        async with aiohttp.ClientSession() as session:
            user_df = await movie_crawl(user, session)
    elif update == "n":
        try:
            user_df = database.get_user_data(user)
        except ValueError:
            print(f"\nuser data does not exist - crawling Letterboxd...\n")
            async with aiohttp.ClientSession() as session:
                user_df = await movie_crawl(user, session)

    # trains recommendation model on processed user data
    model, _, _, _ = train_model(user_df)
    print(f"\ncreated recommendation model")

    # creates df containing all movie data besides the user's
    other_dfs = []
    for u in other_users:
        other_dfs.append(database.get_user_data(u))
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


async def main(user, n, update):
    recommendations = await recommend_n_movies(user, n, update)
    print(
        f"\nRecommendations:\n",
        recommendations.to_string(index=False),
    )


if __name__ == "__main__":
    user = str(input(f"\nEnter a Letterboxd username: "))
    n = int(input(f"\nEnter the number of recommendations: "))
    if n < 1 or n > 100:
        raise ValueError(
            "number of recommendations must be an integer between 1 and 100"
        )
    update = str(input(f"\nDo you want to use your latest data (y or n): "))
    if update not in ["y", "n"]:
        raise ValueError("input must be y or n")
    asyncio.run(main(user, n, update))
