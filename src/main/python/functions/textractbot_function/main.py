# /usr/bin/env python3
# coding: utf-8

from io import BytesIO
import os
import json
import base64

import logging
import logging.config

import boto3
from botocore.exceptions import ClientError

from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage)
from linebot.exceptions import (LineBotApiError, InvalidSignatureError)

NEWLINE_CODE = '\r\n'
SECRETS_MANAGER_SECRET_ARN = os.getenv('SECRETS_MANAGER_SECRET_ARN', None)
LOGGING_CONFIG_FILE_LOCATION = './logging.conf'
logging.config.fileConfig(LOGGING_CONFIG_FILE_LOCATION)

def get_secret():

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name='ap-northeast-1')

    try:
        get_secret_value_response = client.get_secret_value(SecretId=SECRETS_MANAGER_SECRET_ARN)

    except ClientError as e:
        exceptions = [
            'DecryptionFailureException', 
            'InternalServiceErrorException', 
            'InvalidParameterException', 
            'InvalidRequestException', 
            'ResourceNotFoundException']

        if e.response['Error']['Code'] in exceptions:
            raise e

    else:
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        else:
            return json.loads(base64.b64decode(get_secret_value_response['SecretBinary']))

# Handler
def lambda_handler(event, context): 

    secret = get_secret()
    logging.debug(secret.get('LINE_CHANNEL_ACCESS_TOKEN'))
    logging.debug(secret.get('LINE_CHANNEL_SECRET'))

    line_bot_api = LineBotApi(secret.get('LINE_CHANNEL_ACCESS_TOKEN'))
    webhook_handler = WebhookHandler(secret.get('LINE_CHANNEL_SECRET'))

    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    def textract(image=None):
        textract_client = boto3.client('textract', region_name='us-east-1')
        response_textract_client = textract_client.detect_document_text(Document={'Bytes': image})
        blocks = response_textract_client.get('Blocks')

        texts = list()
        for block in blocks: 
            if block.get('BlockType') == 'LINE': 
                logging.info(block['Text'])
                texts.append(block['Text'])
        
        message = NEWLINE_CODE.join(texts)
        return message
    
    def generate_response(status_code=None, body=None): 
        return {"isBase64Encoded": False, "statusCode": status_code, "headers": {}, "body": body}

    @webhook_handler.add(MessageEvent, message=ImageMessage)
    def handle_image_message(line_event):

        message_id = line_event.message.id
        message_content = line_bot_api.get_message_content(message_id)
        # image = BytesIO(message_content.content).read()
        message = textract(image=BytesIO(message_content.content).read())
        line_bot_api.reply_message(line_event.reply_token, TextMessage(text=message))
        return message

    try:
        message = webhook_handler.handle(body, signature)
        return generate_response(status_code=200, body=message)

    except LineBotApiError as e:
        logging.error(f'Got exception from LINE Messaging API: {e.message}')
        for m in e.error.details:
            logging.error("%s: %s" % (m.property, m.message))
        return generate_response(status_code=403, body=e.message)

    except InvalidSignatureError as e: 
        logging.error(f'Invalid Signature Error: {e.message}')
        return generate_response(status_code=403, body=e.message)
