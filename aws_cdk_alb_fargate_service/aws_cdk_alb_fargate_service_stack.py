from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_logs,
)
from constructs import Construct


class AwsCdkAlbFargateServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_vpc = ec2.Vpc(
            self,
            "my_vpc",
            nat_gateways=1,
            cidr="172.31.0.0/16",
            max_azs=3,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    cidr_mask=20,
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name="application",
                    cidr_mask=20,
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                ),
                ec2.SubnetConfiguration(
                    name="data",
                    cidr_mask=20,
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                ),
            ],
        )

        cluster = ecs.Cluster(
            self,
            "service-cluster",
            cluster_name="service-cluster",
            container_insights=True,
            vpc=my_vpc,
        )

        image = ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")

        ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "amazon-ecs-sample",
            circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True),
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=image,
                container_port=80,
                log_driver=ecs.LogDriver.aws_logs(
                    stream_prefix="alb-fargate-service",
                    log_retention=aws_logs.RetentionDays.ONE_DAY,
                ),
            ),
        )
