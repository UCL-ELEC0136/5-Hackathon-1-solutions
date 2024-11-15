## Task 1: Find the stargazers
Consider the empirical distribution represented by the number of stargazers (stars) in each repository in the organisation, https://github.com/google.
We seek the answers to the following questions:
1. What is the average number of stargazers per repository?
2. What is the standard deviation of the number of stargazers?
3.  What are the `5`, `10`, `25`, `75`, `90`, and `95` percentiles of the distribution?
4. What is the minimum number of stargazers for a repository?
5. What is the the maximum?
6. What is the **name** of the repository with the minimum number of stargazers?
7. What is the **name** of the repository with the maximum number of stargazers? 


## Submitting task 1
We will consider the task to be completed if the following conditions are met.
- There is a database called `hackathon-2024`
- In that database there is a collection with the name of your team. Your team name is the name of your repo, except the prefix `5-HACKATHON-1-`. For example, if your repo name is `5-HACKATHON-1-wonderful-Team`, your team name is `wonderful-team`. The collection is **always lowercase**.
- The collection contains the following document:
```json
{
  "task-1": {
    "mean": <mean number of stargazers count as float>,
    "std": <standard deviation of stargazers count as float>,
    "percentile_5": <5-percentile of stargazers count as integer>,
    "percentile_10": <10-percentile of stargazers count as integer>,
    "percentile_25": <25-percentile of stargazers count as integer>,
    "percentile_75": <75-percentile of stargazers count as integer>,
    "percentile_90": <90-percentile of stargazers count as integer>,
    "percentile_95": <95-percentile of stargazers coun as integert,
    "min": <minimum number of stargazers count as integer>,
    "max": <maximum number of stargazers count as integer>,
    "argmin": "<name of the repository with the minimum number of stargazers>",
    "argmax": "<name of the repository with the maximum number of stargazers>"
  }
}
```
