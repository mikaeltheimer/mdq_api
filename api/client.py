"""An API client for the motsdits api

@author Stephen Young (me@hownowstephen.com)
"""

import requests


class ApiClient:

    def __init__(self, client_id, client_secret, base_url="http://api.motsditsquebec.com"):

        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = {}
        self.logged_in = False

    def login(self, username, password):
        '''Perform a login'''
        # Request an access token
        response = self.post("oauth2/access_token/", data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'password',
            'username': username,
            'password': password
        })

        self.headers = {
            'Authorization': 'Bearer ' + response.json()['access_token']
        }
        self.logged_in = True

        return response

    def request(self, method, url, *args, **kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}
        # @TODO: Fix this, it shouldn't override the explicit headers
        kwargs['headers'].update(self.headers)

        return method("{0}/{1}".format(self.base_url, url), *args, **kwargs)

    def __getattr__(self, key):
        func = getattr(requests, key)
        return lambda url, *a, **k: self.request(func, url, *a, **k)
