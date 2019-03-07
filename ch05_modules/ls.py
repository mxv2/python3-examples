#!/usr/bin/env python3
import os
import sys

FULL_PATH, IS_FILE, FILE_SIZE, FILE_MTIME = range(4)


def is_hidden_path(path):
    return path.startswith(".")


def by_path_name(stat_item):
    return stat_item[0]


def gather_fs_stats_simply(root, show_hidden):
    stats = []
    for filename in os.listdir(root):
        if not show_hidden and is_hidden_path(filename):
            continue
        full_path = os.path.join(root, filename)
        if not os.path.isdir(full_path):
            stat = os.stat(full_path, follow_symlinks=False)
            data = (full_path, True, stat.st_size, stat.st_mtime_ns)
        else:
            data = (full_path, False, None, None)
        stats.append(data)
    return stats


def gather_fs_stats_recursively(root_name, show_hidden):
    stats = []
    for root, dirnames, filenames in os.walk(root_name):
        for path in dirnames:
            if not show_hidden and is_hidden_path(path):
                continue
            full_path = os.path.join(root, path)
            stats.append((full_path, False, None, None))
        for path in filenames:
            if not show_hidden and is_hidden_path(path):
                continue
            full_path = os.path.join(root, path)
            stat = os.stat(full_path, follow_symlinks=False)
            stats.append((full_path, True, stat.st_size, stat.st_mtime_ns))
    return stats


def gather_fs_stats(root_names, recursive, show_hidden):
    stats = []
    if not recursive:
        for root_name in root_names:
            stats.extend(gather_fs_stats_simply(root_name, show_hidden))
    else:
        for root_name in root_names:
            stats.extend(gather_fs_stats_recursively(root_name, show_hidden))
    return stats

def main():
    root_names = sys.argv[1:]

    recursive = False
    show_hidden = True

    stats = gather_fs_stats(root_names, recursive, show_hidden)

    for stat in sorted(stats, key=by_path_name):
        if stat[IS_FILE]:
            print(stat[FULL_PATH], stat[FILE_SIZE], stat[FILE_MTIME])
        else:
            print(stat[FULL_PATH])


main()
