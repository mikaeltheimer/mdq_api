Javascript Example
==================

The following is a simple example of an API wrapper library for the MDQ API, it provides the same methods
and functionality as the Python example. Since it is client side, it depends on the access token being explicitly stored within a web cookie, see the oauth2_ example for how this is configured.

.. code-block:: javascript

    /**
     * API Library (requires jQuery)
     */
    function MDQApi(access_token) {

      // The access token to be used
      this.access_token = access_token;

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

    };

The following is a sample flow that performs authorization and then interacts directly with the API
All output will be printed directly to the console

.. code-block:: javascript
    
    // Load the access token from the cookies
    var access_token = $.cookie('access_token');

    var api = new MDQApi(access_token);

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


.. _oauth2: oauth2.html
