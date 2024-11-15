"""
This is the main module responsible for solving the tasks.
To solve each task just run `python main.py`.
"""

import datetime
from dataclasses import dataclass
import os
from typing import Optional

import tyro

import src.processing
import src.acquiring
import src.visualising
import src.storing


@dataclass
class Args:
    team_name: str = "Team-solutions"
    db_name: str = "hackathon-2024"
    server: str = (
        "mongodb+srv://student:submission@cluster0.0ryuw.mongodb.net/?retryWrites=true&w=majority"
    )
    github_token: Optional[str] = None


def task_1(args: Args) -> None:
    # make sure there's a figures directory
    os.makedirs("figures", exist_ok=True)

    client = src.storing.get_mongo_client(args.server)
    # check if mongo already contains repos
    if not src.storing.contains_repositories(client, args.db_name):
        # if not, acquire and store
        print("Acquiring repositories...")
        repos = src.acquiring.acquire_repositories("google")
        print("Done.")
        print("Pushing repositories to MongoDB...")
        src.storing.create_repositories(client, args.db_name, repos)
        print("Done.")

    # read repos from mongo
    print("Reading repositories from MongoDB...")
    repos = src.storing.read_repositories(client, args.db_name)
    print("Done.")

    # get stargazers count for each repo
    print("Calculating statistics...")
    stars = {}
    for repo in repos:
        repo_name = repo.get("name", "unknown repo")
        stargazers = repo.get("stargazers_count", 0)
        stars[repo_name] = stargazers

    distribution = list(stars.values())

    # calculate the statistics of the distribution
    stats = src.processing.statistics(distribution)
    # name of repo with minimum stars
    stats["argmin"] = min(stars, key=stars.get)  # type: ignore
    # name of repo with maximum stars
    stats["argmax"] = max(stars, key=stars.get)  # type: ignore
    print("Done. Statistics are the following " + str(stats))

    # push the statistics to mongo using *update* (not create) (CR*U*D)
    solution = {"task-1": stats}
    client[args.db_name][args.team_name].update_one(
        {"task-1": {"$exists": True}}, {"$set": solution}, upsert=True
    )

    # plot figures
    fig, _ = src.visualising.histogram(distribution)
    src.visualising.save_figure(fig, "figures/stars_histogram.png")

    fig, _ = src.visualising.boxplot(
        stats["mean"],
        stats["min"],
        stats["max"],
        stats["percentile_5"],
        stats["percentile_95"],
    )
    src.visualising.save_figure(fig, "figures/stars_boxplot_5-95.png")

    fig, _ = src.visualising.boxplot(
        stats["mean"],
        stats["min"],
        stats["max"],
        stats["percentile_10"],
        stats["percentile_90"],
    )
    src.visualising.save_figure(fig, "figures/stars_boxplot_10-90.png")

    fig, _ = src.visualising.boxplot(
        stats["mean"],
        stats["min"],
        stats["max"],
        stats["percentile_25"],
        stats["percentile_75"],
    )
    src.visualising.save_figure(fig, "figures/stars_boxplot_25-75.png")


def task_2(args: Args) -> None:
    # create a mongo client
    print("Establishing connection to MongoDB...")
    client = src.storing.get_mongo_client(args.server)
    print("Done.")

    # read auth token
    with open("src/github.token", "r") as file:
        token = file.read().splitlines()[0]

    # acquire data if not in mongo
    if not src.storing.contains_commits(client, args.db_name):
        print("Acquiring commits...")
        commits = src.acquiring.acquire_commits(
            "epignatelli", "navix", auth=(src.acquiring.USERNAME, token)
        )
        print("Done.")
        print("Pushing commits to MongoDB...")
        src.storing.create_commits(client, args.db_name, commits)
        print("Done.")

    # read commits and group them by day
    print("Reading commits from MongoDB...")
    start_date = datetime.datetime(2023, 11, 1)
    end_date = datetime.datetime(2024, 11, 1)
    commits = list(
        src.storing.read_grouped_commits(client, args.db_name, start_date, end_date)
    )
    print("Done.")

    # push the statistics to mongo using *update* (not create) (CR*U*D)
    print("Calculating statistics...")
    counts = [d["count"] for d in commits]
    avg = sum(counts) / len(counts)
    std = (sum((x - avg) ** 2 for x in counts) / len(counts)) ** 0.5
    solution = {
        "task-2": {
            "timeseries": counts,
            "average": avg,
            "std": std,
            "min": min(counts),
            "max": max(counts),
        }
    }
    print("Done. Solution is the following " + str(solution))
    print("Pushing solution to MongoDB...")
    client[args.db_name][args.team_name].update_one(
        {"task-2": {"$exists": True}}, {"$set": solution}, upsert=True
    )
    print("Done.")

    # plot the timeseries
    x = [d["date"] for d in commits]
    y = [d["count"] for d in commits]
    fig, _ = src.visualising.lineplot(x, y)
    src.visualising.save_figure(fig, "figures/timeseries.png")
    return


if __name__ == "__main__":
    args: Args = tyro.cli(Args)
    task_1(args)
    task_2(args)
