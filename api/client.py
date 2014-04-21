"""An API client for the motsdits api

@author Stephen Young (me@hownowstephen.com)
"""

import requests


class ApiClient:

    base_url = "http://api.motsditsquebec.com"

    def __init__(self):
        # Request an access token
        response = requests.post("{0}/oauth2/access_token/".format(self.base_url), data={
            'client_id': '5937f1cbf5e03bf33353',
            'client_secret': 'fd6139071a86c8ebb946f645dd18a22eec2bb23b',
            'grant_type': 'password',
            'username': 'me@hownowstephen.com',
            'password': 'goose'
        })

        self.headers = {
            'Authorization': 'Bearer ' + response.json()['access_token']
        }

    def request(self, method, url, *args, **kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}
        # @TODO: Fix this, it shouldn't override the explicit headers
        kwargs['headers'].update(self.headers)

        return method("{0}/{1}".format(self.base_url, url), *args, **kwargs)

    def __getattr__(self, key):
        func = getattr(requests, key)
        return lambda url, *a, **k: self.request(func, url, *a, **k)
