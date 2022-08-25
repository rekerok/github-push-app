import json
import github
import github.GithubException


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
                "url": user.html_url,
                "repositories": list(repo.html_url for repo in user.get_repos())
            }
        except github.BadCredentialsException:
            print(f"Wrong token entered in account: {key}\n")
            continue
    print(json.dumps(config_dict, indent=2))


readTokensFile()
