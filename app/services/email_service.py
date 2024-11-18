from postmarker.core import PostmarkClient
from typing import Dict, Any
from ..config import settings


class EmailService:
    def __init__(self):
        self.client = PostmarkClient(server_token=settings.postmark_server_token)
