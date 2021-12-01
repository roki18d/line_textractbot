# /usr/bin/env python3
# coding: utf-8

from io import BytesIO
import sys, os
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
SECRETS_MANAGER_SECRET_ARN = os.getenv("SECRETS_MANAGER_SECRET_ARN", None)
LOGGING_CONFIG_FILE_LOCATION = './logging.conf'
logging.config.fileConfig(LOGGING_CONFIG_FILE_LOCATION)

def get_secret():
    logging.debug(f'Function "{sys._getframe().f_code.co_name}" was called.')
    try:
        secretsmanager_client = boto3.client(service_name='secretsmanager', region_name='ap-northeast-1')
        response = secretsmanager_client.get_secret_value(SecretId=SECRETS_MANAGER_SECRET_ARN)
    except ClientError as e:
        logging.error(e.message)
        raise e
    else:
        if "SecretString" in response:
            return json.loads(response.get('SecretString'))
        else:
            return json.loads(base64.b64decode(response.get("SecretBinary")))

# Handler
def lambda_handler(event, context): 
    logging.debug(f'Event: {event}')

    secret = get_secret()
    logging.debug({
        "LINE_CHANNEL_ACCESS_TOKEN": secret.get("LINE_CHANNEL_ACCESS_TOKEN"), 
        "LINE_CHANNEL_SECRET": secret.get("LINE_CHANNEL_SECRET")
    })

    line_bot_api = LineBotApi(secret.get("LINE_CHANNEL_ACCESS_TOKEN"))
    handler = WebhookHandler(secret.get("LINE_CHANNEL_SECRET"))
    logging.debug({"line_bot_api": line_bot_api, "webhook_handler": handler})

    body = event["body"]
    signature = event["headers"]["x-line-signature"]
    logging.debug({"body": body, "signature": signature})

    def generate_response(status_code=None, body=None): 
        logging.debug(f'Function "{sys._getframe().f_code.co_name}" was called.')
        response = {"isBase64Encoded": False, "statusCode": status_code, "headers": {}, "body": body}
        logging.debug(f'Generated response: {response}')
        return response

    def textract(image=None):
        logging.debug(f'Function "{sys._getframe().f_code.co_name}" was called.')
        textract_client = boto3.client('textract', region_name='us-east-1')
        response_textract_client = textract_client.detect_document_text(Document={'Bytes': image})

        texts = list()
        for block in response_textract_client.get('Blocks'): 
            if block.get("BlockType") == "LINE": 
                logging.info(block.get("Text"))
                texts.append(block.get("Text"))
        return NEWLINE_CODE.join(texts)

    @handler.add(MessageEvent, message=ImageMessage)
    def handle_image_message(line_event):
        logging.debug(f'Function "{sys._getframe().f_code.co_name}" was called.')
        message_id = line_event.message.id
        message_content = line_bot_api.get_message_content(message_id)
        message = textract(image=BytesIO(message_content.content).read())
        line_bot_api.reply_message(line_event.reply_token, TextMessage(text=message))

    try:
        handler.handle(body=body, signature=signature)
        return generate_response(status_code=200, body='')

    except LineBotApiError as e:
        logging.error(f'Got exception from LINE Messaging API: {e.message}')
        for m in e.error.details:
            logging.error("%s: %s" % (m.property, m.message))
        return generate_response(status_code=403, body=e.message)

    except InvalidSignatureError as e: 
        logging.error(f'Invalid Signature Error: {e.message}')
        return generate_response(status_code=403, body=e.message)
