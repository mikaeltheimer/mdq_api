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
