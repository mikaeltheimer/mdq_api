import requests
import json

# Keys for the client being used to authenticate
CLIENT_ID = '291f1dda02ea49f16baa'
CLIENT_SECRET = 'c0635020316d5a697f5935cf5d44c769fd454b76'

# And an account to test with
EMAIL_ADDRESS = 'test@motsditsquebec.com'
PASSWORD = 'test'


class MDQApi:
    '''Thin wrapper around requests to keep from having to pass the base url every time'''

    base_url = 'http://api.motsditsquebec.com'

    def __getattr__(self, key):

        def wrapper(url, *args, **kwargs):
            '''Wraps the request with the full url'''
            handler = getattr(requests, key)
            full_url = self.base_url + '/' + url.lstrip('/')
            return handler(full_url, *args, **kwargs)
        return wrapper


api = MDQApi()

# Start by requesting an access token
response = api.post('/oauth2/access_token', data={
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'password',
    'username': EMAIL_ADDRESS,
    'password': PASSWORD
})

if response.status_code == 200:

    # The response is a json object containing our access token
    data = json.loads(response.content)
    access_token = data['access_token']

    # Now we're able to start making requests with the access token
    print "GOT ACCESS TOKEN", access_token

    # create a mot-dit
    response = api.post('/api/v2/motsdits/', json.dumps({
        'what': 'test an api',
        'where': 'montreal',
        'action': 'test',
        'tags': ['created', 'new', 'awesome']
    }), headers={'Authorization': 'Bearer ' + access_token, 'Content-type': 'application/json'})

    print response.status_code
    print response.content

    # like a motdit
    response = api.post('/api/v2/motsdits/1/like/', headers={'Authorization': 'Bearer ' + access_token})
    print response.status_code
    print response.content

    # list me some mots-dits
    response = api.get('/api/v2/motsdits/', headers={'Authorization': 'Bearer ' + access_token})
    data = json.loads(response.content)

    # iterate over the results
    for motdit in data['results']:
        print json.dumps(motdit, indent=2)


else:
    raise ValueError("Got status {}: {}".format(response.status_code, response.content))
