# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

import boto3
import os
import json
import logging
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")


def handler(event, context):
    table = os.environ.get("TABLE_NAME")
    
    # Log request context for security auditing
    request_context = event.get("requestContext", {})
    identity = request_context.get("identity", {})
    
    logger.info(f"Request ID: {context.request_id}")
    logger.info(f"Source IP: {identity.get('sourceIp', 'unknown')}")
    logger.info(f"User Agent: {identity.get('userAgent', 'unknown')}")
    logger.info(f"Request Time: {request_context.get('requestTime', 'unknown')}")
    logger.info(f"Table name: {table}")
    
    try:
        if event["body"]:
            item = json.loads(event["body"])
            logger.info(f"Received payload: {item}")
            year = str(item["year"])
            title = str(item["title"])
            id = str(item["id"])
            dynamodb_client.put_item(
                TableName=table,
                Item={"year": {"N": year}, "title": {"S": title}, "id": {"S": id}},
            )
            logger.info(f"Successfully inserted item with id: {id}")
            message = "Successfully inserted data!"
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": message}),
            }
        else:
            logger.info("Received request without a payload")
            default_id = str(uuid.uuid4())
            dynamodb_client.put_item(
                TableName=table,
                Item={
                    "year": {"N": "2012"},
                    "title": {"S": "The Amazing Spider-Man 2"},
                    "id": {"S": default_id},
                },
            )
            logger.info(f"Inserted default item with id: {default_id}")
            message = "Successfully inserted data!"
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": message}),
            }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal server error"}),
        }
