# gh-contribution-api

A simple API for aggregating statistics about a GitHub user's repositories.

## Installation

`pip install -r requirements.txt`

GitHub's API only allows 600 requests from unauthenticated users. In order to ensure this rate limit is not exceeded, please create the configuration file:

`src/api/config.py`

with the contents:

`token = 'your_token'`

Instructions for creating a personal access token can be found [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## Usage

Run local server with 

`py server.py`

### Request
`GET /user_stats/{username}`

### Query Parameters

| Name   | Data Type | Description |
| ------ | --------- | ----------- |
| forked | boolean   | (Optional) If set to `false` will only include results from repositories that are not forked


### Example Request

`curl -i -H 'Accept:application/json' http://localhost:5000/user_stats/seantomburke`

### Response


    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 354
    Server: Werkzeug/2.0.3 Python/3.7.9
    Date: Wed, 09 Feb 2022 19:28:46 GMT

    {
        "num_repos": 87,
        "num_stargazers": 101,
        "num_forks": 65,
        "avg_repo_size": "10.1 MB",
        "languages": {
            "JavaScript": 31,
            "PHP": 12,
            "CSS": 7,
            "Objective-C": 6,
            "Java": 4,
            "Python": 3,
            "Arduino": 1,
            "EJS": 1,
            "HTML": 1,
            "VimL": 1,
            "C++": 1
        }
    }


## License
[MIT](https://choosealicense.com/licenses/mit/)