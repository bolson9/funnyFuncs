# Common utility functions for the FunnyFunc app
import os
import logging

logger = logging.getLogger("common")

# This function takes a message and assembles a json object representing a server side error
def return_server_error(message):
    logger.debug("Returning a server error code message: %s", message)
    return {'statusCode': 500,
            'body': message,
            'headers': {'Content-Type': 'application/json'}}

# This function takes a category and pulls the topic ARN from environment variables   
def get_topic_arn(category):
    logger.info("Looking for %s category arn", category)
    if category == 'joke':
        sns_topic_arn = os.environ['JOKE_TOPIC']
    elif category == 'fact':
        sns_topic_arn = os.environ['FACT_TOPIC']
    elif category == 'quote':
        sns_topic_arn = os.environ['QUOTE_TOPIC']
    else:
        raise Exception("Unknown category")
    
    logger.debug("Found category %s arn: %s", category, sns_topic_arn)
    
    return sns_topic_arn