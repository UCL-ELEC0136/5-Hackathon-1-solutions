# Hackathon #1

Hello and welcome to your first hackathon of  UCL-ELEC0136, the Data Acquisition and Processing Systems course at UCL.


Unlike our usual labs, part of this exercise is designed to test your ability to solve a problem _ex tempore_ (not at home).
You have to solve 2 tasks, which you can find in the root of this repository ([`Task-1.md`](/Task-1.md) and [`Task-2.md`](/Task-2.md)), and you have 2 hours to complete them.
Your starting point is a text brief, detailing the tasks to solve with no initial code, and some instructions for submission.


## Required files
To allow automated grading, your repository must contain the following files:
- `environment.yml`: a conda environment file that specifies your Python version and installs the requirements.txt file. The environment name must be `daps-hackathon`.
- `requirements.txt`: a pip requirements file that specifies the Python libraries you use in your code.
- `main.py`: a Python file that contains and executes all the code necessary to complete the tasks.

Your final submission will need to have the following structure:
```plaintext
5-hackathon-1-your-team-name
    ├── figures
    │   ├── Figure-1.png
    │   └── ...
    ├── src
    │   ├── acqusition.py
    │   ├── preprocessing.py
    │   └── ...
    ├── .gitignore
    ├── environment.yml
    ├── LICENCE
    ├── main.pys
    ├── README.md
    ├── requirements.txt
    ├── Task-1.md
    └── Task-2.md
```



## Constraints
For each task, you must:
- No jupyter notebooks are allowed. You must write your code in plain Python files.
- Your code must be *reproducible* by us, by simply running `conda env create -f environment.yml && conda activate daps-hackathon && python main.py`
- Follow the [PEP8](https://peps.python.org/pep-0008/) guidelines to write good compliant code
- Use only the [GitHub API](https://docs.github.com/en/rest) and the `requests` python library to acquire any data, any wrapper around these (e.g. https://github.com/PyGithub/PyGithub) is not allowed


## Advices
### Advices for any hackathon
- You have a lot of work to do in very limited time. **We recommend you start by electing a team leader** that will be in charge of distributing subtasks to team members, coordinate integration, and supervise testing for reproducibility.
- Take some time to read through the handouts, and to **identify how you can split the workload**. This includes identifying the bottlenecks that will prevent the team from moving forward, and clearly defining the expected inputs and outputs (data type, structure) of your codebase's modules to allow multiple developper to work in parallel.
- **Keep your eye on the clock**, and make sacrifices if need be. Better to submit something inclomplete but reproducible before the deadline than not submitting anything at all because you started integration too late.
- Google, Google, Google! It is very likely that many before you have had the same exact question you have, seek the answer online!

### Advices for this specific hackathon
- If you hit [rate limits](https://docs.github.com/en/rest/rate-limit/rate-limit?apiVersion=2022-11-28), consider using authentication to increase the number of requests you can perform.
- You can perform an authenticated request as follows: `requests.get(url, auth=(username, token))`, where `token` is a [fine graded GitHub token](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2022-11-28#authenticating-with-a-personal-access-token) with read repo permissions, generated as explained in the Prerequisite section on Moodle.
- Remember that the GitHub API uses a pagination system, it might be a good idea to take a look at [this article](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api?apiVersion=2022-11-28) before solving `Task 1` and `Task 2`.
- MongoDB doesn't like `numpy` data types. Use normal python types like `int`or `float` by casting the array, for example `float(array)` if `array` is a scalar.
- Make sure that you only have one entry for each task on MongoDB, delete duplicates if you run the pipeline multiple times during integration, our use the `update` rather than `create` function of the CRUD (often called [`upsert`](https://en.wiktionary.org/wiki/upsert).

## Pushing to Mongo
Each task will ask you to push data to a MongoDB database. The database is shared amongst all users, so please be careful of the action you perform on it.
Detailed instructions on what to submit are provided in each task.

**Good luck, have fun! :rocket:**
