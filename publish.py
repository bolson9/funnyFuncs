import logging
import boto3
import common
import requests

logger = logging.getLogger('subscribe')
logger.setLevel(logging.DEBUG)

categories = ['quote', 'fact', 'joke']

# Reaches out to a third party joke api and returns a toke text
def get_joke():
    # get joke
    joke_address = 'https://icanhazdadjoke.com/'
    logger.info("Getting joke from %s", joke_address)
    r = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "text/plain"})
    logger.debug("Joke request return code: %d", r.status_code)
    return r.text

# This function reaches out to a third party quote api and returns the result
def get_quote():
    quote_address = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
    logger.info("Getting quote from %s", quote_address)
    r = requests.get(quote_address)
    logger.debug("Quote response code %d", r.status_code)
    quote = r.json()
    return quote['quoteText'] + " - " + quote['quoteAuthor']

# Reaches out to a third party fact api and returns a fact text
def get_fact():
    fact_address = 'https://api.chucknorris.io/jokes/random'
    logger.info("Getting fact from %s", fact_address)
    r = requests.get(fact_address)
    logger.debug("Fact return code: %d", r.status_code)
    return r.json()['value']    

def publish(category, message):
    logger.info("Publishing a message to %s", category)
    logger.debug("%s message will be %s", category, message)
    topic_arn = common.get_topic_arn(category)
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message= "Here is your " + category + " for the day: " + message,
        Subject="Your daily " + category + "!"
    )

def handler(event, context):
    logger.info("Publishing to the joke topic")
    joke_text = get_joke()
    publish("joke", joke_text)
    
    logger.info("Publishing to quote topic")
    quote_text = get_quote()
    publish("quote", quote_text)
    
    logger.info("Publishing to fact topic")
    fact_text = get_fact()
    publish("fact", fact_text)
    return "done"