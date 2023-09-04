import os
import string
import random

import requests


class LinkedinSvc:
    CLIENT_ID = os.environ['LINKEDIN_CLIENT_ID']
    CLIENT_SECRET = os.environ['LINKEDIN_CLIENT_SECRET']
    REDIRECT_URI = os.environ['LINKEDIN_REDIRECT_URI']
    request_token_params = {'scope': 'openid,profile,email,w_member_social'}
    base_url = 'https://api.linkedin.com/v2/'
    request_token_url = None
    access_token = None
    access_token_method = 'POST'
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    authorize_url = 'https://www.linkedin.com/oauth/v2/authorization'

    @classmethod
    def auth_code(cls):
        try:
            csrf_token = cls.csrf_token()
            params = {
                'response_type': 'code',
                'client_id': cls.CLIENT_ID,
                'redirect_uri': cls.REDIRECT_URI,
                'state': csrf_token,
                'scope': 'openid,profile,email,w_member_social'
            }
            response = requests.get(cls.authorize_url, params=params)
            # response.url
            if response.url is not None:
                return response.url
            else:
                return None
        except Exception as e:
            raise e

    @classmethod
    def profile_api(cls, code):
        try:
            if code is not None:
                data = {
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': cls.REDIRECT_URI,
                    'client_id': cls.CLIENT_ID,
                    'client_secret': cls.CLIENT_SECRET
                }
                resp = requests.post(url=cls.access_token_url, data=data, timeout=20)
                return resp
            else:
                raise Exception
        except Exception as e:
            raise e

    @classmethod
    def csrf_token(cls):
        letters = string.ascii_lowercase
        token = ''.join(random.choice(letters) for i in range(20))
        return token
