from typing import Optional, Dict, Any
from jose import jwt, JWTError
import requests
from functools import lru_cache
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import Settings
from app.utils.logging_utils import with_logger


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        return credentials


@with_logger
class CognitoService:
    def __init__(self, settings: Settings):
        self.region = settings.aws_region
        self.user_pool_id = settings.cognito_user_pool_id
        self.client_id = settings.cognito_client_id
        self.logger.info("Initializing CognitoService")
        self._jwks = None
        security = HTTPBearer()
        self.security = Security(security)

    @lru_cache(maxsize=1)
    def _get_jwks(self) -> Dict:
        """Cache and return the JWKS from Cognito"""
        if not self._jwks:
            keys_url = f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json'
            response = requests.get(keys_url)
            self._jwks = response.json()
        return self._jwks

    def _get_public_key(self, kid: str) -> Optional[Dict]:
        """Get the public key from JWKS matching the key ID"""
        jwks = self._get_jwks()
        key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
        return key

    # async def validate_token(self, credentials: HTTPAuthorizationCredentials) -> Dict[str, Any]:
    async def validate_token(self, credentials: HTTPAuthorizationCredentials = Security(CustomHTTPBearer())) -> dict:
        """Validate the JWT token and return the claims"""
        try:
            self.logger.info("we are just getting started")
            self.logger.info(f"Validating token: {credentials.credentials}")
            token = credentials.credentials
            # Get the header without verification
            headers = jwt.get_unverified_headers(token)
            kid = headers['kid']

            # Get the public key
            public_key = self._get_public_key(kid)
            if not public_key:
                raise HTTPException(status_code=401, detail="Invalid token signature")

            # Verify the token
            claims = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience=self.client_id,
                issuer=f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}'
            )

            return claims

        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
