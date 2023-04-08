import os
import sys
import preprocessing
from utils import _load_json, _schema_to_json, _validate_json


def help_info():
    """
    Help information for utilising the command line tool
    """
    print("Usage: framework [options] [ config.json ]\n")
    print("Options:")
    print("\t--run\t\tRun the framework to generate clients using the config.json")
    print("\t--generate\tGenerate a template empty filled config.json")


def run(file):
    config_json_schema = _load_json("config_schema.json")
    config = _load_json(file)
    _validate_json(config, config_json_schema)
    preprocessing.generator(file)
    

def generate(file):
    config_json_schema = _load_json("config_schema.json")
    json_string = _schema_to_json(config_json_schema)
    if os.path.isfile(file):
        print(f"File ${file} already exists!")
        print("Do you want to overwrite? [Y]es/[N]o: ")
        option = input()
        option = option.lower()
        if option == "y" or option == "yes":
            f = open(file, "w")
            f.write(json_string)
            f.close()
            return
        elif option != "n" and option != "no":
            print("Invalid option!")
        print("Aborting generation operation!")
    else:
        f = open(file, "w")
        f.write(json_string)
        f.close()


def main():
    args = sys.argv

    """
    Command line tool rule evaluator engine
    """
    if len(args) == 2:
        # default behaviour: run
        run(args[1])
    elif len(args) == 3:
        option = args[1].lstrip("-").strip()
        if option == "run":
            run(args[2])
        elif option == "generate":
            generate(args[2])
        else:
            print("Error: Invalid option")
            help_info()
    else:
        help_info()


main()
