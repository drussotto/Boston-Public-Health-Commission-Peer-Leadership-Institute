def parse_logins():
    users_dict = {}
    with open("users.txt", "r") as usersFile:
        for l in usersFile.readlines():
            if l.startswith("#"):
                continue
            p = l.split(":")
            users_dict[p[0]] = p[1]
    return users_dict
