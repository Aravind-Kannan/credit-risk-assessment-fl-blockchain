# Standard ML Libraries
import threading
import pandas as pd
import numpy as np
import sys

# Scikit-learn Library Dependecies
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Federated Learning Package with its associated types
import flwr as fl
from typing import Optional, Dict, Tuple

# Blockchain
import web3

# Local dependencies
from blockchain import get_model_contract, get_web3_provider, get_hash_storage_local_contract, get_hash_storage_global_contract, upload_to_ipfs
from model import model_arch
from utils import _load_json

import datetime

# ---------------------------------------------------Initiator----------------------------------------------
class SaveModelStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(self, rnd, results, failures):
        print("[INITIATOR] Calling aggregate_fit...")
        aggregated_weights = super().aggregate_fit(rnd, results, failures)
        if aggregated_weights is not None:
            # Save aggregated_weights locally
            print(f"[INITIATOR] Saving round {rnd} aggregated_weights...")
            np.savez(f"round-{rnd}-weights.npz", *aggregated_weights)
        return aggregated_weights


def get_evaluate_fn(model):
    """Return an evaluation function for initiator-side evaluation."""

    # The `evaluate` function will be called after every round
    def evaluate(
        rounds: int,
        parameters: fl.common.NDArrays,
        config: Dict[str, fl.common.Scalar],
    ) -> Optional[Tuple[float, Dict[str, fl.common.Scalar]]]:
        model.set_weights(parameters)  # Update model with the latest parameters
        filename = f"global_{int(datetime.datetime.now().timestamp())}.h5"
        model.save(filename)
        print(f"[INITIATOR] Rounds: {rounds}")
        print(f"[INITIATOR] Saving {filename} file...")

        hash_value = upload_to_ipfs(filename)
        tx_hash = hash_storage_global_contract.functions.storeHash(hash_value, config_client["application_folder"]).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"[INITIATOR] Uploading {filename} file to IPFS...")
        print(f"[INITIATOR] {filename} hash: {hash_value}")

        loss, accuracy = model.evaluate(x_val, y_val)
        result = model_contract.functions.setValues(
            int(accuracy * OFFSET), int(loss * OFFSET), config_client["application_folder"]
        ).transact()
        print(f"[INITIATOR] Loss: {round(loss, 4) * 100} %   Accuracy: {round(accuracy, 4) * 100} %...")
        print(f"[INITIATOR] {filename} hash: {hash_value}")

        global round_number
        round_number += 1
        
        return loss, {"accuracy": accuracy}

    return evaluate


def initiator():
    # Create strategy and run initiator
    strategy = SaveModelStrategy(evaluate_fn=get_evaluate_fn(model))

    # Start Flower server for n rounds of federated learning
    fl.server.start_server(
        server_address=config_client['server_address'],
        config=fl.server.ServerConfig(num_rounds=config_client['rounds']),
        grpc_max_message_length=1024 * 1024 * 1024,
        strategy=strategy,
    )


# ---------------------------------------------------Client----------------------------------------------
class FLClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        print("[CLIENT] Calling get_parameters...")
        return model.get_weights()

    def fit(self, parameters, config):
        print("[CLIENT] Calling fit...")
        model.set_weights(parameters)
        print("[CLIENT] fit: After setting weights")

        print("[CLIENT] fit: Before model.fit")
        history = model.fit(
            x_train, y_train, epochs=config_client['epochs'], batch_size=config_client['batch_size'], validation_data=(x_test, y_test)
        )
        print("[CLIENT] fit: After model.fit")

        # hist=pd.DataFrame(history.history)
        print(
            "[CLIENT] fit: Fit history (accuracy) in client:",
            history.history["accuracy"],
        )
        results = {
            "loss": history.history["loss"][0],
            "accuracy": history.history["accuracy"][0],
            "val_loss": history.history["val_loss"][0],
            "val_accuracy": history.history["val_accuracy"][0],
        }
        
        filename = f"local_{int(datetime.datetime.now().timestamp())}.h5"
        model.save(filename)
        print(f"[CLIENT] Saving {filename} file...")

        hash_value = upload_to_ipfs(filename)
        tx_hash = hash_storage_local_contract.functions.storeHash(hash_value, config_client["application_folder"]).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"[CLIENT] Uploading {filename} file to IPFS...")
        print(f"[CLIENT] {filename} hash: {hash_value}")

        print("[CLIENT] fit: Results:", results)

        global round_number
        round_number += 1

        return model.get_weights(), len(x_train), results

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
        print("[CLIENT] fit: Eval accuracy:", accuracy)
        return loss, len(x_test), {"accuracy": float(accuracy)}


