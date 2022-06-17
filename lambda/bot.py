import json
import requests
import boto3
import os
import re
import time

from configs import bot_email_id, webex_header

def post_message_to_room(the_header,roomId,msg):
    message = {"roomId":roomId,"markdown":msg}
    uri = 'https://webexapis.com/v1/messages'
    resp = requests.post(uri, json=message, headers=the_header)

def detect_labels_local_file(photo):

    client=boto3.client('rekognition')
   
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
        
    labels = []

    for label in response['Labels']:
         labels.append(label['Name'] + ' : ' + '{:.2f}'.format(label['Confidence']) + '%')

    return labels

def detect_texts_local_file(photo):

    client=boto3.client('rekognition')
    ddb = boto3.resource('dynamodb')

    with open(photo, 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})

    texts = []

    for text in response['TextDetections']:
        if text['DetectedText'] not in texts:
            texts.append(text['DetectedText'] + ' : ' + '{:.2f}'.format(text['Confidence']) + '%')

    return texts

def detect_carplates_local_file(photo):

    client=boto3.client('rekognition')
    ddb = boto3.resource('dynamodb')

    # set environment variable
    TABLE_NAME = os.environ['TABLE_NAME']
    table = ddb.Table(TABLE_NAME)

    with open(photo, 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})

    car_plates_detected = []

    for text in response['TextDetections']:
        carplate_match = re.match("[A-Z]{2,3}\s*\d{3,4}\s*[A-Z]{1}",text['DetectedText'])
        if carplate_match:
            if text['DetectedText'] not in car_plates_detected:
                car_plates_detected.append(text['DetectedText'])
            response = table.put_item(
                Item={
                    'id': str(carplate_match[0]),
                    'createdAt': int(time.time())
                }
            )

    return car_plates_detected

def handler(event, context):

    if event['httpMethod'] == 'POST':
        # On receipt of a POST (webhook), load the JSON data from the request
        post_data = json.loads(event['body'])

        # Only process the request of the sender is not the bot itself
        if post_data['data']['personEmail'] != bot_email_id:

            # Check for files in the request
            if 'files' in post_data['data']:

                # Process all files in the request
                for item in post_data['data']['files']:
                    
                    response = requests.get(item, headers=webex_header)

                    print('Status code: ', response.status_code)

                    if response.status_code == 200:
                        imgHeaders = response.headers

                        if 'image' in imgHeaders['Content-Type']:
                            pic_name = imgHeaders['Content-Disposition'].replace("attachment; ", "").replace('filename', '').replace('=', '').replace('"', '')
                            local_file = '/tmp/{}'.format(pic_name)
                            
                            with open(local_file, 'wb') as f:
                                f.write(response.content)

                            # This section is for your business logic. We are demonstrating dection of labels, faces and texts in the image
                            # as well as car plate detection using regular expression from the detected texts. If a car plate is detected,
                            # we store it in an Amazon DynamoDB table. Feel free to change the regular expression in the detect_carplates_local_file 
                            # function to match your country's car plate format, or implement other business logic for your use case.

                            post_message_to_room(webex_header,post_data['data']['roomId'],'\n\n## Image analysis of ' + pic_name + '\n')
                            labels=detect_labels_local_file(local_file)
                            if len(labels) > 0:
                                post_message_to_room(webex_header,post_data['data']['roomId'],'**Labels:** \n* '+'\n* '.join(labels))
                                                       
                            texts=detect_texts_local_file(local_file)
                            if len(texts) > 0:
                                post_message_to_room(webex_header,post_data['data']['roomId'],'**Texts:** \n* '+'\n* '.join(texts))

                            car_plates= detect_carplates_local_file(local_file)
                            if len(car_plates) > 0:
                                post_message_to_room(webex_header,post_data['data']['roomId'],'**Car Plates:** \n* '+'\n* '.join(car_plates))
                                                        
                            os.remove(local_file)  

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello there! You have hit {} with method {}\n'.format(event['path'],event['httpMethod'])
    }

