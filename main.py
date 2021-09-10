import os 
import json
import boto3
import time
import requests

def main():
    # Input Variables
    # AWS Credentials
    AWS_KEY_ID = os.environ["INPUT_AWS_KEY_ID"]
    AWS_KEY_SECRET = os.environ["INPUT_AWS_KEY_SECRET"]
    #File path of tfsec report
    file_path = os.environ["INPUT_REPORT"]
    # CWL Group
    cwl_group = os.environ["INPUT_CWL_GROUP"]
    # CWL Stream
    cwl_stream = os.environ["INPUT_CWL_STREAM"]

    #Github environment variables
    repository = os.environ["GITHUB_REPOSITORY"]
    author = os.environ["GITHUB_ACTOR"]
    commit = os.environ["GITHUB_SHA"]
    branch = os.environ["GITHUB_REF"]
    #Initialize rules list
    rules = []
    #Instantiate client with CWL
    client = boto3.client(
                            'logs', 
                            region_name='us-east-1', 
                            aws_access_key_id=AWS_KEY_ID, 
                            aws_secret_access_key=AWS_KEY_SECRET
                        )
    
    with open(file_path) as f:
        data = json.load(f)
        # CAREFULLY DECONSTRUCTED from serif format
        rules = data['runs'][0]['tool']['driver']['rules']

    #TODO: Check if PR and comment rules
    output = commentRules(rules)
    
    #Check if CWL stream is created
    try:
        client.create_log_stream(
            logGroupName=cwl_group,
            logStreamName=cwl_stream
        )
    except:
        print(f"Log Stream, {cwl_stream}, already exists")

    # Build dir to send
    message = {}
    message['Repository'] = repository
    message['Branch'] = branch
    message['User'] = author
    message['Commit'] = commit
    message['Rule_Count'] = len(rules) #Get number of rules
    message['Rules'] = rules

    # Get stream status
    response = client.describe_log_streams(
        logGroupName=cwl_group,
        logStreamNamePrefix=cwl_stream
    )

    # Get current timestamp
    timestamp = int(round(time.time() * 1000))

    event_log = {
        'logGroupName': cwl_group,
        'logStreamName': cwl_stream,
        'logEvents': [
            {
                'timestamp': timestamp, 
                'message': json.dumps(message)
            }
        ]
    }

    if 'uploadSequenceToken' in response['logStreams'][0]:
           event_log.update({'sequenceToken': response['logStreams'][0] ['uploadSequenceToken']})

    putResponse = client.put_log_events(**event_log)

    
    print(f'Put log event to {cwl_group} / {cwl_stream}')

def commentRules(rules):
    #Get github token
    token = os.environ('INPUT_GITHUB_TOKEN')
    branch = os.environ["GITHUB_REF"]
    repository = os.environ["GITHUB_REPOSITORY"]
    #Connect to github
    g = Github(token)
    repo = g.get_repo(repository)

    i = repo.create_issue(
        title = 'Issue 1',
        body = json.dumps(rules[0]),
        assignee = 'TC-jScheid',
        labesl = [
            'tfsec'
        ]
    )

    

if __name__ == "__main__":
    main()
