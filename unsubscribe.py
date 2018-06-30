import json
import datetime
import logging
import boto3
import os
import common

logger = logging.getLogger('unsubscribe')
logger.setLevel(logging.DEBUG)

categories = ['quote', 'fact', 'joke']

def disable_dynamo_subscription(email):
    logger.info("Getting boto3 dynamodb resource")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    table.update_item(
        Key={
            'email': email
        },
        UpdateExpression="set Active = :a",
        ExpressionAttributeValues={
            ':a': False
        
    },
    ReturnValues="UPDATED_NEW"
        )
    
def delete_sns_subscription(email, category):
    logger.info("Gettinb boto3 sns resource")
    sns_client = boto3.client('sns')
    logger.info("Finding arn to unsubscribe")
    sns_topic_subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=common.get_topic_arn(category))['Subscriptions']
    sns_topic_subscription = next(filter(lambda subscription: subscription['Endpoint'] == email, sns_topic_subscriptions))
    logger.debug("Deleting subscription arn: %s", sns_topic_subscription['SubscriptionArn'])
    sns_client.unsubscribe(SubscriptionArn=sns_topic_subscription['SubscriptionArn'])

def handler(event, context):
    logger.info("Handling lambda event")
    
    logger.info("Getting boto3 resource")
    
    dynamodb = boto3.client('dynamodb')
    
    body = json.loads(event['body'])
    
    if not 'email' in body:
        logger.error("No email field provided")
        return common.return_server_error('Email field is required')
    else:
        email = body['email']
    
    # set default category - everybody loves jokes
    category = 'joke'
    
    if 'category' in body:
        if body['category'] in categories:
            category = body['category']
        else:
            logger.error("Invalid category %s sent", category)
            return common.return_server_error('Category ' + category + ' is invalid. Must be one of ' + str(category))
    
    try:
        logger.debug("Setting dynamo db record to inactive for %s", email)
        disable_dynamo_subscription(email)
        
        logger.info("Deleting sns subscription for %s", email)
        delete_sns_subscription(email, category)
    except Exception as e:
        return common.return_server_error('Unable to delete subscription: ' + str(e))
    return {'statusCode': 200,
            'body': 'Successfully deleted subscription',
            'headers': {'Content-Type': 'application/json'}}
