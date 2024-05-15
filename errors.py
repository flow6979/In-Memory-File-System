class FileSystemError(Exception):
    pass

class FileNotFoundError(FileSystemError):
    pass

class DirectoryNotFoundError(FileSystemError):
    pass

class InvalidPathError(FileSystemError):
    pass
