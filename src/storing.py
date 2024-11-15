"""This module implements a CRUD (Create, Read, Update, Delete) interface to our noSQL database."""

from typing import Optional, Tuple, List, Dict, Any, Union
import pymongo
from pymongo.mongo_client import MongoClient
import datetime


REPOSITORIES_COLLECTION_NAME = "repositories"
COMMITS_COLLECTION_NAME = "commits"


def get_mongo_credentials(filepath: Optional[str] = None) -> Tuple[str, str]:
    """
    Retrieve MongoDB credentials from a file or return default credentials.

    Args:
        filepath (Optional[str]): Path to the file containing the credentials.

    Returns:
        Tuple[str, str]: A tuple containing the username and password.
    """
    if filepath is None:
        return ("student", "assignment")

    # load password from disk
    with open(filepath, "r") as file:
        credentials = file.read().splitlines()

    username = credentials[0]
    password = credentials[1]
    return username, password


def get_mongo_client(host: str) -> MongoClient:
    """
    Create a MongoDB client.

    Args:
        host (str): The host address of the MongoDB client.

    Returns:
        MongoClient: A MongoDB client connected to the specified host.
    """
    # connect to your local mongo instance
    address = host
    client = pymongo.MongoClient(address)
    return client


def create(
    client: MongoClient,
    db_name: str,
    collection_name: str,
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
) -> Any:
    """
    Insert data into a specified collection in the MongoDB database.

    Args:
        client (MongoClient): The MongoDB client.
        data (List[Dict[str, Any]] | Dict[str, Any]): The data to be inserted.
        db_name (str): The name of the database.
        collection_name (str): The name of the collection.

    Returns:
        Any: The result of the insert operation.
    """
    # grab the collection you want to push the data into
    database = client[db_name]
    collection = database[collection_name]
    # push the data
    if isinstance(data, dict):
        return collection.insert_one(data)
    elif isinstance(data, list):
        return collection.insert_many(data)
    else:
        raise ValueError(
            f"Cannot create new record in {db_name}.{collection_name}. Invalid type for data: {type(data)}"
        )


def read(
    client: MongoClient,
    db_name: str,
    collection_name: str,
    query: Optional[List[Dict[str, Any]]],
) -> Any:
    """
    Retrieve data from a specified collection in the MongoDB database.

    Args:
        client (MongoClient): The MongoDB client.
        db_name (str): The name of the database.
        collection_name (str): The name of the collection.
        query (Optional[List[Dict[str, Any]]]): The query to filter the data.

    Returns:
        Any: The retrieved data.
    """
    # handle null inputs
    query = query or []

    # retrieve the data in `collection_name` that matches `query`
    data = client[db_name][collection_name].aggregate(query)

    return data


def contains_data(
    client: MongoClient, db_name: str, collection_name: str
) -> bool:
    """
    Check if a specified collection in the MongoDB database contains data.

    Args:
        client (MongoClient): The MongoDB client.
        db_name (str): The name of the database.
        collection_name (str): The name of the collection.

    Returns:
        bool: True if the collection contains data, False otherwise.
    """
    # check if database exists
    databases = client.list_database_names()
    if db_name not in databases:
        return False

    # check if collection exists
    collections = client[db_name].list_collection_names()
    if collection_name not in collections:
        return False

    # check if collection contains elements
    collection = client[db_name][collection_name]
    if collection.count_documents({}) <= 0:
        return False

    return True


def contains_repositories(client: MongoClient, db_name: str) -> bool:
    """
    Check if the repositories collection in the MongoDB database contains data.

    Args:
        client (MongoClient): The MongoDB client.
        db_name (str): The name of the database.

    Returns:
        bool: True if the repositories collection contains data, False otherwise.
    """
    return contains_data(client, db_name, REPOSITORIES_COLLECTION_NAME)


def create_repositories(
    client: MongoClient, db_name: str, repos: List[Dict[str, Any]]
) -> Any:
    """
    Insert repository data into the repositories collection in the MongoDB database.

    Args:
        client (MongoClient): The MongoDB client.
        repos (List[Dict[str, Any]]): The repository data to be inserted.
        db_name (str): The name of the database.

    Returns:
        Any: The result of the insert operation.
    """
    return create(client, db_name, REPOSITORIES_COLLECTION_NAME, repos)


def read_repositories(
    client: MongoClient,
    db_name: str,
    query: Optional[List[Dict[str, Any]]] = None,
) -> Any:
    """
    Retrieve repository data from the repositories collection in the MongoDB database.

    Args:
        client (MongoClient): The MongoDB client.
        query (Optional[List[Dict[str, Any]]]): The query to filter the data.
        db_name (str): The name of the database.

    Returns:
        Any: The retrieved repository data.
    """
    return read(client, db_name, REPOSITORIES_COLLECTION_NAME, query)


def contains_commits(client: MongoClient, db_name: str) -> bool:
    """
    Check if the commits collection in the MongoDB database contains data.

    Args:
        client (MongoClient): The MongoDB client.
        db_name (str): The name of the database.

    Returns:
        bool: True if the commits collection contains data, False otherwise.
    """
    return contains_data(client, db_name, COMMITS_COLLECTION_NAME)


def create_commits(
    client: MongoClient, db_name: str, commits: List[Dict[str, Any]]
) -> Any:
    """
    Insert commit data into the commits collection in the MongoDB database.

    Args:
        client (MongoClient): The MongoDB client.
        commits (List[Dict[str, Any]]): The commit data to be inserted.
        db_name (str): The name of the database.

    Returns:
        Any: The result of the insert operation.
    """
    return create(client, db_name, COMMITS_COLLECTION_NAME, commits)


def read_commits(
    client: MongoClient,
    db_name: str,
    query: Optional[List[Dict[str, Any]]] = None,
) -> Any:
    """
    Retrieve commit data from the commits collection in the MongoDB database.

    Args:
        client (MongoClient): The MongoDB client.
        query (Optional[List[Dict[str, Any]]]): The query to filter the data.
        db_name (str): The name of the database.

    Returns:
        Any: The retrieved commit data.
    """
    return read(client, db_name, COMMITS_COLLECTION_NAME, query)


def read_grouped_commits(
    client: MongoClient,
    db_name: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> Any:
    """
    Retrieve and group commit data by date from the commits collection in the MongoDB database.

    Args:
        client (MongoClient): The MongoDB client.
        start_date (datetime.datetime): The start date for the query.
        end_date (datetime.datetime): The end date for the query.
        db_name (str): The name of the database.

    Returns:
        Any: The grouped commit data.
    """
    query = [
        {"$addFields": {"date": "$commit.author.date"}},
        {"$project": {"date": {"$arrayElemAt": [{"$split": ["$date", "T"]}, 0]}}},
        {"$project": {"date": {"$toDate": "$date"}}},
        {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": "$date", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
        {"$project": {"date": "$_id", "count": "$count"}},
    ]
    commits = list(read(client, db_name, COMMITS_COLLECTION_NAME, query))

    # Ensure all dates from start_date to end_date are included
    date_counts = {commit['date']: commit['count'] for commit in commits}
    current_date = start_date
    result = []

    while current_date <= end_date:
        result.append({"date": current_date, "count": date_counts.get(current_date, 0)})
        current_date += datetime.timedelta(days=1)

    return result