def client(address):
    fl.client.start_numpy_client(
        server_address=address, client=FLClient()
    )

# ---------------------------------------------------Decentralization----------------------------------------------
DATASET = "./dataset.csv"
df = pd.read_csv(DATASET)
print(df.shape)

x = df.iloc[:, 0:-1].values
y = df.iloc[:, -1].values

config_client = _load_json(sys.argv[2] if len(sys.argv) >= 3 else 'config.json')
model_contract = get_model_contract(config_client)
hash_storage_local_contract = get_hash_storage_local_contract(config_client)
hash_storage_global_contract = get_hash_storage_global_contract(config_client)
web3 = get_web3_provider(config_client)
model = model_arch()
OFFSET = 100_000

# ---------------------------------------------------Flask Hosting----------------------------------------------
from flask import Flask, Response
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from enum import Enum
from flask_cors import CORS, cross_origin

class JOB_STATUS(Enum):
    IDLE = 0
    RUNNING = 1

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Federated Learning API',
    description='Flower based job runner',
)

ns = api.namespace('jobs', description='Jobs and their status')

job = api.model('Job', {
    'name': fields.String(required=True, description='The job identifier'),
    'status': fields.String(required=True, description='The job status'),
})

local_address = api.model('Local Address', {
    'address': fields.String(required=True, description='The address of the system'),
})

round_info = api.model('Round Info', {
    'round': fields.Integer(required=True, description='The round number'),
    'total_rounds': fields.Integer(required=True, description='The total number of rounds'),
})

job_status_tracker = {
    'client': JOB_STATUS.IDLE,
    'initiator':JOB_STATUS.IDLE,
}

round_number = 0

# class syntax
@ns.route('/initiator')
class InitiatorJob(Resource):
    @api.marshal_with(job)
    def get(self):
        return {
            'name': 'initiator',
            'status': job_status_tracker['initiator'].name
        }
    
    def post(self):
        global x_train, x_test, y_train, y_test, x_val, y_val, round_number

        round_number = 0

        # Load data and model here to avoid the overhead of doing it in `evaluate` itself
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=config_client['initiator_test_size'], random_state=0
        )
        scaler = MinMaxScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        # Use the last 5k training examples as a validation set

        x_val, y_val = x_train[0:500], y_train[0:500]

        def initiator_handler():
            global job_status_tracker, round_number
            initiator()
            job_status_tracker['initiator'] = JOB_STATUS.IDLE

        if job_status_tracker['initiator'] == JOB_STATUS.IDLE and job_status_tracker['client'] == JOB_STATUS.IDLE:
            thread = threading.Thread(target=initiator_handler)
            thread.start()
            job_status_tracker['initiator'] = JOB_STATUS.RUNNING
            return {
                'name': 'initiator',
                'status': job_status_tracker['initiator'].name
            }
        else:
            return Response("Job already running", status=400)

@ns.route('/client')
class ClientJob(Resource):
    @api.marshal_with(job)
    def get(self):
        return {
            'name': 'client',
            'status': job_status_tracker['client'].name
        }

    @api.expect(local_address)
    def post(self):    
        global x_train, x_test, y_train, y_test, round_number

        round_number = 0

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=config_client['client_test_size'], random_state=0
        )
        print(x_train.shape[1])
        scaler = MinMaxScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)

        def client_handler(address):
            global job_status_tracker
            client(address)
            job_status_tracker['client'] = JOB_STATUS.IDLE

        if job_status_tracker['initiator'] == JOB_STATUS.IDLE and job_status_tracker['client'] == JOB_STATUS.IDLE:
            thread = threading.Thread(target=client_handler, args=(api.payload['address'],))
            thread.start()
            job_status_tracker['client'] = JOB_STATUS.RUNNING
            return {
                'name': 'client',
                'status': job_status_tracker['client'].name
            }
        else:
            return Response("Job already running", status=400)
    
@ns.route('/initiator/address')
class InitiatorAddress(Resource):
    @api.marshal_with(local_address)
    def get(self):
        return {
            'address': config_client['ip_address']
        }
    

@ns.route('/initiator/rounds')
class IntiatorRounds(Resource):
    @api.marshal_with(round_info)
    def get(self):
            return {
                'round': round_number,
                'total_rounds': config_client['rounds'] + 1
            }

@ns.route('/client/rounds')
class ClientRounds(Resource):        
    @api.marshal_with(round_info)
    def get(self):
        return {
            'round': round_number,
            'total_rounds': config_client['rounds']
        }

if __name__ == '__main__':
    app.run(debug=True, port=5000)