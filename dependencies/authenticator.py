import base64
from fastapi import Request, HTTPException
from .constants import *


class Authenticator:
    """Handles validation of request."""

    @staticmethod
    def validate(request : Request):
        headers = request.headers
        auth_token = headers.get('Authorization') or headers.get('authorization')
        if not auth_token:
            print('Authentication Token not found.')
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

        auth_token = auth_token.replace("Basic ", "")
        client_id, client_secret = base64.b64decode(auth_token).decode('ascii').split(":")

        if client_id != valid_username or client_secret != valid_password:
            print('No client found for the supplied Authentication Token.')
            raise HTTPException(status_code=403, detail="Invalid credentials")
        else:
            print("Authentication Done!")

        print(f'Authenticated client: [{client_id}]')

        return client_id

authenticator = Authenticator()