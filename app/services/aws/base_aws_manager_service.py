import boto3
from botocore.exceptions import UnknownServiceError
from typing import Optional
from ...config import settings
from ...utils.logging_utils import with_logger


@with_logger
class BaseAwsManager:
    """Base class for AWS service managers"""

    _session: Optional[boto3.Session] = None

    @classmethod
    def get_session(cls) -> boto3.Session:
        """Get or create AWS session singleton"""
        try:
            if cls._session is None:
                cls._session = boto3.Session(
                    aws_access_key_id=settings.aws_access_key_id,
                    aws_secret_access_key=settings.aws_secret_access_key,
                    region_name=settings.aws_region
                )
            return cls._session
        except Exception as e:
            cls.logger.error(f"Failed to initialize SNS connection: {str(e)}")
            raise Exception(f"SNS initialization failed: {str(e)}")


@with_logger
class AWSServiceManager:
    """Base class for specific AWS service managers"""

    # List of services that only support client interface
    CLIENT_ONLY_SERVICES = {'ses', 'pinpoint', 'cognito-identity', 'sts'}

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.session = BaseAwsManager.get_session()
        self.client = self.session.client(service_name)

        # Only try to create resource if service supports it
        self.resource = None
        if service_name not in self.CLIENT_ONLY_SERVICES:
            try:
                self.resource = self.session.resource(service_name)
            except UnknownServiceError:
                # Add to CLIENT_ONLY_SERVICES for future reference
                self.__class__.CLIENT_ONLY_SERVICES.add(service_name)
            except Exception as e:
                self.logger.error(f"Error creating resource for {service_name}: {str(e)}")
                raise
