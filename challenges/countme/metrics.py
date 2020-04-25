import os
import requests
import json

challenge_name = os.getenv('CHALLENGE_NAME')
test_rate = int(os.getenv('rate', 200))
test_duration = int(os.getenv('duration', 200))
ENDPOINT = os.getenv('ENDPOINT', 'http://localhost:8080')
validation_result = {}
with open(f'workspace/code/{challenge_name}/payload.txt') as payload_file:
    payload = int(payload_file.read())
expected_result = test_rate * test_duration  * payload

try:
    response = requests.get(f'{ENDPOINT}/count')
    if response.status_code != 200:
        validation_result['status'] = 'FAILED'
        validation_result['reason'] = f'/count returned status code {response.status_code}'
    elif int(response.text) != expected_result:
        validation_result['status'] = 'FAILED'
        validation_result['reason'] = f'/count returned values is {response.text} but should be {expected_result}'
    else:
        validation_result['status'] = 'SUCCEEED'

except Exception as e:
    validation_result['status'] = 'FAILED'
    validation_result['reason'] = f'{e}'

with open(f'workspace/code/{challenge_name}/metrics.json') as metrics_file:
    metrics_json = json.loads(metrics_file.read())
    metrics_json['validation_result'] = validation_result
    print(json.dumps(metrics_json))
