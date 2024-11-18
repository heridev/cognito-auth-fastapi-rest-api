from .base_aws_manager_service import AWSServiceManager
from ...utils.logging_utils import with_logger


@with_logger
class SNSServiceManager(AWSServiceManager):
    def __init__(self):
        super().__init__('sns')

    async def publish_message(self, message: str, topic_arn: str):
        try:
            response = self.client.publish(
                TopicArn=topic_arn,
                Message=message
            )
            return response

        except Exception as e:
            self.logger.error(f"Failed to publish message to SNS: {str(e)}")
            raise Exception(f"Failed to publish message to SNS: {str(e)}")
