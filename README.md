# osm-login-python
Library to provide osm login oauth2.0 exchange to python projects 

Makes it very easier for the application to implement osm authentication login to their project with oauth2.0 

Example on django : 

```
from django.conf import settings
from osm_auth.app import Auth
from django.http import JsonResponse
import json

# initialize osm_auth with our credentials
osm_auth=Auth(osm_url=settings.OSM_URL, client_id=settings.OSM_CLIENT_ID,client_secret=settings.OSM_CLIENT_SECRET, secret_key=settings.OSM_SECRET_KEY, login_redirect_uri=settings.OSM_LOGIN_REDIRECT_URI, scope=settings.OSM_SCOPE)

def login(request):
    """Generates login url for OSM Login

    Args:
        request (get): _description_

    Returns:
        json: login_url
    """
    login_url=osm_auth.login()
    return JsonResponse(json.loads(login_url))

def callback(request):
    """Callback method redirected from osm callback method

    Args:
        request (_type_): contains code and state as parametr redirected from osm

    Returns:
        json: access_token
    """
    # Generating token through osm_auth library method
    token=osm_auth.callback(request.build_absolute_uri())
    return JsonResponse(json.loads(token))
 ```
