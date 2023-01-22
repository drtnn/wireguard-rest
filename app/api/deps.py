from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from app.settings.main import settings


class BearerTokenAuthentication(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        authorization_credentials = await super(BearerTokenAuthentication, self).__call__(request=request)
        if authorization_credentials.credentials == settings.AUTH_TOKEN:
            return authorization_credentials
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )


authentication_scheme = BearerTokenAuthentication()
