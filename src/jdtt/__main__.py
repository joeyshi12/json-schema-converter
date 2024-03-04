import sys
import select
import json
import argparse
from jdtt.transcompilation import transcompile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", type=str, choices=["python", "scala", "typescript"], default="python", help="target language for transpilation")
    parser.add_argument("-n", "--schema_name", type=str, default="Schema", help="name of the schema")
    parser.add_argument("-d", "--detect_date", action="store_true", help="include to infer datetime fields")
    parser.add_argument("json_file", type=argparse.FileType("r"), nargs="?", help="JSON filepath", default=None)
    args = parser.parse_args()

    if args.json_file is None and not select.select([sys.stdin, ], [], [], 0.0)[0]:
        parser.print_help()
        return

    json_file = sys.stdin if args.json_file is None else args.json_file
    target_language = args.language.lower()
    schema_name = "Schema" if args.schema_name is None else args.schema_name
    date_format = r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2})?(\.\d{3})?Z" if args.detect_date else None

    with json_file as f:
        try:
            schema_json = json.load(f)
            result = transcompile(schema_json, target_language, date_format, schema_name)
            sys.stdout.write(result)
            return
        except Exception as e:
            pass

    sys.stderr.write(f"Failed to transpile JSON object {json_path}")


if __name__ == "__main__":
    main()
