import json

default_values = {
    "string": "",
    "number": 0,
    "list": [],
    "dict": {},
    "boolean": False,
}

def _load_json(file):
    """
    Helper function: Convert JSON file into python dictionary
    """
    f = open(file, "r")
    data = json.loads(f.read())
    return data

def _validate_json(json_data, json_schema):
    """
    Helper function: Validate type matching in JSON
    """
    for k, v in json_schema.items():
        expected = default_values[v["type"]]
        received = json_data[k]
        if type(expected) != type(received):
            raise Exception(
                f"Validation Failed: Type mismatch for ${k}\n\tExpected: ${expected} \n\tReceived: ${received}"
            )


def _schema_to_json(s):
    """
    Helper function: JSON schema to JSON template
    """
    res = {k: default_values[v["type"]] for k, v in s.items()}
    return json.dumps(res)