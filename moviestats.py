# Imports
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Program
def getStats(user):
    with open(f"{user}/{user}_data.csv") as path:
        userData = pd.read_csv(
            path, index_col=0, encoding="latin-1", encoding_errors="ignore"
        )

    # creates a json file in user directory containing the user's movie stats
    userStats = {
        "User Rating": {
            "Mean": round(userData["User Rating"].mean(), 3),
            "Standard Deviation": round(userData["User Rating"].std(), 3),
        },
        "Letterboxd Rating": {
            "Mean": round(userData["Letterboxd Rating"].mean(), 3),
            "Standard Deviation": round(userData["Letterboxd Rating"].std(), 3),
        },
        "Rating Differential": {
            "Mean": round(userData["Rating Differential"].mean(), 3)
        },
        "Letterboxd Rating Count": {
            "Mean": round(userData["Letterboxd Rating Count"].mean(), 3)
        },
    }
    with open(f"{user}/{user}_stats.json", "w") as f:
        json.dump(userStats, f, indent=4, ensure_ascii=False)

    visualizeData(user, userData)


def visualizeData(user, userData):
    sns.set_theme()

    ax = sns.kdeplot(
        data=[userData["User Rating"], userData["Letterboxd Rating"]], cut=0
    )

    ax.set(xlabel="Rating", ylabel="Count", title=f"{user}")
    plt.savefig(f"{user}/{user}_ratings.png")
