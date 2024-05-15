# script.py
import os
import json
from errors import (
    FileSystemError,
    FileNotFoundError,
    DirectoryNotFoundError,
    InvalidPathError
)

class FileSystem:
    class Node:
        def __init__(self, name, is_directory=False):
            self.name = name
            self.is_directory = is_directory
            self.children = {}
            self.content = ""

    def __init__(self):
        self.root = self.Node("/")
        self.current_directory = self.root

    def mkdir(self, directory_name):
        original_name = directory_name
        count = 1
        while directory_name in self.current_directory.children:
            directory_name = f"{original_name}{count}"
            count += 1

        new_directory = self.Node(directory_name, True)
        self.current_directory.children[directory_name] = new_directory

        if original_name != directory_name:
            print(f"{original_name} created as {directory_name}")


    def cd(self, path):
        if path == "/":
            self.current_directory = self.root
        elif path == "..":
            if self.current_directory != self.root:
                self.current_directory = self._get_parent(self.current_directory)
            else:
                raise InvalidPathError("Cannot move up from root directory.")
        else:
            target_directory = self._find_directory(path)
            if target_directory:
                self.current_directory = target_directory
            else:
                raise DirectoryNotFoundError(f"Directory '{path}' not found.")

    def ls(self, path=""):
        target_directory = self._find_directory(path) if path else self.current_directory
        if target_directory:
            for directory in target_directory.children.keys():
                print(directory)
        else:
            raise DirectoryNotFoundError(f"Directory '{path}' not found.")

    def touch(self, file_name):
        if file_name not in self.current_directory.children:
            new_file = self.Node(file_name)
            self.current_directory.children[file_name] = new_file
        else:
            raise FileNotFoundError(f"File '{file_name}' already exists.")

    def mv(self, source, destination):
        source_node = self._find_node(source)

        if not source_node:
            raise FileNotFoundError(f"Source '{source}' not found.")

        destination_node = self._find_directory(destination)

        if not destination_node:
            raise DirectoryNotFoundError(f"Destination directory '{destination}' not found.")

        if source_node.name in destination_node.children:
            raise FileSystemError(f"Destination '{destination}' already contains a node with the same name.")

        source_parent = self._get_parent(source_node)
        del source_parent.children[source_node.name]
        destination_node.children[source_node.name] = source_node

        print(f"{source} moved to {destination}")

    def cp(self, source, destination):
        source_node = self._find_directory_or_file(source)
        if source_node:
            destination_node = self._find_directory(destination)

            if not destination_node:
                raise DirectoryNotFoundError(f"Destination directory '{destination}' not found.")

            if source_node.name in destination_node.children:
                raise FileSystemError(f"Destination '{destination}' already contains a node with the same name.")

            copy_node = self._copy_node(source_node)
            destination_node.children[source_node.name] = copy_node

            print(f"{source} copied to {destination}")
        else:
            raise FileNotFoundError(f"Source '{source}' not found.")

    def rm(self, name):
        target = self._find_node(name)
        if not target:
            raise FileNotFoundError(f"'{name}' not found.")

        parent = self._get_parent(target)

        if parent:
            self._delete_node(target)
            del parent.children[name]
            print(f"{name} removed successfully.")
        else:
            raise FileSystemError("Cannot remove root directory.")

    def grep(self, file_name, pattern):
        file_node = self._find_directory_or_file(file_name)
        if file_node and not file_node.is_directory:
            if pattern in file_node.content:
                print(f"Pattern found in {file_name}")
            else:
                print(f"Pattern not found in {file_name}")
        else:
            raise FileNotFoundError(f"File '{file_name}' not found.")

    def cat(self, file_name):
        file_node = self._find_directory_or_file(file_name)
        if file_node and not file_node.is_directory:
            print(file_node.content)
        else:
            raise FileNotFoundError(f"File '{file_name}' not found or is a directory.")

    def save_state(self, path):
        state = {
            "current_directory": self.current_directory.name,
            "file_system_structure": self._serialize_node(self.root)
        }
        with open(path, "w") as f:
            json.dump(state, f)

    def load_state(self, path):
        with open(path, "r") as f:
            state = json.load(f)
            self.current_directory = self._find_directory(state["current_directory"])
            self.root = self._deserialize_node(state["file_system_structure"])

    def _serialize_node(self, node):
        serialized_node = {
            "name": node.name,
            "is_directory": node.is_directory,
            "content": node.content
        }
        if node.is_directory:
            serialized_node["children"] = {child.name: self._serialize_node(child) for child in node.children.values()}
        return serialized_node

    def _deserialize_node(self, serialized_node):
        node = self.Node(serialized_node["name"], serialized_node["is_directory"])
        node.content = serialized_node["content"]
        if serialized_node["is_directory"]:
            node.children = {child_name: self._deserialize_node(child) for child_name, child in serialized_node["children"].items()}
        return node

    def _find_node(self, path):
        return self._find_node_recursive(self.current_directory, path)

    def _delete_node(self, node):
        if node.is_directory:
            for child in node.children.values():
                self._delete_node(child)
        del node

    def _copy_node(self, source):
        copy = self.Node(source.name, source.is_directory)
        if source.is_directory:
            for child_name, child_node in source.children.items():
                copy.children[child_name] = self._copy_node(child_node)
        else:
            copy.content = source.content
        return copy

    def _find_directory(self, path):
        components = path.split("/")
        current = self.current_directory

        for component in components:
            if component == "..":
                current = self._get_parent(current)
            elif component in current.children:
                current = current.children[component]
            else:
                return None

        return current

    def _find_directory_or_file(self, name):
        if name in self.current_directory.children:
            return self.current_directory.children[name]
        else:
            return None

    def _get_parent(self, node):
        if node == self.root:
            return self.root

        for parent_node in self.root.children.values():
            if node in parent_node.children.values():
                return parent_node
        return None

    def _find_node_recursive(self, current, path):
        if not path or path == ".":
            return current

        components = path.split("/")
        next_component = components[0]

        if next_component in current.children:
            next_node = current.children[next_component]
            if len(components) == 1:
                return next_node
            else:
                return self._find_node_recursive(next_node, "/".join(components[1:]))
        else:
            return None