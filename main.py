import json
import os
import random
from typing import Any, Dict

import colorama
import github
from github import BadCredentialsException
from github import GithubException
from github import UnknownObjectException

import config, utils

colorama.init(autoreset=True)


def get_list_files_accounts():
    return list(
        map(lambda x: config.PATH_ACTIVE_ACCOUNTS + x, [file for file in os.listdir(config.PATH_ACTIVE_ACCOUNTS)]))


def parse_json_accounts(files) -> list[Any]:
    list_accounts = list()
    for file in files:
        with open(file, 'r') as file:
            data = json.load(file)
            list_accounts.append(data)
    return list_accounts


def print_info_account(token):
    acc = github.Github(token)
    user = acc.get_user()
    print(f"acc - {user.login}")
    print(f"name - {user.name}\n")


def get_repo_name_from_link(link):
    parts = link.split('/')
    username = parts[-2]
    repo_name = parts[-1]
    return f"{username}/{repo_name}"


def get_code_from_file(path_to_file):
    with open(path_to_file, "r") as file_name:
        code = file_name.read()
    return code


def connect_to_account(token):
    git = github.Github(token)
    try:
        acc = git.get_user()
        print(acc.login)
        return git, acc
    except BadCredentialsException:
        utils.print_error_connecting_with_token(token)
        return None, None


def connect_to_repo(acc, repo_name):
    try:
        repo = acc.get_repo(repo_name)
        return repo
    except UnknownObjectException:
        return None


def connect_to_file(repo, file_path):
    try:
        return repo.get_contents(file_path)
    except (UnknownObjectException, GithubException):
        return None


def push_in_repo(repo, file_to_push, code_to_push):
    content_file = connect_to_file(repo, file_to_push)
    if content_file:
        text_for_push = content_file.decoded_content.decode('utf-8') + code_to_push
        commit_for_push = f"update file {file_to_push}"
        file_sha = content_file.sha
        repo.update_file(path=file_to_push, message=commit_for_push, content=text_for_push, sha=file_sha)
        utils.print_successful_file_push_message(file_to_push)
    else:
        text_for_push = code_to_push
        commit_for_push = f"create file {file_to_push}"
        repo.create_file(path=file_to_push, message=commit_for_push, content=text_for_push)
        utils.print_successful_file_creation_message(file_to_push)
        utils.print_successful_file_push_message(file_to_push)


def select_random_file(type):
    return random.choice(os.listdir(config.PATH_CODE_STORAGE_RANDOM + type))


def parse_lines(lines):
    range_linas = list(map(lambda x: int(x), lines.split('-')))
    if len(range_linas) == 2:
        min_lines, max_lines = range_linas
        return random.randint(min_lines, max_lines)
    else:
        return range_linas[0]


def random_part_string(code, count_lines):
    parts_code = code.splitlines(keepends=True)
    if len(parts_code) < count_lines:
        return code
    else:
        start = random.randint(0, len(parts_code) - count_lines)
        return "".join(parts_code[start:start + count_lines])


def select_random_code(type_folder, count_lines):
    if os.path.isdir(os.path.join(config.PATH_CODE_STORAGE_RANDOM + type_folder)):
        lines = parse_lines(count_lines)
        code_from_file = get_code_from_file(
            os.path.join(config.PATH_CODE_STORAGE_RANDOM, type_folder,
                         select_random_file(type_folder)))
        code = random_part_string(code_from_file, lines)
        return code
    else:
        return None


def preparing_for_a_commit(acc_dict: Dict):
    token = acc_dict['token']
    git, acc = connect_to_account(token)
    if not acc:
        return False
    for repo_link in acc_dict['repos']:
        repo = connect_to_repo(acc, repo_link['name'])
        if not repo:
            repo = acc.create_repo(repo_link['name'])
            repo.create_file("README.md", "Initial commit", f"#{repo_link['name']}", branch=repo.default_branch)
        utils.print_successful_connection_to_repo_message(repo)
        for file in repo_link["files"]:
            if file['random']:
                code_for_push = select_random_code(file['folder'], file['lines'])
                if code_for_push:
                    utils.print_successful_read_of_random_code_from_file_message(file)
                else:
                    utils.print_no_existence_of_folder_message(file)
                    continue
            else:
                path_to_file = os.path.join(config.PATH_CODE_STORAGE, file['output'])
                if os.path.isfile(path_to_file):
                    code_for_push = get_code_from_file(path_to_file)
                    utils.print_read_of_file_result_message(file, True)
                else:
                    utils.print_read_of_file_result_message(file, False)
                    continue
            push_in_repo(repo, file['input'], code_for_push)
    return True


def main():
    accounts_files = get_list_files_accounts()
    accounts_dict = parse_json_accounts(accounts_files)
    for acc_dict in accounts_dict:
        preparing_for_a_commit(acc_dict)
        print('')


if __name__ == "__main__":
    main()
