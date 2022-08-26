import json
import github


# Repository = Directory
def searcFilesInDirectory(repo, path=""):
    list_content = list()
    try:
        contents = repo.get_contents(path)
    except github.GithubException:
        return []
    print(repo.fork)
    for file_contenet in contents:
        if file_contenet.type == "dir":
            list_content.extend(searcFilesInDirectory())
        else:
            list_content.append(file_contenet.path)
    return list_content


def makeDictionaryRepo(repos):
    repos_dict = {}
    for repo in repos:
        repos_dict[repo.name] = {
            "use": "Input True or False",
            "files": [] if repo.fork else searcFilesInDirectory(repo)
        }
    return repos_dict


def readTokensFile():
    with open("example_accounts.json") as file_json:
        data = json.load(file_json)
    config_dict = dict()
    for key, value in data.items():
        g = github.Github(value)
        user = g.get_user()
        try:
            config_dict[value] = {
                "username": user.login,
                "use": True,
                "url": user.html_url,
                "repositories": makeDictionaryRepo(user.get_repos())
            }
        except github.BadCredentialsException:
            print(f"Wrong token entered in account: {key}\n")
            continue
    print(json.dumps(config_dict, indent=2))


readTokensFile()
