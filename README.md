# osm-login-python
Library to provide osm login oauth2.0 exchange to python projects 

Makes it very easier for the application to implement osm authentication login to their project with oauth2.0 

Auth can be initialized with your credentials like this : 
```
from osm_auth.app import Auth
osm_auth=Auth(osm_url=settings.OSM_URL, client_id=settings.OSM_CLIENT_ID,client_secret=settings.OSM_CLIENT_SECRET, secret_key=settings.OSM_SECRET_KEY, login_redirect_uri=settings.OSM_LOGIN_REDIRECT_URI, scope=settings.OSM_SCOPE)
```

Provides 3 Functions inside Auth class : 

1. login() -- Returns the login url for osm
2. callback() -- Returns the access token for the user
3. deserialize_access_token() -- returns the user data

Example on django : 

```
from django.conf import settings
from osm_auth.app import Auth
from django.http import JsonResponse
import json

# initialize osm_auth with our credentials
osm_auth=Auth(osm_url=settings.OSM_URL, client_id=settings.OSM_CLIENT_ID,client_secret=settings.OSM_CLIENT_SECRET, secret_key=settings.OSM_SECRET_KEY, login_redirect_uri=settings.OSM_LOGIN_REDIRECT_URI, scope=settings.OSM_SCOPE)

def login(request):
    login_url=osm_auth.login()
    return JsonResponse(json.loads(login_url))

def callback(request):
    # Generating token through osm_auth library method
    token=osm_auth.callback(request.build_absolute_uri())
    return JsonResponse(json.loads(token))

def get_my_data(request,access_token: str):
    user_data=osm_auth.deserialize_access_token(access_token)
    return JsonResponse(user_data)
 ```
