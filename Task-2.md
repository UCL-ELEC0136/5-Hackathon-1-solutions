## Task 2: Time series
Now consider the https://github.com/epignatelli/navix repository.
We seek the answers to the following questions:
1. What is the number of commits per day in the repository between 01/11/2023 and 01/11/2024?
2. What is the average number of commits per day in the period?
3. What is the standard deviation of the number of commits per day in the period?
4. What is the minimum number of commits per day in the period?
5. What the maximum?

## Advices
- Acquire and store all commits first, then process them. This will allow you to avoid unnecessary requests to the GitHub API.
- There might be multiple commits in one day, you might need to group them.
- To group, you can use either the [mongo aggregation pipeline](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/) with the [group](https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/) operator, or Python directly.
- Using mongo queries will be more efficient and have higher scores from us.

## Submitting task 2
We will consider the task to be completed if the following conditions are met
- There is a database called `hackathon-2024`
- In that database there is a collection with the name of your team. Your team name is the name of your repo, except the prefix `5-HACKATHON-1-`. For example, if your repo name is `5-HACKATHON-1-wonderful-Team`, your team name is `wonderful-team`. The collection is **always lowercase**.
- The collection contains the following document:
```json
{
  "task-2": {
    "timeseries": <the number of commits per each day as an array of integers>,
    "average": <the average number of commits per day as a float>,
    "std": <the standard deviation of the number of commits per day as a float>,
    "min": <the minimum number of commits per day as an integer>,
    "max": <the maximum number of commits per day as an integer>
  }
}
```
