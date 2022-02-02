import requests

def list_repos(org):
    # TODO Add error response/code for invalid org
    res = requests.get("https://api.github.com/orgs/%s/repos?per_page=100" % org)
    repo_list = res.json()
    count = 2
    while len(res.json()) == 100:
        res = requests.get("https://api.github.com/orgs/%s/repos?per_page=100&page=%s" % (org, count))
        repo_list.extend(res.json())
        count += 1

    return repo_list

def new_contributor(repo, contributor):
    return None

def sort_contributors(repos):
    # {"contribution": 123, "image_url": xyz, "email": xyz, "latest_commit": commit_url}
    contributors = {}
    for r in repos:
        res = requests.get("https://api.github.com/repos/%s?per_page=100" % r["full_name"])
        count = 2
        while len(res.json()) == 100:
            for c in res.json():
                if c["login"] in contributors:
                    contributors[c["login"]]["contribution"] += c["contributions"]
                    # Update latest commit
                else:
                    # New contributor
                    contributors[c["login"]] = new_contributor(r["full_name"], c)

            res = requests.get("https://api.github.com/repos/%s?per_page=100&page=%s" % (r["full_name"], count))
            count += 1