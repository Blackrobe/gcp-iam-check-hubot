import yaml
import requests
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='/etc/iambot/env')

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

iam_file_name = sys.argv[1]
iam_newer_file_name = sys.argv[2]

with open(iam_file_name) as iam_file:
    iam = yaml.safe_load(iam_file)
with open(iam_newer_file_name) as iam_newer_file:
    iam_newer = yaml.safe_load(iam_newer_file)

message = "\n" + iam_file_name.split('/')[-1] + "\n"

update = False
for binding in iam['bindings']:
    if binding not in iam_newer['bindings']:
        update = True
        message = message + "*" + binding['role'] + "*\n"
        found = False
        for binding_newer in iam_newer['bindings']:
            if binding_newer['role'] == binding['role']:
                found = True
                for member in binding['members']:
                    if member not in binding_newer['members']:
                        message = message + '- Removed: ' + member + "\n"
                for member_newer in binding_newer['members']:
                    if member_newer not in binding['members']:
                        message = message + '- Added: ' + member_newer + "\n"
        if not found:
            message = message + "All members removed\n"
            for member in binding['members']:
                message = message + '- Removed: ' + member + "\n"
            

binding_roles = []
for binding in iam['bindings']:
    binding_roles.append(binding['role'])
for binding in iam_newer['bindings']:
    if binding['role'] not in binding_roles:
        update = True
        message = message + '*New role: ' + binding['role'] + "*\n"
        for member in binding['members']:
            message = message + '- Added: ' + member + "\n"

if update:
    requests.post(WEBHOOK_URL, data = json.dumps({"text": message}), headers={'Content-Type': 'application/json'})
    print("Update sent for", iam_file_name)
