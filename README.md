# An integration of federated learning with blockchain for credit assessment

## Set Up

```bash
# Create new environment using anaconda
conda create --name env-name python=3.8

# Activate newly created environment
conda activate env-name

# Install required packages
pip install -r requirements.txt

# Deactivate environment
conda deactivate env-name
```

## Getting started

## Decentralized Federated Learning

### Generate clients

- Configure `constants.py` to edit `SOURCE_CSV` and `SERVER_ADDRESS`

```bash
python preprocessing.py
```

### Run clients

```bash
# Change into the directory of the client you wish to execute
cd path/of/client

# Initiating client of FL round
python client.py initiator

# Participating client in FL round
python client.py client
```

## Credits

Dataset: [Lending Club 2007-2018](https://www.kaggle.com/datasets/wordsforthewise/lending-club)
Source: [Kaggle](https://www.kaggle.com/)

Created and maintained by Undergraduate Students of the Sri Sivasubramaniya Nadar College of Engineering, Kalavakkam as part of the curriculum to apply the engineering concepts applied thus far to come up with a innovative solution to a prevalent problem

- Anandh Krushna SK
- Aravind Kannan Rathinasabapathi
