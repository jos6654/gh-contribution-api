from more_itertools import last
import requests
import dateutil.parser
from .config import token

header = {'Authorization': 'token %s' % token}


def collect_stats(username, forked):

    stats = {}
    page = 1
    last_page = False
    repositories = []
    while not last_page:
        res = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100&page={page}", headers=header)
        if forked:
            repositories.extend(res.json())
        else:
            for repo in res.json():
                if not repo["fork"]: repositories.append(repo)
        
        page += 1   
        if len(res.json()) < 100: last_page = True
    
    stats["num_repos"], stats["languages"] = len(repositories), {}
    stats["num_stargazers"] = stats["num_forks"] = stats["avg_repo_size"] = 0
    for repo in repositories:
        stats["num_stargazers"] += repo["stargazers_count"]
        stats["num_forks"] += repo["forks_count"]
        stats["avg_repo_size"] += repo["size"]
        stats["languages"][repo["language"]] = stats["languages"].setdefault(repo["language"], 0) + 1

    stats["avg_repo_size"] = int(stats["avg_repo_size"]/stats["num_repos"])

    return stats
    # A list of languages with their counts, sorted by the most used to least used
