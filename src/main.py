# main.py
import json
import argparse
from . import file_io as io_mod
from . import gpt


def process_directory(dirpath):
    """Process all receipt images in a directory and extract structured fields.

    For each regular file in `dirpath`, this function:
    1) base64-encodes the file contents
    2) sends it to the OpenAI extraction function
    3) stores results under the filename key

    Args:
        dirpath (str): Directory containing receipt image files.

    Returns:
        dict[str, dict]: Mapping of filename -> extracted receipt fields dict.

    Raises:
        FileNotFoundError: If `dirpath` does not exist.
        NotADirectoryError: If `dirpath` is not a directory.
        PermissionError: If directory listing or file reading is not permitted.
        json.JSONDecodeError: If model output is not valid JSON.
        openai.OpenAIError: If the OpenAI API request fails.
    """
    results = {}
    for name, path in io_mod.list_files(dirpath):
        image_b64 = io_mod.encode_file(path)
        data = gpt.extract_receipt_info(image_b64)
        results[name] = data
    return results


def main():
    """CLI entry point.

    Parses command-line arguments:
      - dirpath (positional): directory containing receipt images
      - --print (flag): print extracted JSON to stdout

    Runs extraction over the directory and prints the resulting JSON mapping
    when --print is provided.

    Raises:
        SystemExit: Raised by argparse on invalid arguments.
        FileNotFoundError: If `dirpath` does not exist.
        NotADirectoryError: If `dirpath` is not a directory.
        PermissionError: If the directory or files cannot be accessed.
        json.JSONDecodeError: If model output is not valid JSON.
        openai.OpenAIError: If the OpenAI API request fails.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args()

    data = process_directory(args.dirpath)
    if args.print:
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
