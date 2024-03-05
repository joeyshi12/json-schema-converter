# json-data-type-transcompiler

![pytest.yml](https://github.com/joeyshi12/json-data-type-transcompiler/actions/workflows/pytest.yml/badge.svg)

A transcompiler from JSON to a programming language by inferring types from the JSON values.

A web interface for using this library is provided at <a href="https://devtools.joeyshi.xyz">devtools.joeyshi.xyz</a>

## Usage

```
usage: jdtt [-h] [-l {python,typescript,java,scala}] [-n SCHEMA_NAME] [-s] [-d DATE_FORMAT] [json_file]

positional arguments:
  json_file                            JSON filepath

options:
  -h                                   show this help message and exit
  -l {python,typescript,java,scala}    target language for transpilation
  -n SCHEMA_NAME                       name of the schema
  -s                                   sanitize symbol names in schema
  -d DATE_FORMAT                       regex for detecting date fields
```
