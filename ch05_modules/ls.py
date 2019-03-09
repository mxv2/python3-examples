#!/usr/bin/env python3
import locale
import os
from datetime import datetime
from optparse import OptionParser

FULL_PATH, IS_FILE, FILE_SIZE, FILE_MTIME = range(4)


def is_hidden_path(path):
    return path.startswith(".")


def by_path_name(stat_item):
    return stat_item[FULL_PATH]


def by_file_size(stat_item):
    size = stat_item[FILE_SIZE]
    return size if size else 0


def by_file_mtime(stat_item):
    mtime = stat_item[FILE_MTIME]
    return mtime if mtime else 0


def gather_fs_stats_simply(root, show_hidden):
    stats = []
    for filename in os.listdir(root):
        if not show_hidden and is_hidden_path(filename):
            continue
        full_path = os.path.join(root, filename)
        if not os.path.isdir(full_path):
            stat = os.stat(full_path, follow_symlinks=False)
            data = (full_path, True, stat.st_size, stat.st_mtime)
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
            stats.append((full_path, True, stat.st_size, stat.st_mtime))

        dirnames[:] = [dir for dir in dirnames if not is_hidden_path(dir)]
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


def print_stats(stats, show_size, show_time, locale_id):
    locale.setlocale(locale.LC_ALL, locale_id)

    print_template = "{name:<s}"
    if show_size:
        print_template = "{size: >15{size_fmt}} " + print_template
    if show_time:
        print_template = "{time: <20} " + print_template

    file_count = 0
    dir_count = 0

    for stat in stats:
        name = stat[FULL_PATH]
        if stat[IS_FILE]:
            file_count += 1

            if show_size:
                size = stat[FILE_SIZE]
                size_fmt = "n"
            if show_time:
                time = datetime.utcfromtimestamp(stat[FILE_MTIME]).strftime("%x %X")
        else:
            dir_count += 1

            if show_size:
                size = ""
                size_fmt = ""
            if show_time:
                time = ""

        print(print_template.format(**locals()))
    print("\n{0} file{1}, {2} director{3}".format(file_count, "" if file_count == 1 else "s",
                                                  dir_count, "y" if dir_count == 1 else "ies"))


def resolve_order_func(order_option):
    if order_option in ("name", "n"):
        return by_path_name
    elif order_option in ("modified", "m"):
        return by_file_mtime
    else:
        return by_file_size


def process_options():
    usage = ("%prog [options] [path1 [path2 [... pathN]]]\n"
             "The paths are optional; if not given . is used.")
    parser = OptionParser(usage=usage)
    parser.add_option("-H", "--hidden",
                      action="store_true", dest="show_hidden", default=False,
                      help="show hidden files [default: off]")
    parser.add_option("-m", "--modified",
                      action="store_true", dest="show_time", default=False,
                      help="show last modified date/time [default: off]")
    parser.add_option("-o", "--order",
                      type="choice", choices=["name", "n", "modified", "m", "size", "s"], default="name",
                      help="order by ('name', 'n', 'modified', 'm', 'size', 's') [default: name]")
    parser.add_option("-r", "--recursive",
                      action="store_true", dest="recursive", default=False,
                      help="recurse into subdirectories [default: off]")
    parser.add_option("-s", "--sizes",
                      action="store_true", dest="show_size", default=False,
                      help="show sizes [default: off]")
    return parser.parse_args()


def main():
    (options, args) = process_options()

    root_names = args if args else "."
    stats = gather_fs_stats(root_names, options.recursive, options.show_hidden)
    print_stats(sorted(stats, key=resolve_order_func(options.order)),
                options.show_size, options.show_time, "ru_RU.UTF-8")


main()
