import sys
import json
import os

print(os.getcwd())
challenge_name = os.getenv('CHALLENGE_NAME')
with open(f'workspace/code/{challenge_name}/metrics.json') as metrics_file:
    metrics_json = json.load(metrics_file)
    status_codes = metrics_json.get('status_codes', {})
    num_of_200s = status_codes.get('200', 0)
    print(f'{num_of_200s} requests received 200')
