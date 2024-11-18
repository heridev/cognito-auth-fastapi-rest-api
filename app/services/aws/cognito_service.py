from typing import Optional, Dict, Any
import boto3
import jwt
from jwt.algorithms import RSAAlgorithm
import requests
from functools import lru_cache
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import Settings


class CognitoService:
    def __init__(self, settings: Settings):
        self.region = settings.AWS_REGION
        self.user_pool_id = settings.COGNITO_USER_POOL_ID
        self.client_id = settings.COGNITO_CLIENT_ID
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

    def _get_public_key(self, kid: str) -> Optional[str]:
        """Get the public key from JWKS matching the key ID"""
        jwks = self._get_jwks()
        key_data = next((key for key in jwks['keys'] if key['kid'] == kid), None)
        if key_data:
            return RSAAlgorithm.from_jwk(key_data)
        return None

    async def validate_token(self, credentials: HTTPAuthorizationCredentials) -> Dict[str, Any]:
        """Validate the JWT token and return the claims"""
        try:
            token = credentials.credentials
            # Decode without verification first to get the key ID
            header = jwt.get_unverified_header(token)
            kid = header['kid']

            # Get the public key
            public_key = self._get_public_key(kid)
            if not public_key:
                raise HTTPException(status_code=401, detail="Invalid token signature")

            # Verify and decode the token
            claims = jwt.decode(
                token,
                key=public_key,
                algorithms=['RS256'],
                audience=self.client_id,
                issuer=f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}'
            )
            return claims

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
