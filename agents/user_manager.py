# user_manager.py 

import json
import os

BASE_DIR = os.path.dirname(__file__)
USER_FILE = os.path.join(BASE_DIR, "users.json")

def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump([], f)
    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(name, email, mobile):
    users = load_users()

    # Ensure unique email
    for u in users:
        if u["email"].lower() == email.lower():
            return False, "User already exists."

    new_user = {
        "name": name,
        "email": email,
        "mobile": mobile
    }

    users.append(new_user)
    save_users(users)

    return True, new_user   # Return user object directly
