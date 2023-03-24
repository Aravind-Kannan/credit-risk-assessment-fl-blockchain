import os, sys
import shutil
from utils import _load_json

def generator(config_file):
    config = _load_json(config_file)
    parent_dir = os.getcwd()
    directory = "generated"
    parent_path = os.path.join(parent_dir, directory)

    try:
        os.mkdir(parent_path)
    except:
        print("Deleting existing contents in folder...")
        shutil.rmtree(parent_path)
        os.mkdir(parent_path)

    NO_OF_CLIENTS = 3
    if config['number_of_clients'] >= 3:
        NO_OF_CLIENTS = config['number_of_clients']
    else:
        print("Minimum of 3 clients required...")

    exec(f'from {config["application_folder"]}.preprocessing import preprocess')
    df=eval("preprocess(config['source_csv'])")
    print(df.shape)

    for i in range(1, NO_OF_CLIENTS + 1):
        sampled_df = df.sample(frac=1.0 / NO_OF_CLIENTS, replace=False, random_state=1)
        print("Client ", i, ": ", sampled_df.shape)
        client_path = os.path.join(parent_path, "client" + str(i))
        application_path = config["application_folder"]
        try:
            os.mkdir(client_path)
        except:
            print("Already created path")
        try:
            shutil.copy("./client.py", client_path)
            shutil.copy("./blockchain.py", client_path)
            shutil.copy("./utils.py", client_path)
            shutil.copy(config_file, client_path)
            os.rename(client_path + "/" + config_file, client_path + "/config.json")
            for item in os.listdir(application_path):
                if item != "__pycache__":
                    shutil.copy(application_path + "/" + item, client_path)
            sampled_df.to_csv(client_path + "/dataset.csv")
        except:
            print("Copying and generating CSV failed")