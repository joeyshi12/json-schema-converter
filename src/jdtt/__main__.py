import json
import argparse
from jdtt.transcompilation import transcompile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_language", type=str, choices=["python", "scala", "typescript"], default="python", help="target language")
    parser.add_argument("--schema_name", type=str, default="Schema", help="name of the schema")
    parser.add_argument("--detect_date", action="store_true", help="detect datetime fields and convert to date type")
    parser.add_argument("--output", type=str, required=True, help="output filepath")
    parser.add_argument("json_path", type=str, help="json filepath")
    args = parser.parse_args()

    json_path = args.json_path
    output_path = args.output
    target_language = args.target_language.lower()
    date_format = r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2})?(\.\d{3})?Z" if args.detect_date else None

    with open(json_path, "r", encoding="utf-8") as f:
        schema_json = json.load(f)

    with open(output_path, "w", encoding="utf-8") as f:
        schema_str = transcompile(schema_json, target_language, date_format)
        f.write(schema_str)
        print(f"{args.target_language} schemas written to {output_path}")


if __name__ == "__main__":
    main()
