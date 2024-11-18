from ....utils.logging_utils import LoggerFactory
from ....models.contact import ContactForm, ContactFormData
from ....services.aws.dynamo_db_service import DynamoDBService
from ....services.aws.sns_service import SNSServiceManager
from ....services.aws.ses_service import SESService
from ....services.email_contact_service import EmailContactService
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"]
)


logger = LoggerFactory.get_logger(__name__)

dynamo_service = DynamoDBService()
sns_service = SNSServiceManager()
ses_service = SESService()
postmark_service = EmailContactService()


@router.post("")
async def create_contact(contact: ContactForm):
    logger.info(f"Received contact form submission from {contact.name} ({contact.email}): {contact.message}")
    try:
        contact_form_data: ContactFormData = ContactFormData(
            contact=contact,
            toEmailList=['joseheribertoperezmagana@gmail.com', 'joseheribertoperezmagana+secondadmin@gmail.com'])
        response = postmark_service.send_emails(contact_form_data)
        print("postmark email send response", response)
        return {"message": "Contact form submitted successfully"}
    except Exception as e:
        logger.error(f"Error sending emails for the contact form: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
