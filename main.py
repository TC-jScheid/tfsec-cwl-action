import os 
import json
import requests  # noqa We are just importing this to prove the dependency installed correctly


def main():
    #my_input = os.environ["tfsec.sarif"]
    file_path = os.environ["INPUT_PATH"]
    
    with open(os.environ["INPUT_PATH"]) as f:
        data = json.load(f)

        rules = data['runs'][0]['tool']['driver']['rules']

        for r in rules:
            print(f"Rule: {r} ")    
    


if __name__ == "__main__":
    main()
