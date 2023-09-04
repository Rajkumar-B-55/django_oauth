import os

import google.auth.transport.requests
import requests
from google.oauth2 import id_token
from django.http import HttpResponse, request


class GoogleSvc:
    CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
    GOOGLE_REDIRECT_URI = os.environ['GOOGLE_REDIRECT_URI']

    @classmethod
    def login(cls):
        authorization_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={cls.CLIENT_ID}"
            f"&redirect_uri={cls.GOOGLE_REDIRECT_URI}"
            "&response_type=code"
            "&scope=email profile openid"
        )
        return authorization_url

    @classmethod
    def callback(cls, code):
        try:
            token_url = "https://oauth2.googleapis.com/token"
            token_payload = {
                "code": code,
                "client_id": cls.CLIENT_ID,
                "client_secret": cls.CLIENT_SECRET,
                "redirect_uri": cls.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }

            response = requests.post(token_url, data=token_payload)
            token_data = response.json()

            id_info = id_token.verify_oauth2_token(
                id_token=token_data["id_token"],
                request=google.auth.transport.requests.Request(),
                audience=cls.CLIENT_ID,
                clock_skew_in_seconds=10
            )
            return id_info
        except Exception as e:
            raise e

    @classmethod
    def login_is_required(cls, function):
        def wrapper(request, *args, **kwargs):
            if "google_id" not in request.session:
                return HttpResponse("Unauthorized", status=401)
            else:
                return function(request, *args, **kwargs)

        return wrapper
