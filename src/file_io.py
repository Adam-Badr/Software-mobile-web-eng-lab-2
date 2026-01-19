# file_io.py
import os
import base64


def encode_file(path):
    """Read a file as bytes and return a base64-encoded UTF-8 string.

    Args:
        path (str): Path to the file to encode.

    Returns:
        str: Base64-encoded contents of the file, decoded as a UTF-8 string.

    Raises:
        FileNotFoundError: If `path` does not exist.
        PermissionError: If the file cannot be opened due to permissions.
        OSError: For other I/O related errors.
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def list_files(dirpath):
    """Yield (filename, full_path) for each regular file in a directory.

    This function lists direct children of `dirpath` (non-recursive) and yields
    only entries that are regular files (not directories).

    Args:
        dirpath (str): Path to the directory to scan.

    Yields:
        tuple[str, str]: A tuple of (name, path), where `name` is the file name
        and `path` is the absolute or joined file path.

    Raises:
        FileNotFoundError: If `dirpath` does not exist.
        NotADirectoryError: If `dirpath` is not a directory.
        PermissionError: If the directory cannot be listed due to permissions.
        OSError: For other OS-related errors.
    """
    for name in os.listdir(dirpath):
        path = os.path.join(dirpath, name)
        if os.path.isfile(path):
            yield name, path
