import sys

from src import manager


def run():
    if len(sys.argv) < 2:
        raise ValueError("Argument not provided: file path name")
    file_path_name = sys.argv[1]
    manager.show_file_analysis(file_path_name)


if __name__ == "__main__":
    run()
