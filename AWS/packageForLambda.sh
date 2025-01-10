#!/bin/bash

# This script automates the packaging process for deploying a Python script to AWS Lambda.
# It installs necessary dependencies, packages the script, and zips everything into a 
# deployable format for Lambda.

# Step 1: Create a temporary directory named "package" to hold the dependencies and script files.
mkdir -p package

# Step 2: Use pipreqs to generate a requirements.txt file based on the Python scripts in the current directory.
# The '--force' flag overwrites any existing requirements.txt file.
# The '--ignore package' flag ensures pipreqs ignores the "package" directory.
pip3 install pipreqs  # Ensure pipreqs is installed
pipreqs . --force --ignore package

# Step 3: Install all the required Python packages listed in requirements.txt into the "package" directory.
pip3 install -r requirements.txt -t ./package

# Step 4: Copy all Python script files from the current directory into the "package" directory.
cp *.py ./package

# Step 5: Navigate into the "package" directory to prepare for zipping.
cd package

# Step 6: Create a zip file named "lambda_function.zip" containing all the contents of the "package" directory.
# This zip file will be the deployable package for AWS Lambda.
zip -r ../lambda_function.zip .

# Step 7: Return to the original directory after zipping.
cd ..

# Step 8: (Optional) Clean up by removing the "package" directory and requirements.txt file.
rm -rf package requirements.txt