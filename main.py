import sys
import signal
import json 
from script import FileSystem

def execute_command(file_system, command):
    if not command:
        return False

    tokens = command.split()

    if tokens:
        operation = tokens[0]
        tokens = tokens[1:]

        if operation == "exit":
            return True
        elif operation == "ls" and not tokens:
            file_system.ls()
        elif operation == "ls" and len(tokens) == 1:
            file_system.ls(tokens[0])
        elif operation == "cd" and len(tokens) == 1:
            file_system.cd(tokens[0])
        elif operation == "mkdir" and len(tokens) == 1:
            file_system.mkdir(tokens[0])
        elif operation == "touch" and len(tokens) == 1:
            file_system.touch(tokens[0])
        elif operation == "mv" and len(tokens) == 2:
            file_system.mv(tokens[0], tokens[1])
        elif operation == "cp" and len(tokens) == 2:
            file_system.cp(tokens[0], tokens[1])
        elif operation == "rm" and len(tokens) == 1:
            file_system.rm(tokens[0])
        elif operation == "grep" and len(tokens) == 2:
            file_system.grep(tokens[0], tokens[1])
        elif operation == "cat" and len(tokens) == 1:
            file_system.cat(tokens[0])
        else:
            print("Error: Invalid command.")
    else:
        print("Error: Invalid command.")

    return False

def save_state_and_exit(file_system, path):
    file_system.save_state(path)
    print("State saved successfully.")
    sys.exit(0)

def load_state(file_system, path):
    try:
        with open(path, "r") as file:
            data = json.load(file)
            file_system.load_state(data)
            print("State loaded successfully.")
    except FileNotFoundError:
        print("Error: File not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")

def main():
    file_system = FileSystem()

    def signal_handler(sig, frame):
        save_state_and_exit(file_system, "autosave.json")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if len(sys.argv) > 1 and sys.argv[1] == "--load":
        load_state(file_system, "autosave.json")

    while True:
        command = input(f"Current Directory: {file_system.current_directory.name} $ ")

        if execute_command(file_system, command):
            break

if __name__ == "__main__":
    main()
