from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_dynamodb as ddb,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class CiscoWebexAiBotWithAmazonRekognitionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "AI-Chatbot-Lambda-Policy", assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRekognitionReadOnlyAccess"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))        
        
        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'BotHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='bot.handler',
            role=role,
            timeout=Duration.seconds(30),
            memory_size=512
        )
        
        # Defines an Amazon API Gateway endpoint
        apigw_endpoint = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=my_lambda
        )

        # Create an Amazon DynamoDB table. Note that the removal policy is DESTROY. In a production
        # environment, you might want to consider setting it to RETAIN so that you don't lose data
        # after destroying the stack.
        image_details = ddb.Table(
            self, "ImageDetails",
            partition_key=ddb.Attribute(
                name="id",
                type=ddb.AttributeType.STRING
            ),
            sort_key = ddb.Attribute(
                name="createdAt",
                type=ddb.AttributeType.NUMBER
            ),
            encryption=ddb.TableEncryption.AWS_MANAGED,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Write the Amazon DynamoDB table name in the AWS lambda function's environment variable
        # and grant rights to the AWS Lambda function to write data to the table.
        # The environment variable will be used by the AWS lambda function later.
        my_lambda.add_environment("TABLE_NAME", image_details.table_name)
        image_details.grant_write_data(my_lambda)
           
        CfnOutput(scope=self,id="endpoint",value=apigw_endpoint.url)