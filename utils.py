import colorama


def print_error_connecting_with_token(token):
    print(f"ОШИБКА подключения по токену {token}")


def print_successful_connection_to_repo_message(repo):
    print(f"Подключение к репозиторию {repo.html_url} - {colorama.Fore.GREEN}УСПЕШНО")


def print_successful_file_push_message(file_to_push):
    print(f"Файл {file_to_push} запушился {colorama.Fore.GREEN}УСПЕШНО")


def print_successful_file_creation_message(file_to_push):
    print(f"Файл {file_to_push} создался {colorama.Fore.GREEN}УСПЕШНО")


def print_successful_read_of_random_code_from_file_message(file):
    print(f"Случайный код из файла тип {colorama.Back.BLUE}{file['folder'][:-1]}{colorama.Style.RESET_ALL} считался {colorama.Fore.GREEN}УСПЕШНО")


def print_no_existence_of_folder_message(file):
    print(f"Папки с файлами типа {file['folder']}{colorama.Fore.RED} НЕ СУЩЕСТВУЕТ")


def print_read_of_file_result_message(file, isSuccessful):
    if isSuccessful:
        print(f"Файл {file['output']} считался {colorama.Fore.GREEN}УСПЕШНО")
    else:
        print(f"Файл {file['output']} считался {colorama.Fore.RED}НЕУСПЕШНО")