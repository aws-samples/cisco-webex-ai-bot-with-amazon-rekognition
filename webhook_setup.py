#!/usr/bin/env python3
 
from webhook_lib import *

bot_webhook_id = get_webhook_id(webex_header,bot_webhook_name)
bot_webhook_targetUrl = get_api_endpoint(stack_name,region_name)

if bot_webhook_id is not None:
    print('Updating Webhook :', bot_webhook_name)
    status_code = update_webhook(webex_header,bot_webhook_id,bot_webhook_name,bot_webhook_targetUrl)
    if status_code in [200, 204]:
        print('Webhook updated with target URL: ', bot_webhook_targetUrl)
    else:
        print('Operation failed with status code: ', status_code)
else:
    print('Could not find webhook : ', bot_webhook_name)
    print('Creating Webhook :', bot_webhook_name)
    status_code = create_webhook(webex_header,bot_webhook_name,bot_webhook_targetUrl)
    if status_code in [200, 204]:
        print('Webhook created with target Url : ', bot_webhook_targetUrl)
    else:
        print('Operation failed with status code: ', status_code)

