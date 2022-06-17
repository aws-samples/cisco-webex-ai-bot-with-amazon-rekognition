stack_name = 'CiscoWebexAiBotWithAmazonRekognitionStack' # Do not modify
region_name='ap-southeast-1' # Change to reflect the region your AWS CLI is configured
bot_token = '' # Insert your Bot's token here
bot_email_id = 'xxx@webex.bot' # Replace with your bot's username
bot_webhook_name = 'webex-ai-chatbot-hook' # Change to your desired webhook name
webex_header =  {
                'Authorization': 'Bearer ' + bot_token,
                'Content-Type':'application/json; charset=utf-8',
                }