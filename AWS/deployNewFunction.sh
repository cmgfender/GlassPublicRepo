#!/bin/bash

# Define variables
FUNCTION_NAME="my_lambda_function"
ROLE_ARN="arn:aws:iam::123456789012:role/lambda-role"
ZIP_FILE="lambda_function.zip"

# Create a new Lambda function
aws lambda create-function \
  --function-name $FUNCTION_NAME \
  --runtime python3.8 \
  --role $ROLE_ARN \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://$ZIP_FILE