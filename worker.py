import yaml
from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)

projects = [
    'my-project-1',
    'my-project-2'
]


def process_previous(iam_file_name, iam_newer_file_name):

    with open(iam_file_name) as iam_file:
        iam = yaml.safe_load(iam_file)
    with open(iam_newer_file_name) as iam_newer_file:
        iam_newer = yaml.safe_load(iam_newer_file)

    message = f"\nCompared with previous day:\n{iam_file_name.split('/')[-1]}\n"

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
        return message
    if not update:
        return f"{iam_file_name.split('/')[-1]} compared with today: No changes.\n"


@app.route('/compare')
@app.route('/Compare')
def compare():

    date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    message_cumulative = ""

    for project in projects:
        iam = f"{project}_iam_{date}"
        iam_newer = f"{project}_iam_newer"
        try:
            with open(iam) as iam_file:
                pass
        except FileNotFoundError:
            message_cumulative = message_cumulative + f"\nCan't find comparison with previous day: {iam}\n\n"
        message_cumulative = message_cumulative + process_previous(iam, iam_newer)

    return message_cumulative
