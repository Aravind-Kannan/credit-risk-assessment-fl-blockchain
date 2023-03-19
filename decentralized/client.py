# Standard ML Libraries
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
from blockchain import get_metrics_contract, get_web3_provider
from model import model_arch
from utils import _load_json

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
        model.save("model.h5")
        loss, accuracy = model.evaluate(x_val, y_val)
        return loss, {"accuracy": accuracy}

    return evaluate


def initiator():
    # Create strategy and run initiator
    strategy = SaveModelStrategy(evaluate_fn=get_evaluate_fn(model))

    # Start Flower server for n rounds of federated learning
    fl.server.start_server(
        server_address=config_file['server_address'],
        config=fl.server.ServerConfig(num_rounds=config_file['rounds']),
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
            x_train, y_train, epochs=config_file['epochs'], batch_size=config_file['batch_size'], validation_data=(x_test, y_test)
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
        tx_hash = metrics_contract.functions.setMetrics(
            int(results["loss"] * OFFSET), int(results["accuracy"] * OFFSET)
        ).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print("[CLIENT] fit: Results:", results)
        return model.get_weights(), len(x_train), results

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
        print("[CLIENT] fit: Eval accuracy:", accuracy)
        return loss, len(x_test), {"accuracy": float(accuracy)}


def client():
    fl.client.start_numpy_client(
        server_address=config_file['server_address'], client=FLClient()
    )

# ---------------------------------------------------Decentralization----------------------------------------------
DATASET = "./dataset.csv"
df = pd.read_csv(DATASET)
print(df.shape)

x = df.iloc[:, 0:-1].values
y = df.iloc[:, -1].values

config_file = _load_json(sys.argv[2] if len(sys.argv) >= 3 else 'config.json')
metrics_contract = get_metrics_contract(config_file)
web3 = get_web3_provider(config_file)
model = model_arch()
OFFSET = 100_000

if sys.argv[1] == "initiator":
    # Load data and model here to avoid the overhead of doing it in `evaluate` itself
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=config_file['initiator_test_size'], random_state=0
    )
    scaler = MinMaxScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    # Use the last 5k training examples as a validation set

    x_val, y_val = x_train[0:500], y_train[0:500]
    initiator()
elif sys.argv[1] == "client":
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=config_file['client_test_size'], random_state=0
    )
    print(x_train.shape[1])
    scaler = MinMaxScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    client()
