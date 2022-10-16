import base64
from pydantic import ValidationError
from requests_oauthlib import OAuth2Session
from itsdangerous.url_safe import URLSafeSerializer
from itsdangerous import BadSignature, SignatureExpired
from . import Login, Token


class Auth:
    def __init__(
        self, osm_url, client_id, client_secret, secret_key, login_redirect_uri, scope
    ):
        self.osm_url = osm_url
        self.client_secret = client_secret
        self.secret_key = secret_key
        self.authorize_url = f"{osm_url}/oauth2/authorize/"
        self.oauth = OAuth2Session(
            client_id,
            redirect_uri=login_redirect_uri,
            scope=scope,
        )

    def login(
        self,
    ):

        login_url, _ = self.oauth.authorization_url(self.authorize_url)
        return Login(url=login_url)

    def callback(self, callback_url: str):
        token_url = f"{self.osm_url}/oauth2/token"
        self.oauth.fetch_token(
            token_url,
            authorization_response=callback_url,
            client_secret=self.client_secret,
        )
        user_api_url = f"{self.osm_url}/api/0.6/user/details.json"
        resp = self.oauth.get(user_api_url)
        if resp.status_code != 200:
            raise ValueError("Invalid response from OSM")
        data = resp.json().get("user")
        serializer = URLSafeSerializer(self.secret_key)
        user_data = {
            "id": data.get("id"),
            "username": data.get("display_name"),
            "img_url": data.get("img").get("href") if data.get("img") else None,
        }
        token = serializer.dumps(user_data)
        access_token = base64.b64encode(bytes(token, "utf-8")).decode("utf-8")
        token = Token(access_token=access_token)
        return token

    def deserialize_access_token(self, access_token: str):
        deserializer = URLSafeSerializer(self.secret_key)

        try:
            decoded_token = base64.b64decode(access_token)
        except Exception:
            raise ValueError("Could not decode token")

        try:
            user_data = deserializer.loads(decoded_token)
        except (SignatureExpired, BadSignature):
            raise ValidationError("Invalid token")

        return user_data
