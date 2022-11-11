import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_alb_fargate_service.aws_cdk_alb_fargate_service_stack import AwsCdkAlbFargateServiceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cdk_alb_fargate_service/aws_cdk_alb_fargate_service_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCdkAlbFargateServiceStack(app, "aws-cdk-alb-fargate-service")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
