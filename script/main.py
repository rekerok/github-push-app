import json
import os
from typing import Any, Dict

import github
from github import BadCredentialsException
from github import UnknownObjectException

PATH_PRIVATE_TOKENS = "./private_token.txt"
PATH_FOLDER_ACCOUNTS = "./account/"
PATH_FOLDER_CODE_STORAGE = "./code"


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


def connecting_to_repo(acc, link):
    try:
        return acc.get_repo(get_repo_name_from_link(link))
    except UnknownObjectException:
        return None


def connecting_to_file(repo, file_path):
    try:
        return repo.get_contents(file_path)
    except UnknownObjectException:
        return None


def push(repo, file_path, commit_message, code_for_commit, file_sha):
    pass


def preparing_for_a_commit(acc_dict: Dict):
    acc = connecting_to_account(acc_dict['token'])
    if not acc:
        return False
    user = acc.get_user()
    for repo_link in acc_dict['repos']:
        repo = acc.get_repo(get_repo_name_from_link(repo_link['name']))
        if not repo:
            print(f"Подключение к репозиторию {repo_link['name']} - ОБОРВАЛОСЬ")
            continue
        print(f"Подключение к репозиторию {repo.html_url} - УСПЕШНО")
        for file in repo_link["files"]:
            name_output_file = file['output']
            code_from_file, correct_file = get_code_from_file(file["output"])
            if correct_file:
                print(f"Файл {name_output_file} считался УСПЕШНО")
            else:
                print(f"Файл {name_output_file} считался НЕ УСПЕШНО")
                continue
            name_input_file = file['input']
            content_file = connecting_to_file(repo, name_input_file)
            if content_file:
                text_for_push = content_file.decoded_content.decode() + code_from_file
                commit_for_push = f"update file {name_input_file}"
                file_sha = content_file.sha
                repo.update_file(path=name_input_file, message=commit_for_push, content=text_for_push, sha=file_sha)
            else:
                text_for_push = code_from_file
                commit_for_push = f"create file {name_input_file}"
                repo.create_file(path=name_input_file, message=commit_for_push, content=text_for_push)
    return True


def main():
    accounts_files = get_list_files_accounts()
    accounts_dict = parse_json_accounts(accounts_files)
    for acc_dict in accounts_dict:
        preparing_for_a_commit(acc_dict)


if __name__ == "__main__":
    main()
