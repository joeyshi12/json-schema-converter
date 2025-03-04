import sys
import select
import json
import argparse
from jdtt.transcompilation import transcompile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", type=str, choices=["python", "typescript", "java", "scala", "proto"], default="python", help="target language for transcompilation")
    parser.add_argument("-n", "--schema_name", type=str, default="Schema", help="name of the schema")
    parser.add_argument("-s", "--sanitize_symbols", action="store_true", help="sanitize symbol names in schema")
    parser.add_argument("-d", "--date_format", type=str, help="regex for detecting date fields from string fields")
    parser.add_argument("json_file", type=argparse.FileType("r"), nargs="?", help="JSON filepath")
    args = parser.parse_args()

    json_file = args.json_file if sys.stdin.isatty() else sys.stdin
    if json_file is None:
        parser.print_help()
        sys.exit(1)

    with json_file as f:
        try:
            schema_json = json.load(f)
            result = transcompile(
                schema_json,
                args.language,
                args.date_format, 
                args.schema_name,
                args.sanitize_symbols
            )
            sys.stdout.write(result)
            sys.exit(0)
        except Exception as e:
            sys.stderr.write(f"jdtt: {e}\n")
            sys.exit(1)

    sys.stderr.write("jdtt: failed to read file\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
