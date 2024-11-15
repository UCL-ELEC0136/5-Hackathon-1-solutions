"""
This is the main module responsible for solving the tasks.
To solve each task just run `python main.py`.
"""

from dataclasses import dataclass
from typing import Any, Dict

import tyro
import pymongo


@dataclass
class TestArgs:
    team_name: str
    db_name: str = "hackathon-2024"
    server: str = (
        "mongodb+srv://student:submission@cluster0.0ryuw.mongodb.net/?retryWrites=true&w=majority"
    )


def is_equal(a: Any, b: Any, tol=0.05) -> bool:
    """Calculate if two objects are equal.
    If they are floats, check if they are equal within 5% tolerance.
    Otherwise, it uses the `==` operator.
    """
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol * a
    return a == b


def check_task(args: TestArgs, task_name: str):
    """
    Check the task solution for a given team against the reference solution.

    Args:
        args (TestArgs): The arguments containing team name, database name, and server URL.
        task_name (str): The name of the task to check.

    Returns:
        Dict[str, int]: A dictionary containing the scores for each statistic.
    """
    # read task solituion from MongoDB for all teams
    print("Collecting solutions...")
    client = pymongo.MongoClient(args.server)
    our_solution = client[args.db_name]["solutions"].find_one(
        {task_name: {"$exists": True}}
    )
    # finding teaching team solution
    if our_solution is None:
        print(f"Task {task_name} does not have solutions!")
        return
    our_solution = our_solution[task_name]

    # finding student team solution
    team_solutions = client[args.db_name][args.team_name].find_one(
        {task_name: {"$exists": True}}
    )
    if team_solutions is None:
        print(f"Team {args.team_name} did not submit solutions for task {task_name}!")
        return
    team_solutions = team_solutions[task_name]  # type: ignore
    print("Done.")
    print("Teaching team solution:", str(our_solution))
    print(f"Team {args.team_name} solution:", str(team_solutions))

    # check if the solution is correct
    print("Calculating scores...")
    scores = {}
    for statistic in our_solution:
        k_team_solution = team_solutions[statistic]
        k_our_solution = our_solution[statistic]
        # Check within 5% tolerance
        gain = is_equal(k_our_solution, k_team_solution, 0.05)
        scores[statistic] = int(gain)

    # calculate the score
    score = sum(scores.values())
    scores["total"] = score
    print(f"Done.")
    print("Scores are the following:", str(scores))
    print("Total score:", str(score))

    print(f"Team {args.team_name} scored {score}/{len(our_solution)}")
    # push the scores to mongo
    print("Pushing scores to MongoDB...")
    client[args.db_name]["scores"].update_one(
        {task_name: {"$exists": True}},
        {"$set": {args.team_name: {task_name: scores}}},
        upsert=True,
    )
    return


if __name__ == "__main__":
    args: TestArgs = tyro.cli(TestArgs)
    check_task(args, "task-1")
    check_task(args, "task-2")
