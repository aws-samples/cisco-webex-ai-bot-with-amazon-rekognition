#!/usr/bin/env python3

from webhook_lib import *

bot_webhook_id = get_webhook_id(webex_header,bot_webhook_name)

if bot_webhook_id is not None:
    print('Deleting Webhook ', bot_webhook_name)    
    status_code = delete_webhook(webex_header,bot_webhook_id)

    if status_code in [200, 204]:
        print('Webhook {} deleted successfully'.format(bot_webhook_name))
    else:
        print('Operation failed with status code: ', status_code)
else:
    print('Could not find webhook : ', bot_webhook_name)
