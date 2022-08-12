import github


def main():
    print("def main")
    import os
    print(os.listdir())
    arrToken = list()
    with open("script/accessTokens.txt", "r") as file:
        for line in file.readlines():
            arrToken.append(line)

    arrToken = list(map(lambda x: x.strip('\n'), arrToken))
    for token in arrToken:
        g = github.Github(token)
        user = g.get_user()
        print(user.name)


if __name__ == "__main__":
    main()
