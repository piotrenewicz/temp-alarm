import jsonschema
import json

INPUT_FILE_NAME = "input.json"
INPUT_SCHEMA_FILE_NAME = "input_schema.json"


def validate_schema(input_object: dict) -> None:
    with open(INPUT_SCHEMA_FILE_NAME, 'r') as file:
        schema = json.load(file)

    jsonschema.validate(input_object, schema)

    return None


def get_input() -> dict:
    with open(INPUT_FILE_NAME) as f:
        input_object = json.load(f)

    validate_schema(input_object)  # Validate the input

    return input_object

#
# def get_split_input() -> "tuple[list,list,dict]":
#     input_object = get_input()
#     sensors = input_object["sensors"]
#     mail_list = input_object["send_alarm_to_mails"]
#     glob = input_object
#
#     return sensors, mail_list
