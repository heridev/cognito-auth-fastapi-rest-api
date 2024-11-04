import boto3
from botocore.exceptions import ClientError
from ..config import settings
from ..models.contact import ContactForm
import logging

logger = logging.getLogger(__name__)


class DynamoDBService:
    def __init__(self):
        try:
            self.session = boto3.Session(
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region
            )

            self.dynamodb = self.session.resource('dynamodb')
            self.table = self.dynamodb.Table(settings.dynamodb_table_name)

            # Verify table exists
            self.table.table_status
            logger.info(f"Successfully connected to DynamoDB table: {settings.dynamodb_table_name}")

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            error_message = e.response.get('Error', {}).get('Message')
            logger.error(
                f"Failed to initialize DynamoDB connection. Error code: {error_code}, Message: {error_message}")
            raise Exception(f"DynamoDB initialization failed: {error_message}")

    async def save_contact_form(self, contact: ContactForm):
        try:
            item = {
                'email': contact.email,
                'name': contact.name,
                'message': contact.message,
                'created_at': contact.created_at.isoformat()
            }

            response = self.table.put_item(Item=item)
            return response

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            error_message = e.response.get('Error', {}).get('Message')
            logger.error(f"Failed to save contact form. Error code: {error_code}, Message: {error_message}")
            raise Exception(f"Failed to save contact form: {error_message}")
