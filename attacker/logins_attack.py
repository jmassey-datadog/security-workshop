import json
import random

import requests

LOGIN_URL = 'http://server:80/login'
EXPECTED_STATUS_CODES = [200, 401]

with open('attacker_ips.json') as f:
    attacker_ips = json.load(f)

with open('user_breach_db.json') as f:
    user_breach_db = json.load(f)

with open('compromised_users.json') as f:
    compromised_users = json.load(f)



def login(username, password, ip):
    headers = {
        "X_FORWARDED_FOR": ip
    }
    body = {
        "user": username,
        "password": password,
    }
    r = requests.post(LOGIN_URL, headers=headers, json=body)
    if r.status_code not in EXPECTED_STATUS_CODES:
        r.raise_for_status()


if __name__ == "__main__":
    # todo: ensure some logins are for users in the database
    for user in compromised_users:
        login(user, user, random.choice(attacker_ips))

    for user in user_breach_db:
        login(user, "invalid_password", random.choice(attacker_ips))

