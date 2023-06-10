import os

from rich.text import Text
from rich.tree import Tree


def build_hierarchy(entries: list[str]) -> dict:
    """
    Builds a hierarchical dictionary structure based on the given list of entries.

    Args:
        entries (list[str]): The list of entries to build the hierarchy from.

    Returns:
        dict: A nested dictionary representing the hierarchy of entries.
    """

    entry_hierarchy = {}

    for entry in entries:
        parts = entry.split('/')
        current_dict = entry_hierarchy
        for part in parts:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]

    return entry_hierarchy


def build_tree(tree: Tree, entries: dict[str, dict]):
    """
    Recursively builds a tree structure based on the provided dictionary.

    Args:
        tree (Tree): The tree object to build the structure in.
        entries (dict[str, dict]): The entries dictionary representing the hierarchy.
    """
    for k, v in entries.items():
        icon = "📁 " if v else "📄 "
        branch = tree.add(Text(icon) + k)

        if v:
            build_tree(branch, v)


def clear_screen():
    # Clear the screen based on the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')
