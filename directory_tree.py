import os


class DirectoryTree:
    def __init__(self, root):
        self.root = root

    def print(self):
        """
        Recursively prints the directory tree starting from the specified root.
        """
        self.print_directory_tree(self.root, "")

    @staticmethod
    def print_directory_tree(root, prefix):
        """
        Recursively prints the directory tree starting from the specified root.

        Args:
            root (str): The root directory to start printing from.
            prefix (str): The prefix to use for the current level of the tree.
        """
        items = os.listdir(root)
        for i, item in enumerate(sorted(items)):
            path = os.path.join(root, item)
            if os.path.isdir(path):
                print(prefix + "+--" + item + "/")
                if i == len(items) - 1:
                    DirectoryTree.print_directory_tree(path, prefix + "    ")
                else:
                    DirectoryTree.print_directory_tree(path, prefix + "|   ")
            else:
                if i == len(items) - 1:
                    print(prefix + "+--" + item)
                else:
                    print(prefix + "|--" + item)
