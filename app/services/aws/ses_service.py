from .base_aws_manager_service import AWSServiceManager
from ...utils.logging_utils import with_logger
from typing import Optional


@with_logger
class SESService(AWSServiceManager):
    DEFAULT_SENDER = 'email@cognitoauth.pro'

    def __init__(self):
        super().__init__('ses')

    async def send_email(self,
                         recipient: str,
                         subject: str,
                         body_html: Optional[str] = None,
                         body_text: Optional[str] = None,
                         sender: Optional[str] = DEFAULT_SENDER):

        self.logger.info(f"Sending email to {recipient} with subject: {subject}")

        try:

            message = {
                'Subject': {'Data': subject},
                'Body': {}
            }

            if body_html:
                message['Body']['Html'] = {'Data': body_html}
            if body_text:
                message['Body']['Text'] = {'Data': body_text}

            response = self.client.send_email(
                Source=sender,
                Destination={
                    'ToAddresses': [
                        recipient,
                    ]
                },
                Message=message
            )
            return response

        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            raise Exception(f"Failed to send email: {str(e)}")

    def get_send_quota(self):
        """Get SES sending quota"""
        return self.client.get_send_quota()
