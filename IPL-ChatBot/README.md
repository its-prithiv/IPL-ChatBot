# Prithiv README.md FILE


# IPL Chatbot

This repository contains the code and configuration for the IPL Chatbot built using Amazon Lex and AWS Lambda.

## Description

The IPL Chatbot provides information about IPL match details, including toss results, player of the match, venue details, and match results.

## Setup Instructions

### Prerequisites
- An AWS account with access to AWS Lex and AWS Lambda.
- AWS CLI installed and configured (if deploying via CLI).

### Deploying the Lambda Function
1. **Navigate to AWS Lambda:**
   - Go to the AWS Management Console and open the Lambda service.

2. **Create a New Lambda Function:**
   - Choose "Author from scratch."
   - Set a name for your function.
   - Choose a runtime (Python 3.x).
   - Set permissions (create a new role with basic Lambda permissions).

3. **Upload the Code:**
   - Under "Function code," select "Upload a .zip file."
   - Zip the contents of the `chatbot-package` directory:
     ```bash
     zip -r chatbot-package.zip lambda_function.py requirements.txt lex_bot_config.json
     ```
   - Upload `chatbot-package.zip`.

4. **Install Dependencies (if any):**
   - If you have dependencies in `requirements.txt`, you can install them locally, then include them in your zip, or use AWS Lambda Layers.

### Deploying the Lex Bot
1. **Navigate to AWS Lex:**
   - Open the AWS Management Console and go to the Lex service.

2. **Create a New Bot:**
   - Choose "Create."
   - Follow the prompts to create your bot based on the configuration in `lex_bot_config.json`.
   - Import the bot settings if supported, or recreate it manually based on the configuration.

## Testing the Chatbot
1. **Test in Lex Console:**
   - Use the built-in test interface in the Lex console to interact with the bot and verify functionality.

2. **Testing with Web UI:**
   - If you implemented a simple web UI, open the webpage in a browser and test various intents.

## Notes
- Ensure that your AWS Lambda function has permission to access other services if necessary (e.g., S3 for fetching data).
- Monitor logs in CloudWatch for troubleshooting any issues.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
