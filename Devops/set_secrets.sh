#!/bin/bash

secret_string=$(aws secretsmanager get-secret-value --secret-id $ENVIRONMENT-payments-scheduler-secrets --query SecretString)
python ./Devops/populate_secrets_to_env.py "$secret_string"
