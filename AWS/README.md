
# AWS Lambda Scripts Repository

This repository contains a collection of Python scripts designed to interact with various AWS services. The included bash script simplifies the process of packaging Python scripts and their dependencies for deployment to AWS Lambda.

## Features

- Automatically generates a `requirements.txt` file using `pipreqs`
- Installs all required dependencies into a dedicated directory
- Packages Python scripts and dependencies into a deployable `.zip` file
- Streamlines deployment to AWS Lambda

## Files

- `package_lambda.sh`: A bash script that handles packaging and zipping.
- `lambda_function.zip`: The deployable Lambda package created by the script.
- Python script files: Custom Python code to interact with AWS services.

## Usage

1. Run the bash script:
   ```bash
   ./package_lambda.sh
   ```

2. The deployable `lambda_function.zip` file will be created in the current directory.

3. Upload the zip file to AWS Lambda for deployment.

## Prerequisites

- Python 3.x installed
- `pipreqs` installed
- AWS Lambda-compatible Python scripts

## Notes

- Make sure the scripts in this repository are AWS Lambda-compatible.
- You may customize the bash script for specific project needs.

## License

This repository is licensed under the MIT License. See the `LICENSE` file for details.
