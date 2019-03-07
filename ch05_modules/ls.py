#!/usr/bin/env python3
import os


def is_hidden_path(path):
    return path.startswith(".")


def by_path_name(stat_entry):
    return stat_entry[0]


def main():
    # TODO: sanitize input roots - expanduser, expandvars, abspath
    root_names = ["/home/mkiryanov/", "~/.local/"]
    expanded_roots_iter = zip(root_names,
                              [os.path.abspath(os.path.expanduser(os.path.expandvars(r))) for r in root_names])

    recursive = False
    show_hidden = False

    stats = {}
    if not recursive:
        for root_name, root_abs_path in expanded_roots_iter:
            for path in os.listdir(root_abs_path):
                if not show_hidden and is_hidden_path(path):
                    continue
                file_abs_path = os.path.join(root_abs_path, path)
                path_name = os.path.join(root_name, path)
                if not os.path.isdir(file_abs_path):
                    stat = os.stat(file_abs_path)
                    data = (path_name, True, stat.st_size, stat.st_mtime_ns)
                else:
                    data = (path_name, False, None, None)
                stats.update({file_abs_path: data})
    else:
        for root_name, root_abs_path in expanded_roots_iter:
            for root, dirnames, filenames in os.walk(root_abs_path):
                for path in dirnames:
                    if not show_hidden and is_hidden_path(path):
                        continue
                    path_name = os.path.join(root, path)
                    stats.update({path: (path_name, False, None, None)})
                for path in filenames:
                    if not show_hidden and is_hidden_path(path):
                        continue
                    file_abs_path = os.path.join(root, path)
                    stat = os.stat(file_abs_path)
                    path_name = os.path.join(root, path)
                    data = (path_name, True, stat.st_size, stat.st_mtime_ns)
                    stats.update({file_abs_path: data})

    for path_name, stat in sorted(stats.items(), key=by_path_name):
        if stat[1]:
            print(stat[0], stat[2], stat[3])
        else:
            print(stat[0])


main()
