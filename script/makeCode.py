import os
import random

import github

PATH_TEMPLATES_FOLDER = "../templates"

g = github.Github("", per_page=1)


# query = 'pony language:python'
# try:
#     for i in g.search_code(query=query):
#         print(i.html_url)
# except github.RateLimitExceededException:
#     print("RateLimitExceededException")

def listAllFileInDirectory(path):
    # listFile = list()
    # for root, dirs, files in os.walk(path):
    #     for name in files:
    #         listFile.append(os.path.join(root, name))
    return [os.path.join(root, name) for root, dirs, files in os.walk(path) for name in files]


def selectRandomTemplate():
    list_directories = sorted(os.listdir(PATH_TEMPLATES_FOLDER), key=lambda x: int(x))
    random_select_folder = list_directories[random.randint(0, len(list_directories))]
    random_template_path = os.path.abspath(f"{PATH_TEMPLATES_FOLDER}/{random_select_folder}")
    print(listAllFileInDirectory(random_template_path))
    size = {value:os.path.getsize(value) for value in listAllFileInDirectory(random_template_path)}
    print(size)


selectRandomTemplate()
