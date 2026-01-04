import os
from dotenv import load_dotenv

load_dotenv()

_DUMMY_USERS = {
    os.getenv("verifier_email", "verifier@example.com"): os.getenv("verifier_password", "verifier123"),
    "demo@local.test": "demo1234",
}


def register(email, password):
    try:
        _DUMMY_USERS[email] = password
        print(email, password)
        return "success"
    except Exception as e:
        print(f"Error: {e}")
        return "failure"

def login(email, password):
    try:
        print(email, password)
        if _DUMMY_USERS.get(email) == password:
            return "success"
        return "failure"
    except Exception as e:
        print(f"Error: {e}")
        return "failure"
