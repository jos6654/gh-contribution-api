from more_itertools import last
import requests
import dateutil.parser
from .config import token

header = {'Authorization': 'token %s' % token}

def list_repos(org):
    # TODO Add error response/code for invalid org
    repo_list = []
    count = 1
    last_page = False
    while not last_page:
        res = requests.get("https://api.github.com/orgs/%s/repos?per_page=100&page=%s" % (org, count), headers=header)
        repo_list.extend([r["full_name"] for r in res.json()])
        count += 1
        if len(res.json()) < 100:
            last_page = True
    return repo_list

def new_contributor(repo, contributor):
    print(repo + " " + contributor["login"])
    res = requests.get("https://api.github.com/repos/%s/commits?per_page=1&author=%s" % (repo, contributor["login"]), headers=header)
    if res.json():
        return {"contribution": contributor["contributions"], "image_url": contributor["avatar_url"], "email": res.json()[0]["commit"]["committer"]["email"], \
            "latest_commit_message": res.json()[0]["commit"]["message"], "date": res.json()[0]["commit"]["committer"]["date"]}
    else:
        return {"contribution": contributor["contributions"], "image_url": contributor["avatar_url"], "email": "Private", \
            "latest_commit_message": "Unavailable", "date": "0000-00-00T00:00:00Z"}

def sort_contributors(repos):
    # {"contribution": 123, "image_url": xyz, "email": xyz, "latest_commit_message": message, "date": ISO 8601}
    contributors = {}
    duplicate = 0
    for r in repos:
        count = 1
        last_page = False
        while not last_page:
            res = requests.get("https://api.github.com/repos/%s/contributors?per_page=100&page=%s" % (r, count), headers=header)
            for c in res.json():
                if c["login"] in contributors:
                    duplicate += 1
                    contributors[c["login"]]["contribution"] += c["contributions"]
                    # Update for possibility of no commits
                    commit_res = requests.get("https://api.github.com/repos/%s/commits?per_page=1&author=%s" % (r, c["login"]), headers=header).json()[0]["commit"]
                    curr_date = dateutil.parser.parse(contributors[c["login"]]["date"])
                    new_date = dateutil.parser.parse(commit_res["committer"]["date"])
                    if new_date > curr_date:
                        contributors[c["login"]]["latest_commit_message"] = commit_res["message"]
                        contributors[c["login"]]["date"] = commit_res["committer"]["date"]
                        contributors[c["login"]]["email"] = ["committer"]["email"]
                else:
                    contributors[c["login"]] = new_contributor(r, c)
            count += 1
            if len(res.json()) < 100:
                last_page = True
    print("DUPLICATES: " + str(duplicate))
    return contributors