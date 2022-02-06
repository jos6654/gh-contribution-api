import requests
from .config import token

header = {'Authorization': 'token %s' % token}

# Collect relevant statistics from user's repositories
# username: str
# forked: bool
def collect_stats(username, forked):
    stats = {}
    page = 1
    last_page = False
    repositories = []

    # Loop through all pages, 100 repositories at a time
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

    # Iterate through repositories to collect stats
    for repo in repositories:
        stats["num_stargazers"] += repo["stargazers_count"]
        stats["num_forks"] += repo["forks_count"]
        stats["avg_repo_size"] += repo["size"]
        stats["languages"][repo["language"]] = stats["languages"].setdefault(repo["language"], 0) + 1

    # Sort languages and make file size human readable
    stats["languages"] = dict(sorted(stats["languages"].items(), key=lambda language: language[1], reverse=True))
    stats["avg_repo_size"] = readable_file_size(stats["avg_repo_size"]/stats["num_repos"])
    
    return stats

# Format file size to be human readable with units, based off this solution: https://stackoverflow.com/a/1094933
# size: float
def readable_file_size(size):
    for unit in ["KB", "MB", "GB"]:
        if abs(size) < 1024.0:
            return f"{size:3.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"