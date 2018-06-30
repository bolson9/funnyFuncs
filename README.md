# Welcome to funnyFuncs!

Funny functions is a serverless application that lets users subscribe for daily updates
from categorites they are interested interested

## Supported categories

* Quotes
* Jokes
* Facts about Chuck Norris

## Endpoints

*/subscribe*

This endpoint takes a json object of the format

`{"email": "bo67192@gmail.com", "category": "joke"}`

And creates a dynamodb record for the user and subscribes them to the correct topic arn

*/unsubscribe*

This endpoint takes a json object of the format

`{"email": "bo67192@gmail.com"}`

It marks the dynamodb record for that subscription as inactive, and deletes the corresponding sns topic subscription

## AWS Resources

### Lambda Functions

*Unsubscribe*

Services the `/unsubscribe` endpoint

*Subscribe*

Services the `/subscribe` endpoint

*Publish*

Handles once a day publishing for the application.

This function depends on 3 external endpoints

* https://icanhazdadjoke.com/
* http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en
* https://api.chucknorris.io/jokes/random

And publishes to the SNS topics

### SNS Topics

* Joke topic - used to publish to joke subscribers
* Quote topic - used to publish to quote subscribers
* Fact topic - used to publish to fact subscribers

### API Gateway

Passes inbound requests to the Lambda functions

### DynamoDB Table

The table Name tag is `"${EnvironmentParameter}FunnyFuncSubs"`

This table tracks the subscriptions, endpoints, category they are subscribed to, and whether or not they are active

Item format

{"email": "email@email.com", "Active": True, "category": "joke", "Hour": 8}