import sys
import json

if len(sys.argv) != 2:
    print('Valid usage: ', sys.argv[0], ' <secret-string>')
    exit(1)

secret_string = sys.argv[1]
secrets = json.loads(json.loads(secret_string))

with open('secrets.json', 'w') as f:
    json.dump(secrets, f)
