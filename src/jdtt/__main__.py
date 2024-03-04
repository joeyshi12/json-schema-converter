import sys
import json
import argparse
from jdtt.transcompilation import transcompile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", type=str, choices=["python", "scala", "typescript"], default="python", help="target language for transpilation")
    parser.add_argument("-n", "--schema_name", type=str, default="Schema", help="name of the schema")
    parser.add_argument("-d", "--detect_date", action="store_true", help="include to infer datetime fields")
    parser.add_argument("json_path", type=str, help="JSON filepath")
    args = parser.parse_args()

    json_path = args.json_path
    target_language = args.language.lower()
    schema_name = "Schema" if args.schema_name is None else args.schema_name
    date_format = r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2})?(\.\d{3})?Z" if args.detect_date else None

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            schema_json = json.load(f)
            result = transcompile(schema_json, target_language, date_format, schema_name)
            sys.stdout.write(result)
            return
        except Exception as e:
            pass

    sys.stderr.write("Invalid JSON file: " + json_path)


if __name__ == "__main__":
    main()
