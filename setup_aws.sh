#!/bin/bash

# Create the .aws directory if it doesn't exist
mkdir -p ~/.aws

# Write the credentials file
cat <<EOL > ~/.aws/credentials
[default]
aws_access_key_id = YOUR_AWS_ACCESS_KEY
aws_secret_access_key = YOUR_AWS_SECRET_ACCESS_KEY
EOL

# Write the config file
cat <<EOL > ~/.aws/config
[default]
region = YOUR_REGION
EOL

echo "AWS credentials and config files have been set up."
