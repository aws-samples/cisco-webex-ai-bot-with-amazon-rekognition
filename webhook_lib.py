#!/usr/bin/env python3
 
import requests
import sys
import boto3
import json

sys.path.insert(0, './lambda')

from configs import stack_name, region_name, bot_webhook_name, webex_header

def get_api_endpoint(stack_name,region_name):
    '''
    This function retrieves all outputs of a stack from CloudFormation.
    '''     
    stack_outputs = {}
    cf_client = boto3.client('cloudformation',region_name=region_name)
    response = cf_client.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0]["Outputs"]
    for output in outputs:
        stack_outputs[output["OutputKey"]] = output["OutputValue"]
    
    return stack_outputs['endpoint']

def get_webhook_id(the_header,bot_webhook_name):
    '''
    This function retrieves webhook ID for a specific webhook name.
    '''        
    uri = 'https://webexapis.com/v1/webhooks/'
    resp = requests.get(uri, headers=the_header)
    result = None
    for item in resp.json()['items']:
        if item['name'] == bot_webhook_name:
            result = item['id']
            #print('Current TargetURL: ',item['targetUrl'])
    return result

def update_webhook(the_header,bot_webhook_id,bot_webhook_name,bot_webhook_targetUrl):
    '''
    This function updates the webhook with the target Url.
    '''        
    uri = 'https://webexapis.com/v1/webhooks/'+bot_webhook_id
    payload = {
        "targetUrl" : bot_webhook_targetUrl,
        "name" : bot_webhook_name
    }
    resp = requests.put(uri, data=json.dumps(payload), headers=the_header)
    return resp.status_code

def create_webhook(the_header,bot_webhook_name,bot_webhook_targetUrl):
    '''
    This function creates a webhook with the target Url.
    '''        
    uri = 'https://webexapis.com/v1/webhooks/'
    payload = {
        "targetUrl" : bot_webhook_targetUrl,
        "name" : bot_webhook_name,
        "resource" : "messages",
        "event" : "created"
    }
    resp = requests.post(uri, data=json.dumps(payload), headers=the_header)
    return resp.status_code    

def delete_webhook(the_header,bot_webhook_id):
    '''
    This function deletes a webhook.
    '''        
    uri = 'https://webexapis.com/v1/webhooks/'+bot_webhook_id
    resp = requests.delete(uri, headers=the_header)
    return resp.status_code  

