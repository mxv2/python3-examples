#!/usr/bin/env python3
import os
from pprint import pprint


def is_hidden_path(path):
    return path.startswith(".")


def main():
    # TODO: sanitize input roots - expanduser, expandvars, abspath
    roots = ["/home/mkiryanov/", ".local/"]

    recursive = True
    show_hidden = False

    stats = {}
    if not recursive:
        for root in roots:
            abs_root = os.path.abspath(root)
            for path in os.listdir(root):
                if not show_hidden and is_hidden_path(path):
                    continue
                abs_path = os.path.join(abs_root, path)
                data = None
                if not os.path.isdir(abs_path):
                    stat = os.stat(abs_path)
                    rel_path = os.path.join(root, path)
                    data = (rel_path, stat.st_size, stat.st_mtime_ns)
                stats.update({abs_path: data})
    else:
        for root in roots:
            for root, dirnames, filenames in os.walk(root):
                abs_root = os.path.abspath(root)
                for path in dirnames:
                    if not show_hidden and is_hidden_path(path):
                        continue
                    stats.update({os.path.join(abs_root, path): None})
                for path in filenames:
                    if not show_hidden and is_hidden_path(path):
                        continue
                    abs_path = os.path.join(abs_root, path)
                    stat = os.stat(abs_path, follow_symlinks=False)
                    rel_path = os.path.join(root, path)
                    data = (rel_path, stat.st_size, stat.st_mtime_ns)
                    stats.update({abs_path: data})

    pprint(stats.values())


main()
