from ....services.dynamodb import DynamoDBService
from fastapi import APIRouter, HTTPException
from ....models.contact import ContactForm
import logging

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"]
)

logger = logging.getLogger(__name__)

dynamo_service = DynamoDBService()


@router.post("")
async def create_contact(contact: ContactForm):
    try:
        await dynamo_service.save_contact_form(contact)
        return {"message": "Contact form submitted successfully"}
    except Exception as e:
        logger.error(f"Error saving contact form: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
