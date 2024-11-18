from .email_service import EmailService
from typing import Any
from ..utils.logging_utils import with_logger
from ..models.contact import ContactForm, ContactFormData


@with_logger
class EmailContactService:
    def __init__(self):
        self.email_client = EmailService().client

    def send_user_confirmation_email(self, contact: ContactForm) -> Any:
        response = self.email_client.emails.send_with_template(
            TemplateAlias='user-thank-you-contact-message',
            From='email@cognitoauth.pro',
            To=contact.email,
            TrackOpens=True,
            TrackLinks='HtmlAndText',
            TemplateModel={
                "emailSubject": "Thank you for contacting us at Cognito Auth",
                "userContactName": contact.name,
            }
        )
        self.logger.info(f"Confirmation email sent to {contact.email}")
        return response

    def send_admin_email(self, contact_form_data: ContactFormData) -> Any:
        response = self.email_client.emails.send_with_template(
            TemplateAlias='admin-thank-you-contact-message',
            From='email@cognitoauth.pro',
            To=contact_form_data.toEmailList,
            TrackOpens=True,
            TrackLinks='HtmlAndText',
            TemplateModel={
                "emailSubject": "We received a new contact form submission from Cognito Auth",
                "contactEmail": contact_form_data.contact.email,
                "contactName": contact_form_data.contact.name,
                "contactMessage": contact_form_data.contact.message,
            }
        )
        self.logger.info(f"Confirmation email sent to admins {contact_form_data.contact.email}")
        return response

    def send_emails(self, contact_form_data: ContactFormData) -> Any:
        try:
            self.send_admin_email(contact_form_data)
            self.send_user_confirmation_email(contact_form_data.contact)
        except Exception as e:
            self.logger.error(f"Error sending emails: {str(e)}")
