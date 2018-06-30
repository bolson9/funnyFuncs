import json
import datetime
import logging
import boto3
import os
import common
import json

logger = logging.getLogger('subscribe')
logger.setLevel(logging.DEBUG)

categories = ['quote', 'fact', 'joke']

def create_subscription_db_entry(subscription_info):
    logger.info("Getting boto3 dynamodb resource")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    logger.debug("Saving subscription")
    table.put_item(
        Item = subscription_info
    )

def create_sns_subscription(subscription_info):
    logger.info("Gettinb boto3 sns resource")
    sns_resource = boto3.resource('sns')
    logger.debug("Obtained sns boto3 resource")

    sns_topic = sns_resource.Topic(common.get_topic_arn(subscription_info['category']))
    logger.debug("After switch statement to get sns topic")
    
    sns_topic.subscribe(
        Protocol='email',
        Endpoint=subscription_info['email']
        )
    logger.debug("After attempting to subscript")

def handler(event, context):
    logger.info("Handling lambda event")
    
    logger.debug("Lambda Event keys: " + str(event.keys()))
    
    body = json.loads(event['body'])
    
    logger.debug("Request Body keys: " + str(body.keys()))

    # set default category - everybody loves jokes
    category = 'joke'
    
    # set default hour - everybody loves mornings
    hour = 8
    
    # Check for an email, return a 500 if one is not found
    if not 'email' in body:
        logger.error("Request with no email in body")
        return common.return_server_error('Email field is required')
    else:
        email = body['email']

    # Check that the category is valid
    if 'category' in body:
        if body['category'] in categories:
            category = body['category']
        else:
            logger.error("Invalid category %s", category)
            return common.return_server_error('Category ' + category + ' is invalid. Must be one of ' + str(category))

    if 'hour' in body:
        hour = body['hour']
    
    subscription_info = {    'email': email,
                'category': category,
                'hour': hour,
                'Active': True
            }
    logger.debug("Updating table %s", os.environ['TABLE_NAME'])
    logger.debug("Creating subscription: %s", str(subscription_info))
    try:
        create_subscription_db_entry(subscription_info)
    except Exception as e:
        return common.return_server_error('Error saving subscription to dynamodb: ' + str(e))

    create_sns_subscription(subscription_info)
    try:
        create_sns_subscription(subscription_info)
    except Exception as e:
        return common.return_server_error('Error saving subscription to sns: ' + str(e))

    return {'statusCode': 200,
            'body': 'Successfully created subscription',
            'headers': {'Content-Type': 'application/json'}}
