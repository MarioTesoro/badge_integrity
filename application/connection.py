import json
import os
import inspect
from pathlib import Path
from web3 import Web3

# Python 3.13 removed inspect.getargspec; some web3 deps still expect it.
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_CONTRACTS_DIR = REPO_ROOT / "build" / "contracts"
DEPLOYMENT_CONFIG = REPO_ROOT / "deployment_config.json"


def get_web3():
    # Allow custom RPC without changing code.
    provider_uri = os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:8545")
    return Web3(Web3.HTTPProvider(provider_uri))


def get_contract_abi():
    certification_json_path = BUILD_CONTRACTS_DIR / "Certification.json"
    try:
        with open(certification_json_path, "r") as json_file:
            certification_data = json.load(json_file)
            return certification_data.get("abi", [])
    except FileNotFoundError:
        print(f"Error: {certification_json_path} not found.")
        return []


def get_contract_address():
    try:
        with open(DEPLOYMENT_CONFIG, "r") as json_file:
            address_data = json.load(json_file)
        return address_data.get("Certification")
    except FileNotFoundError:
        print(f"Error: {DEPLOYMENT_CONFIG} not found.")
        return None


w3 = get_web3()
contract_abi = get_contract_abi()
contract_address = get_contract_address()

contract = None
if contract_abi and contract_address:
    # Create the contract handle only when artifacts + address are present.
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
