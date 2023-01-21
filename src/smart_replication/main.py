#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import requests
import json
from utils import msg

CLIENT_SECRET = os.environ['SMART_REPLICATION_CLIENT_SECRET']
AUTH_SERVICE_TOKEN_URL = os.environ['AUTH_SERVICE_TOKEN_URL']
CHANGE_OWNER = os.environ['CHANGE_OWNER']
HA_SMART_REPLICATION_WEB_BASE_URL = os.environ['HA_SMART_REPLICATION_WEB_BASE_URL']

def get_token():
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"clientId": "gitlab-smart-replication-client","clientSecret": "%s"}' % (CLIENT_SECRET)

    print(msg.info('Try to get access token from auth-service...'))
    auth_response = requests.post(AUTH_SERVICE_TOKEN_URL, headers=headers, data=data)
    print(msg.info(f'Auth responce status code {auth_response.status_code}'))

    if auth_response.status_code == 200:
        token = json.loads(auth_response.content.decode('utf-8'))
        return token["accessToken"]
    else:
        sys.exit(1)

def change_replication_state(replication_enabled, auth_token=None):
    headers = { 'Authorization': f"Bearer {auth_token}" }

    rest_url = HA_SMART_REPLICATION_WEB_BASE_URL + "owners/" + CHANGE_OWNER + "/replication-state?replicationEnabled=" + replication_enabled
    ha_response = requests.put(rest_url, headers=headers)

    print(msg.info(f'Ha response status code {ha_response.status_code}'))
    if ha_response.status_code != 200:
        response_content = ha_response.content.decode('utf-8')
        print(msg.error(f'Status code {response_content}'))
        sys.exit(1)

def change_stand_in_state(stand_in_state, auth_token=None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {auth_token}"
    }

    data = '{"owner": "%s","newState": "%s", "ignoreRetryTopic": "true"}' % (CHANGE_OWNER, stand_in_state)

    rest_url = HA_SMART_REPLICATION_WEB_BASE_URL + "owners/" + CHANGE_OWNER + "/stand-in-state"
    ha_response = requests.put(rest_url, headers=headers, data=data)

    print(msg.info(f'Ha response status code {ha_response.status_code}'))
    if ha_response.status_code != 200:
        response_content = ha_response.content.decode('utf-8')
        print(msg.error(f'Status code {response_content}'))
        sys.exit(1)

if __name__ == '__main__':
    auth_token = get_token()
    print(msg.ok(f'Auth-token: {auth_token}'))

    command = sys.argv[1]
    if command == 'change_replication_state':
        enabled = sys.argv[2]
        change_replication_state(enabled, get_token())
    elif command == 'change_stand_in_state':
        stand_in_state = sys.argv[2]
        change_stand_in_state(stand_in_state, get_token())
    else:
        print(msg.error('Unknown command'))
        sys.exit(1)
