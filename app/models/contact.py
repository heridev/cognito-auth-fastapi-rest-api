from pydantic import BaseModel, EmailStr
from datetime import datetime


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str
    created_at: datetime = datetime.now()
