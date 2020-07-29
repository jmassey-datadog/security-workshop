import json
import random
from time import sleep
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import requests

LOGIN_URL = 'http://server:80/login'
EXPECTED_STATUS_CODES = [200, 401]

with open('legitimate_ips.json') as f:
    legitimate_ips = json.load(f)

with open('users.json') as f:
    users = json.load(f)



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
    while True:
        user = users[random.choice(list(users))]
        ip = random.choice(legitimate_ips[str(user.get('tenant_id'))])
        login(user['username'], user['password'], ip)
        logger.info('logging in as {}'.format(user['username']))
        t = random.randint(30, 60)
        logger.info('sleeping for {} seconds'.format(t))
        sleep(t)

