Javascript Example
==================

This is a pure-javascript example. It's worth noting that the API key generation stage should NOT be done in pure frontend javascript in a production setting. The proper approach is:

1. Receive request from user to log-in
2. Pass credentials to a backend service that queries the API (server side)
3. Store the access key in the session cookie
4. Access only the session key via Javascript

For the purposes of example, this API provides all of the functionality on the frontend

The following is a simple example of an API wrapper library for the MDQ API, it provides the same methods
and functionality as the Python example

.. code-block:: javascript

    /**
     * API Library (requires jQuery)
     */
    function MDQApi(client_id, client_secret) {

      // Client ID and secret supplied by the application
      this.client_id = client_id;
      this.client_secret = client_secret;

      // The access token to be used
      this.access_token = null;

      // Actual request wrapper
      this.request = function(method, path, data, callback, content_type){

        if(!content_type){
          content_type = 'application/json';
          data = JSON.stringify(data);
          processData = false;
        }else{
          processData = true;
        }

        var headers = {'content-type': content_type};

        // Once the access token is set, add it to requests
        if(this.access_token) headers['Authorization'] = 'Bearer ' + this.access_token;

        return $.ajax({
            url: 'http://api.motsditsquebec.com/' + path,
            data: data,
            success: callback,
            type: method,
            headers: headers,
            processData: processData
        })
      };

      // Wrap the normal HTTP methods
      this.get = function(path, callback, ctype){ return this.request('GET', path, null, callback, ctype); };
      this.post = function(path, data, callback, ctype){ return this.request('POST', path, data, callback, ctype); };
      this.put = function(path, data, callback, ctype){ return this.request('PUT', path, data, callback, ctype); };
      this.delete = function(path, data, callback, ctype){ return this.request('DELETE', path, data, callback, ctype); };

      // And handle the oauth2 authorization implicitly
      // WARNING: This is for demonstration purposes, and should NOT be used client-side
      this.authorize = function(email, password, post_authorize){

        var self = this;
        this.post('/oauth2/access_token', {
            'client_id': this.client_id,
            'client_secret': this.client_secret,
            'grant_type': 'password',
            'username': email,
            'password': password
        }, function(response){
          self.access_token = response.access_token;
          if(post_authorize) post_authorize();
        }, 'application/x-www-form-urlencoded');
      };

    };

The following is a sample flow that performs authorization and then interacts directly with the API
All output will be printed directly to the console

.. code-block:: javascript

    var api = new MDQApi('291f1dda02ea49f16baa', 'c0635020316d5a697f5935cf5d44c769fd454b76');

    var test_email = 'test@motsditsquebec.com';
    var test_password = 'test';

    api.authorize(test_email, test_password, function(){
        // Create a new motdit
        var new_motdit = {
            'what': 'test an api',
            'where': 'montreal',
            'action': 'test',
            'tags': ['created', 'new', 'awesome']
        };

        // Simple response handler
        var log_response = function(r){ console.log(r); };

        // Create a mot-dit
        api.post('/api/v2/motsdits/', new_motdit, log_response);

        // Like a mot-dit
        api.post('/api/v2/motsdits/1/like/', {}, log_response);

        // List all mots-dits
        api.get('/api/v2/motsdits/', function(response){
            for(var i in response.motsdits){
                console.log(response.motsdits[i]);
            }
        });
    });
