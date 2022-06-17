import aws_cdk as core
import aws_cdk.assertions as assertions

from cisco_webex_ai_bot_with_amazon_rekognition.cisco_webex_ai_bot_with_amazon_rekognition_stack import CiscoWebexAiBotWithAmazonRekognitionStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cisco_webex_ai_bot_with_amazon_rekognition/cisco_webex_ai_bot_with_amazon_rekognition_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CiscoWebexAiBotWithAmazonRekognitionStack(app, "cisco-webex-ai-bot-with-amazon-rekognition")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
