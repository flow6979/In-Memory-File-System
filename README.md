# In-Memory File System

## Overview

This project implements a file system simulator in Python, allowing users to perform various file system operations through a command-line interface. The simulator includes functionalities for creating directories, managing files, navigating directories, and saving/loading the file system state.

## Dependencies

- The `FileSystem` class is defined in `script.py`.
- The `Node` class, which represents individual file system nodes, is an inner class of `FileSystem`.
- Error classes (`FileSystemError`, `FileNotFoundError`, `DirectoryNotFoundError`, `InvalidPathError`) are imported from an external module named `errors`.

## FileSystem Class

The `FileSystem` class provides a set of methods for managing the file system:
1. `mkdir`: Create a new directory.
2. `cd`: Changes the current directory. Support navigating to the parent directory using `..`, moving to the root directory using `/`, and navigating to a specified absolute path. Basically anything that you can do in a normal terminal. Since there is no user level implementation, ~ and / should take you to root.
3. `ls`: List the contents of the current directory or a specified directory.
4. `grep`: Search for a specified pattern in a file. **PS: Its a bonus**
5. `cat`: Display the contents of a file.
6. `touch`: Create a new empty file.
7. `echo`: Write text to a file. ex - `echo 'I am "Finding" difficult to write this to file' > file.txt`
8. `mv`: Move a file or directory to another location. ex - `mv /data/ice_cream/cassata.txt ./data/boring/ice_cream/mississippimudpie/`
9. `cp`: Copy a file or directory to another location. ex - `cp /data/ice_cream/cassata.txt .` **. For current directory **
10. `rm`: Remove a file or directory.


## Main Script (main.py)

The `main` function in `main.py` orchestrates the execution of the file system simulator:
- It initializes a `FileSystem` object and sets up signal handlers for interrupt and termination signals (`SIGINT` and `SIGTERM`).
- If the script is invoked with the `--load` argument, it attempts to load the previous state of the file system from "autosave.json".
- The script enters a loop to continuously prompt the user for commands and execute them using the `execute_command` function.
- If the user enters the "exit" command, the script saves the current state of the file system to "autosave.json" and exits gracefully.

## Execute Command Function

The `execute_command` function parses and executes user-entered commands:
- It splits the command into tokens and determines the operation to perform based on the first token.
- Depending on the operation, it calls the corresponding method of the `FileSystem` object.
- If the command is invalid, it prints an error message.

## Save State and Exit Function

The `save_state_and_exit` function saves the current state of the file system to a JSON file and exits the script:
- It is called when the user interrupts the script (e.g., pressing `Ctrl+C`) or when the "exit" command is entered.

## Load State Function

The `load_state` function attempts to load the previous state of the file system from a JSON file:
- It catches `FileNotFoundError` and `json.JSONDecodeError` exceptions and prints appropriate error messages if the file is not found or has an invalid JSON format.


## How to use ?

We need python3 installed to execute this python program
1. Running the code to use file system operations
    ```
    python3 main.py
    ```
2. Running unit tests
    ```
    python3 -m unittest unit_test.py
    ```
3. For autosavng current state in autosave.json
    ```
    ctrl c
    ```
## Approach:

**Understanding:** Initially, I carefully reviewed the project requirements to gain a clear understanding of the task at hand. This involved identifying the necessary functionalities required for a file system simulator, such as directory management and file manipulation.

**Designing Structure:** With a solid understanding of the requirements, I proceeded to design the class structure. I created the `FileSystem` class to encapsulate the file system functionality and an inner `Node` class to represent the nodes within the file system.

**Implementing Features:** Each method within the `FileSystem` class was then implemented to execute specific file system operations. I ensured that each method addressed a particular aspect of file system management, resulting in a comprehensive set of functionalities.

**Error Handling:** To enhance the robustness of the file system simulator, I incorporated error handling mechanisms. This involved importing error classes from an external module and implementing graceful error handling to handle various scenarios encountered during execution.

**Main Script:** To orchestrate the execution of the file system simulator, I developed the main script. This script provided a command-line interface for user interaction, enabling users to interact with the file system and manage its state effectively.

**State Management:** I implemented functionality within the file system to save and load its state. This feature allowed users to persist their work across sessions, enhancing the usability and convenience of the simulator.

**Testing and Refinement:** To ensure the reliability and correctness of the implementation, I wrote unit tests to validate the functionality of each method. I iteratively refined the implementation based on test results and feedback, ensuring that the simulator met the specified requirements.

**Documentation:** Finally, I provided comprehensive project documentation via a README file. This documentation offered an overview of the file system simulator and provided guidance on how to use it effectively, contributing to its usability and accessibility.

## Test Results Explanation:

### Test `test_mkdir`:
- **Outcome:** PASSED
- **Explanation:** This test verifies the functionality of the `mkdir` method, which creates a new directory in the file system. It checks whether the directory was successfully created and if it is marked as a directory in the file system's current directory. The test passed as the directory was created, and its properties were correctly set.

### Test `test_cd`:
- **Outcome:** PASSED
- **Explanation:** This test validates the functionality of the `cd` method, responsible for changing the current directory in the file system. It creates a directory, changes to it using `cd`, and checks if the current directory's name matches the expected name. The test passed as the current directory was successfully changed to the newly created directory.

### Test `test_ls`:
- **Outcome:** PASSED
- **Explanation:** The `test_ls` function tests the `ls` method, which lists the contents of the current directory in the file system. After creating a directory, the test invokes `ls` and verifies if the directory is listed among the current directory's contents. The test passed as the directory was correctly listed.

### Test `test_touch`:
- **Outcome:** PASSED
- **Explanation:** This test assesses the `touch` method's functionality, which creates a new file in the current directory of the file system. After creating a new file, the test checks if the file exists in the current directory and if it is marked as a file (not a directory). The test passed as the file was successfully created, and its properties were accurately set.

These tests passed as expected because the implemented methods behaved as intended, satisfying the specified requirements and functionality.

## Future scope - 
- we can save the current path by ctrl - c, but we cannot start from that path right now by using something like --load.
- I would work on this thing, any collaboration, help or suggestion is heartfully welcome.

## Appendix - 
https://docs.rtems.org/branches/master/filesystem/in-memory.html
