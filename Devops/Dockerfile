ARG AWS_ACCOUNT_ID
ARG AWS_REGION
FROM $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/coi-base-images:python-3.9.1

WORKDIR /app
COPY scheduler_api/ ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

ENTRYPOINT gunicorn --chdir service wsgi:app -b 0.0.0.0:80
