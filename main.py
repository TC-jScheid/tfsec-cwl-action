import os 
import json

def main():


    file_path = os.environ["INPUT_REPORT"]

    with open(file_path) as f:
        data = json.load(f)

        rules = data['runs'][0]['tool']['driver']['rules']

# Send to cloudwatch logs as 1 json object

        for r in rules:
            print(f"Rule: {r} ")

if __name__ == "__main__":
    main()
