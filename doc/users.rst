Users
=====

http://api.motsditsquebec.com/api/v2/users/

Users represent all accounts interacting with the API - they are what gets authenticated to generate a valid api_key and also allow for complex description of an individual's network


Listing Users
-------------

**GET** http://api.motsditsquebec.com/api/v2/users/

Users have the following attributes:

+----------------+--------------------------------------------------------+-------------------------------+
|  **username**  |                   A unique username                    |                               |
+----------------+--------------------------------------------------------+-------------------------------+

Creating Users (under development)
----------------------------------

**POST** http://api.motsditsquebec.com/api/v2/users/

Your POST data should look like:

.. code-block:: javascript

    {
        "username": "testuser",
        "email": "testuser@motsditsquebec.com",
        "password": "plaintext_password",
        "first_name": "Test",
        "last_name": "User"
    }

Logging in and out
------------------

Performing authentication for user accounts requires an oauth_ key - please review the oauth_ documentation for further information on logging in and out.


.. _item: items.html
.. _motsdits: motsdits.html
.. _score: scores.html
.. _photo: photos.html
.. _user: users.html
.. _oauth: oauth2.html
