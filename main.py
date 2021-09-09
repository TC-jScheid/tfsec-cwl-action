import os 
import json
import boto3

def main():

    AWS_KEY_ID = os.environ["AWS_KEY_ID_GITHUB_ACTIONS"]
    AWS_KEY_SECRET = os.environ["AWS_KEY_SECRET_GITHUB_ACTIONS"]
    file_path = os.environ["INPUT_REPORT"]

    with open(file_path) as f:
        data = json.load(f)

        rules = data['runs'][0]['tool']['driver']['rules']

# Send to cloudwatch logs as 1 json object
        print(f"Sending rules using key: {AWS_KEY_ID}")

        for r in rules:
            print(f"Rule: {r} ")

if __name__ == "__main__":
    main()
