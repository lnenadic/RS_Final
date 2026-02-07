import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

DYNAMODB_ENDPOINT = "http://localhost:4566"
REGION_NAME = "eu-central-1"
TABLE_NAME = "Votes"


def get_dynamodb_resource():
    return boto3.resource(
        "dynamodb",
        endpoint_url=DYNAMODB_ENDPOINT,
        region_name=REGION_NAME,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )


def create_table_if_not_exists():
    dynamodb = get_dynamodb_resource()
    try:
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "vote_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "vote_id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        print(f"Tablica '{TABLE_NAME}' uspješno kreirana u regiji {REGION_NAME}.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"Tablica '{TABLE_NAME}' već postoji.")
        else:
            raise e


def save_vote_to_db(option: str) -> dict:
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(TABLE_NAME)

    vote_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    table.put_item(Item={"vote_id": vote_id, "option": option, "timestamp": timestamp})
    return {"vote_id": vote_id, "timestamp": timestamp}


def get_all_votes():
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(TABLE_NAME)

    response = table.scan()
    return response.get("Items", [])
