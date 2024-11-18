from botocore.exceptions import ClientError
from ...models.contact import ContactForm
from .base_aws_manager_service import AWSServiceManager
from ...utils.logging_utils import with_logger


@with_logger
class DynamoDBService(AWSServiceManager):
    def __init__(self):
        super().__init__('dynamodb')

    async def save_contact_form(self, contact: ContactForm):
        try:
            item = {
                'email': contact.email,
                'name': contact.name,
                'message': contact.message,
                'created_at': contact.created_at.isoformat()
            }

            response = self.client.table.put_item(Item=item)
            return response

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            error_message = e.response.get('Error', {}).get('Message')
            self.logger.error(f"Failed to save contact form. Error code: {error_code}, Message: {error_message}")
            raise Exception(f"Failed to save contact form: {error_message}")
