#!/bin/python

import sys
import json

if len(sys.argv) != 2:
    print('Valid usage: ', sys.argv[0], ' <secret-name>')
    exit(1)

secret_name = sys.argv[1]

with open('secrets.json', 'r') as f:
    secrets = json.load(f)
    print(secrets[secret_name])
