# import the json utility package since we will be working with a JSON object
import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
# import two packages to help us with dates and date formatting
from time import gmtime, strftime
# import the universally unique id module
import uuid
# email error handling 
from botocore.exceptions import ClientError


# set up resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CESContacts')
client = boto3.client('ses',region_name=AWS_REGION)
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
SENDER = "Cullen <cullen@cloudengineeringsolutions.com>"
RECEIVER = "Cullen <cullen@cloudengineeringsolutions.com>"
CONFIGURATION_SET = "ConfigSet"
AWS_REGION = "us-east-1"
CHARSET = "UTF-8"

# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
# extract values from the event object we got from the Lambda service and store in a variable
    id = str(uuid.uuid4())
    name = event['Name'] 
    email = event['email']
    message = event['Message']
# write name and time to the DynamoDB table using the object we instantiated and save response in a variable
    response = table.put_item(
        Item={
            'ID': id,
            'Name': name,
            'email': email,
            'Message': message,
            'SubmissionDate':now
            })

    # try sending email
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECEIVER,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': message,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': email,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': name,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
# return a properly formatted JSON object
    return {
        'statusCode': 200,
        'body': json.dumps('Hello, ' + name + ' you will receive an email at ' + email + ' in less than 24 hours. Thank you')
    }

