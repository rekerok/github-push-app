import faker
import github
import os

def updateSeveralFiles(repo, commit_message, file_list):
    fake = faker.Faker()
    master_ref = repo.get_git_ref("heads/main")
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for file in file_list:
        print(repo.get_contents(file).decoded_content.decode())
        element = github.InputGitTreeElement(file, "100644", "blob",
                                             f"{repo.get_contents(file).decoded_content.decode()}\n{fake.paragraph(nb_sentences=1)}")
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)


def main():
    print("def main")
    print(os.listdir())
    arrToken = list()
    with open("script/accessTokens.txt", "r") as file:
        for line in file.readlines():
            arrToken.append(line)

    arrToken = list(map(lambda x: x.strip('\n'), arrToken))
    for token in arrToken:
        g = github.Github(token)
        user = g.get_user()
        print(f"\t{user.login}")
        repos = user.get_repos()
        for repo in repos:
            print(f"\t\t{repo.name}")


if __name__ == "__main__":
    main()
