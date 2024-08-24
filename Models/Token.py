import jwt
import time
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
import jwt
import time
from jwt import ExpiredSignatureError, InvalidTokenError, DecodeError

class Token:
    # Roles for the restaurant rating API
    ROLE_REGULAR = "Regular"
    ROLE_ADMIN = "Admin"

    # Secret key for encoding and decoding the JWT
    KEY = "cdf97907258bb76aebaa7d435992f6b94f6f8886de4d725036e38cc17420625dc23fc2856519a1b51937ce89502cbb309b3501dd3908b4ff0966ff49c8747dfc"
    LENGTH_VALID = 3600  # 1 Hour

    def __init__(self):
        self.token = ""

    def build_token(self, email, role):
        token_id = jwt.utils.base64url_encode(jwt.utils.random_secret(16)).decode('utf-8')
        issued_at = int(time.time())
        not_before = issued_at
        expire = not_before + self.LENGTH_VALID
        server_name = "http://icarus.cs.weber.edu"

        data = {
            'iat': issued_at,
            'jti': token_id,
            'iss': server_name,
            'nbf': not_before,
            'exp': expire,
            'data': {
                'email': email,
                'role': role
            }
        }

        self.token = jwt.encode(data, self.KEY, algorithm='HS256')

        return self.token

    @staticmethod
    def extract_token_data(jwt_token):
        try:
            token_data = jwt.decode(jwt_token, Token.KEY, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidTokenError, DecodeError) as e:
            raise PermissionError("Invalid token.") from e

        return token_data

    @staticmethod
    def get_email_from_token(jwt_token=None):
        if jwt_token is None:
            jwt_token = Token.get_bearer_token_from_header()
        token_data = Token.extract_token_data(jwt_token)
        return token_data['data']['email']

    @staticmethod
    def get_role_from_token(jwt_token=None):
        if jwt_token is None:
            jwt_token = Token.get_bearer_token_from_header()
        token_data = Token.extract_token_data(jwt_token)
        return token_data['data']['role']

    @staticmethod
    def get_bearer_token_from_header():
        import os
        auth_header = os.environ.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith("Bearer "):
            raise PermissionError("No credentials provided.")

        jwt_token = auth_header.split("Bearer ")[-1]

        if not jwt_token:
            raise PermissionError("No credentials provided.")

        return jwt_token
