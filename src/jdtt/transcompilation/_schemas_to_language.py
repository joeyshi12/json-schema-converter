from jdtt.schema import Schema, SchemaDataType, SchemaBasicDataType, \
    SchemaListDataType, SchemaReference, SchemaListDataType, DataType
from jdtt.exceptions import JDTTException


def schemas_to_python(schema_dict: dict[str, Schema]) -> str:
    schema_str_list = [_schema_to_python(schema) for _, schema in schema_dict.items()]
    import_statements_str = "from datetime import datetime\nfrom dataclasses import dataclass\n\n"
    return import_statements_str + "\n\n".join(schema_str_list)


def _schema_to_python(schema: Schema) -> str:
    data_type_to_symbol = {
        DataType.BOOLEAN: "bool",
        DataType.INTEGER: "int",
        DataType.FLOAT: "float",
        DataType.STRING: "str",
        DataType.DATE: "datetime",
        DataType.UNKNOWN: "object"
    }
    list_formatter = "list[{}]"
    field_str_list = []

    for field in schema.fields:
        type_symbol = _get_type_symbol(field.data_type, data_type_to_symbol, list_formatter)
        field_str_list.append(f"    {field.name}: {type_symbol}")

    fields_str = "\n".join(field_str_list) if len(field_str_list) > 0 else "    pass"
    return f"@dataclass\nclass {schema.name}:\n{fields_str}"


def schemas_to_typescript(schema_dict: dict[str, Schema]):
    schema_str_list = [_schema_to_typescript(schema) for _, schema in schema_dict.items()]
    return "\n\n".join(schema_str_list)


def _schema_to_typescript(schema: Schema) -> str:
    data_type_to_symbol = {
        DataType.BOOLEAN: "boolean",
        DataType.INTEGER: "number",
        DataType.FLOAT: "number",
        DataType.STRING: "string",
        DataType.DATE: "Date",
        DataType.UNKNOWN: "any"
    }
    list_formatter = "{}[]"
    field_str_list = []

    for field in schema.fields:
        type_symbol = _get_type_symbol(field.data_type, data_type_to_symbol, list_formatter)
        field_str_list.append(f"    {field.name}: {type_symbol};")

    fields_str = "\n" + "\n".join(field_str_list) + "\n" if field_str_list else ""
    return f"export interface {schema.name} {{{fields_str}}}"


def schemas_to_java(schema_dict: dict[str, Schema]):
    schema_str_list = [_schema_to_java(schema) for _, schema in schema_dict.items()]
    import_statements_str = "import java.util.Date\n\n"
    return import_statements_str + "\n\n".join(schema_str_list)


def _schema_to_java(schema: Schema) -> str:
    data_type_to_symbol = {
        DataType.BOOLEAN: "boolean",
        DataType.INTEGER: "int",
        DataType.FLOAT: "float",
        DataType.STRING: "String",
        DataType.DATE: "Date",
        DataType.UNKNOWN: "AnyType"
    }
    list_formatter = "List[{}]"
    field_str_list = []

    for field in schema.fields:
        type_symbol = _get_type_symbol(field.data_type, data_type_to_symbol, list_formatter)
        field_str_list.append(f"    public {type_symbol} {field.name};")

    fields_str = "\n" + "\n".join(field_str_list) + "\n" if len(field_str_list) > 0 else ""
    return f"class {schema.name} {{{fields_str}}}"


def schemas_to_scala(schema_dict: dict[str, Schema]):
    schema_str_list = [_schema_to_scala(schema) for _, schema in schema_dict.items()]
    import_statements_str = "import org.joda.time.DateTime\n\n"
    return import_statements_str + "\n\n".join(schema_str_list)


def _schema_to_scala(schema: Schema) -> str:
    data_type_to_symbol = {
        DataType.BOOLEAN: "Boolean",
        DataType.INTEGER: "Int",
        DataType.FLOAT: "Float",
        DataType.STRING: "String",
        DataType.DATE: "DateTime",
        DataType.UNKNOWN: "Any"
    }
    list_formatter = "IndexedSeq[{}]"
    field_str_list = []

    for field in schema.fields:
        type_symbol = _get_type_symbol(field.data_type, data_type_to_symbol, list_formatter)
        field_str_list.append(f"    {field.name}: {type_symbol}")

    fields_str = "\n" + ",\n".join(field_str_list) + "\n" if len(field_str_list) > 0 else ""
    return f"case class {schema.name}({fields_str})"


def _get_type_symbol(schema_type: SchemaDataType,
                     data_type_to_symbol: dict[DataType, str],
                     list_formatter: str) -> str:
    match schema_type:
        case SchemaBasicDataType(data_type):
            if data_type not in data_type_to_symbol and DataType.UNKNOWN not in data_type_to_symbol:
                raise JDTTException(f"Missing symbol for data type {data_type}")
            return data_type_to_symbol.get(data_type, data_type_to_symbol[DataType.UNKNOWN])
        case SchemaListDataType(item_type):
            return list_formatter.format(_get_type_symbol(item_type, data_type_to_symbol, list_formatter))
        case SchemaReference(schema_name):
            return schema_name
        case _:
            raise JDTTException(f"Invalid schema type {schema_type}")
