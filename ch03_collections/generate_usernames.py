#!/usr/bin/env python3
import collections
import sys

User = collections.namedtuple("User",
                              "id username forename middlename surname")

ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)


def process_line(line, usernames):
    fields = line.split(":")
    username = generate_username(fields, usernames)
    return User(fields[ID], username, fields[FORENAME], fields[MIDDLENAME], fields[SURNAME])


def generate_username(fields, usernames):
    username = (fields[FORENAME][0] + fields[MIDDLENAME][:1] +
                fields[SURNAME]).replace("-", "").replace("'", "")
    username = original_username = username[:8].lower()
    count = 1
    while username in usernames:
        username = "{0}{1}".format(original_username, count)
        count += 1
    usernames.add(username)
    return username


def print_users(users):
    namewidth = 32
    usernamewidth = 9

    print("{0:<{nw}} {1:^6} {2:^{uw}}".format(
        "Name", "ID", "Username", nw=namewidth, uw=usernamewidth))
    print("{0:-<{nw}} {0:-<6} {0:-<{uw}}".format(
        "", nw=namewidth, uw=usernamewidth
    ))

    for key in sorted(users):
        user = users[key]
        fullname = user.forename + ", " + user.surname
        if user.middlename:
            fullname += " " + user.middlename[:1]
        print("{fn:.<{nw}} ({u.id:^4}) {u.username:<{uw}}".format(
            fn=fullname, u=user, nw=namewidth, uw=usernamewidth))


def main():
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        print("usage: {0} file1 [file2 [... fileN]]".format(sys.argv[0]))
        sys.exit()

    usernames = set()
    users = {}
    for filename in sys.argv[1:]:
        for line in open(filename, encoding="utf8"):
            line = line.strip()
            if not line:
                continue
            user = process_line(line, usernames)
            users[(user.surname.lower(), user.forename.lower(), user.id)] = user

    print_users(users)


main()
