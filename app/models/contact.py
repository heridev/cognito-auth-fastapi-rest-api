from pydantic import BaseModel, EmailStr
from datetime import datetime


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str
    created_at: datetime = datetime.now()


class ContactFormData:
    def __init__(self, contact: ContactForm, toEmailList: list[str]):
        self.contact = contact
        self.toEmailList = toEmailList
