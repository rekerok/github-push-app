import json
import os
from typing import Any, Dict

import colorama
import github
from github import BadCredentialsException
from github import GithubException
from github import UnknownObjectException

PATH_PRIVATE_TOKENS = "./private_token.txt"
PATH_FOLDER_ACCOUNTS = "./account/"
PATH_FOLDER_CODE_STORAGE = "./code"
colorama.init(autoreset=True)


def get_list_files_accounts():
    return list(map(lambda x: PATH_FOLDER_ACCOUNTS + x, [file for file in os.listdir(PATH_FOLDER_ACCOUNTS)]))


def parse_json_accounts(files) -> list[Any]:
    list_accounts = list()
    for file in files:
        with open(file, 'r') as file:
            data = json.load(file)
            list_accounts.append(data)
    return list_accounts


def read_file_private_token():
    with open(PATH_PRIVATE_TOKENS, "r") as file:
        lines = list(map(lambda x: x.replace("\n", ''), file.readlines()))
    return lines


def info_acc(token):
    acc = github.Github(token)
    user = acc.get_user()
    print(f"acc - {user.login}")
    print(f"name - {user.name}\n")


def get_repo_name_from_link(link):
    parts = link.split('/')
    username = parts[-2]
    repo_name = parts[-1]
    return f"{username}/{repo_name}"


def get_code_from_file(file_name):
    full_path = f"{PATH_FOLDER_CODE_STORAGE}/{file_name}"
    try:
        with open(full_path, "r") as file_name:
            code = file_name.read()
    except FileNotFoundError:
        return None, False
    return code, True


def check_exist_file_in_repo(files_in_repo, check_file):
    if check_file in [file.name for file in files_in_repo if file.type == 'file']:
        return True
    else:
        return False


def connecting_to_account(token):
    try:
        return github.Github(token)
    except BadCredentialsException:
        return None


def connecting_to_repo(acc, repo_name):
    try:
        print([repo.name for repo in acc.get_repos()])
    except UnknownObjectException:
        return None


def connecting_to_file(repo, file_path):
    try:
        return repo.get_contents(file_path)
    except (UnknownObjectException, GithubException):
        return None


def push_in_repo(repo, file, code_from_file):
    content_file = connecting_to_file(repo, file)
    if content_file:
        text_for_push = content_file.decoded_content.decode('utf-8') + code_from_file
        commit_for_push = f"update file {file}"
        file_sha = content_file.sha
        repo.update_file(path=file, message=commit_for_push, content=text_for_push, sha=file_sha)
        print(f"Файл {file} запушился {colorama.Fore.GREEN}УСПЕШНО")
    else:
        text_for_push = code_from_file
        commit_for_push = f"create file {file}"
        repo.create_file(path=file, message=commit_for_push, content=text_for_push)
        print(f"Файл {file} создался и запушился {colorama.Fore.GREEN}УСПЕШНО")


def preparing_for_a_commit(acc_dict: Dict):
    git = connecting_to_account(acc_dict['token'])
    acc = git.get_user()
    print(acc)
    if not git:
        return False
    for repo_link in acc_dict['repos']:
        repo = connecting_to_repo(acc, repo_link['name'])
        # repo = git.get_repo(f"{name_acc}/{repo_link['name']}")
        if not repo:
            repo = acc.create_repo(repo_link['name'])
            repo.create_file("README.md", "Initial commit", f"#{repo_link['name']}", branch=repo.default_branch)
        print(f"Подключение к репозиторию {repo.html_url} - {colorama.Fore.GREEN}УСПЕШНО")
        for file in repo_link["files"]:
            name_output_file = file['output']
            code_from_file, correct_file = get_code_from_file(file["output"])
            if correct_file:
                print(f"Файл {name_output_file} считался {colorama.Fore.GREEN}УСПЕШНО")
            else:
                print(f"Файл {name_output_file} считался {colorama.Fore.RED}НЕ УСПЕШНО")
                continue
            name_input_file = file['input']
            push_in_repo(repo, name_input_file, code_from_file)
    return True


def main():
    accounts_files = get_list_files_accounts()
    accounts_dict = parse_json_accounts(accounts_files)
    for acc_dict in accounts_dict:
        preparing_for_a_commit(acc_dict)


if __name__ == "__main__":
    main()
