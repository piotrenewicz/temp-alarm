import jsonschema
import json

INPUT_FILE_NAME = "input.json"
INPUT_SCHEMA_FILE_NAME = "input_schema.json"


def validate_schema(input_object):
    with open(INPUT_SCHEMA_FILE_NAME, 'r') as file:
        schema = json.load(file)

    jsonschema.validate(input_object, schema)

    return None


def get_input():
    with open(INPUT_FILE_NAME) as f:
        input_json = json.load(f)

    validate_schema(input_json)  # Validate the input

    return input_json
