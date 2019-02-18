#!/usr/bin/env python3
import os
import sys
from collections import namedtuple


def get_string(message, name="string", default=None,
               minimum_length=0, maximum_length=80):
    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length == 0:
                    return ""
                else:
                    raise ValueError("{0} may not be empty".format(
                        name
                    ))
            if not (minimum_length <= len(line) <= maximum_length):
                raise ValueError("{name} must have at least "
                                 "{minimum_length} and at most "
                                 "{maximum_length} characters".format(**locals()))
            return line
        except ValueError as err:
            print("ERROR:", err)


def get_integer(message, name="integer", default=None,
                minimum=0, maximum=100, allowed_zero=True):
    while True:
        try:
            line = get_string(message, name, default, 1)
            number = int(line)
            if not (minimum <= number <= maximum):
                raise ValueError("{name} must have at least "
                                 "{minimum} and at most "
                                 "{maximum}".format(**locals()))
            if not allowed_zero and number == 0:
                raise ValueError("{name} must not be zero")
            return number
        except ValueError as err:
            print("ERROR:", err)


def get_one_of_range(message, range, name="value", default=None):
    assert "default value should be in range", default in range
    while True:
        try:
            value = get_string(message, name, default, 1, 1)
            if value not in range:
                raise ValueError("invalid choice - enter one of '{0}'".format(
                    range
                ))
            return value
        except ValueError as err:
            print("ERROR:", err)
            input("Press Enter to continue...")


ListKeeper = namedtuple("ListKeeper",
                        "items commands source")


def print_sorted_items(items):
    print()
    item_template = "{0}: {1}"
    if len(items) == 0:
        print("-- no items are in the list --")
    for index, item in enumerate(sorted(items), start=1):
        print(item_template.format(index, item))


def make_prompt_message(list_keeper):
    command_message = "[A]dd  "
    if len(list_keeper.items) > 0:
        command_message += "[D]elete  "
    if len(list_keeper.commands) > 0:
        command_message += "[S]ave  "
    command_message += "[Q]uit"
    return command_message


def load_items_from_source(source):
    fh = None
    try:
        fh = open(source, "r", encoding="utf-8")
        return [item.strip() for item in fh.readlines()]
    except EnvironmentError as err:
        print("ERROR:", err)
    finally:
        if fh is not None:
            fh.close()


def handle_add(list_keeper):
    new_item = get_string("Add item", name="item", minimum_length=1)
    list_keeper.items.append(new_item)
    list_keeper.commands.append(("add", new_item))


def handle_delete(list_keeper):
    item_index = get_integer("Delete item number (or 0 to cancel)",
                             name="number",
                             maximum=len(list_keeper.items), allowed_zero=True)
    if item_index == 0:
        return
    deleted_item = sorted(list_keeper.items)[item_index - 1]
    list_keeper.items.remove(deleted_item)
    list_keeper.commands.append(("del", deleted_item))


def handle_save(list_keeper):
    fh = None
    try:
        fh = open(list_keeper.source, "w", encoding="utf-8")
        for item in list_keeper.items:
            fh.write(item + "\n")
    except EnvironmentError as err:
        print("ERROR:", err)
    else:
        list_keeper.commands.clear()
        print("Saved {0} items to {1}".format(
            len(list_keeper.items), list_keeper.source))
    finally:
        if fh is not None:
            fh.close()


def handle_quit(list_keeper):
    if len(list_keeper.commands) == 0:
        return
    need_save_opt = get_string("Save unsaved changes (y/n)",
                               default="y",
                               minimum_length=1, maximum_length=1)
    if need_save_opt in ("y", "Y"):
        handle_save(list_keeper)


def init_list_keeper():
    list_keeper = None

    filenames = [path for path in os.listdir(".") if path.endswith(".lst")]
    if len(filenames) > 0:
        print("Found {0} files in current directory".format(len(filenames)))
        print_sorted_items(filenames)
        index = get_integer("Choose filename (or 0 to new)", name="source",
                            maximum=len(filenames), allowed_zero=True)
        if index > 0:
            source = sorted(filenames)[index - 1]
            items = load_items_from_source(source)
            list_keeper = ListKeeper(items, [], source)

    if list_keeper is None:
        filename = get_string("Choose filename", "filename", minimum_length=1)
        if not filename.endswith((".lst",)):
            filename += ".lst"
        list_keeper = ListKeeper([], [], filename)
    return list_keeper


def main():
    list_keeper = init_list_keeper()

    while True:
        print_sorted_items(list_keeper.items)
        command = get_one_of_range(make_prompt_message(list_keeper),
                                   "AaDdSsQq", default="a")

        if command in ("a", "A"):
            handle_add(list_keeper)
        elif command in ("d", "D"):
            handle_delete(list_keeper)
        elif command in ("s", "S"):
            handle_save(list_keeper)
            input("Press Enter to continue...")
        elif command in ("q", "Q"):
            handle_quit(list_keeper)
            sys.exit()


main()
