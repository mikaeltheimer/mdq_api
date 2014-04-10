Authenticating with oAuth2
==========================

When working with the API, it is always a good idea to do the initial authentication on the server side, to ensure that the client secret key doesn't get exposed to the web. This can be done using cookies, as in the following flask_ example

First, set up some imports and variables

.. code-block:: python
    
    # Depends on flask and requests - to install run:
    # pip install flask requests

    from flask import Flask, request, make_response
    import requests

    # Create a flask app
    app = Flask(__name__)

    # This are your client credentials (keep the secret SECRET)
    CLIENT_ID = '291f1dda02ea49f16baa'
    CLIENT_SECRET = 'c0635020316d5a697f5935cf5d44c769fd454b76'


And then we'll be making several pieces of a single-page application. Firstly, we want to handle what happens when you just visit the page. In this example, if the user is logged in it will just show the auth token we're using, and otherwise it will show a login form

.. code-block:: python
    
    # If the token is in the cookies, display that
    if request.cookies.get('access_token'):
        return "You are logged in, your token is {}".format(request.cookies.get('access_token'))

    # Otherwise we display the login form
    else:
        return """<form action='.' method='POST'>
            Email: <input type="text" name="email"><br />
            Password: <input type="password" name="password"><br />
            <input type="submit" value="log-in">
        </form>"""

The second case we need to handle is when the form gets submitted - we should either respond with a success when it succeeds or a failure if the login did not. First of all, we need to send the login request to the API.

.. code-block:: python

    # This performs the actual request to the API for an access token using the submitted form data
    response = requests.post('http://api.motsditsquebec.com/oauth2/access_token', data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'password',
        'username': request.form['email'],
        'password': request.form['password']
    })

Then, if it succeeds, we will set a cookie containing the corresponding access token

.. code-block:: python

    resp = make_response("success")
    resp.set_cookie('access_token', response.json()['access_token'])
    return resp

Otherwise, we notify the client that something failed


.. code-block:: python

    return "login failed. check your login credentials"


All put together, here's the application.

.. code-block:: python

    from flask import Flask, request, make_response
    import requests

    app = Flask(__name__)

    CLIENT_ID = '291f1dda02ea49f16baa'
    CLIENT_SECRET = 'c0635020316d5a697f5935cf5d44c769fd454b76'


    @app.route('/', methods=['GET', 'POST'])
    def application():

        if request.method == 'GET':

            if request.cookies.get('access_token'):
                return "You are logged in, your token is {}".format(request.cookies.get('access_token'))
            else:
                return """<form action='.' method='POST'>
                    Email: <input type="text" name="email"><br />
                    Password: <input type="password" name="password"><br />
                    <input type="submit" value="log-in">
                </form>"""

        elif request.method == 'POST':

            # login, and print success message
            response = requests.post('http://api.motsditsquebec.com/oauth2/access_token', data={
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'grant_type': 'password',
                'username': request.form['email'],
                'password': request.form['password']
            })

            if response.status_code == 200:
                resp = make_response("success")
                resp.set_cookie('access_token', response.json()['access_token'])
                return resp
            else:
                return "login failed. check your login credentials"

    if __name__ == '__main__':
        app.run()


Save it as "authenticating.py" and run it with the following

.. code-block:: shell

    $ python authenticating.py

Then point your browser to http://localhost:5000


.. _flask: http://flask.pocoo.org
