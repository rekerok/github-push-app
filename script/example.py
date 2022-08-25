import github
import faker

fake = faker.Faker()


def osateam():
    token = ""
    g = github.Github("")
    repo = g.get_user().get_repo("osateam-private-repo")
    print(fake.name())
    content = repo.get_contents("qwer.txt")
    repo.update_file("qwer.txt", "update qwer.txt",
                     f"{content.decoded_content.decode()}\n{fake.paragraph(nb_sentences=1)}",
                     repo.get_contents("qwer.txt").sha)


def pump():
    token = ""  #
    g = github.Github("")
    repo = g.get_user().get_repo("pumperinho-private-repo")
    print(fake.name())
    content = repo.get_contents("qwer.txt")
    repo.update_file("qwer.txt", "update qwer.txt",
                     f"{content.decoded_content.decode()}\n{fake.paragraph(nb_sentences=1)}",
                     repo.get_contents("qwer.txt").sha)


def egorivanovtest():
    token = ""
    g = github.Github("")
    repo = g.get_user().get_repo("egorivanovtest-private-repo")
    print(fake.name())
    content = repo.get_contents("qwer.txt")
    repo.update_file("qwer.txt", "update qwer.txt",
                     f"{content.decoded_content.decode()}\n{fake.paragraph(nb_sentences=1)}",
                     repo.get_contents("qwer.txt").sha)


def main():
    pass
    # osateam()
    # pump()
    # egorivanovtest()


if __name__ == "__main__":
    main()
