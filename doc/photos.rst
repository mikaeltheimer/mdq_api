Photos
======

http://api.motsditsquebec.com/api/v2/photos/

Photos 


Listing Photos
--------------

**GET** http://api.motsditsquebec.com/api/v2/photos/

Photos have the following attributes:

+----------------+--------------------------------------------------------+-------------------------------+
|    **url**     |         A URL for retrieving the actual photo          |                               |
+----------------+--------------------------------------------------------+-------------------------------+
| **motdit**     | The motdit_ object this photo is related to            | when compact, just the **ID** |
+----------------+--------------------------------------------------------+-------------------------------+
| **created_by** | A condensed user_ object                               |                               |
+----------------+--------------------------------------------------------+-------------------------------+
| **user_likes** | Does the acting user like this photo?                  |                               |
+----------------+--------------------------------------------------------+-------------------------------+
| **score**      | The overall static score_ that this story has received |                               |
+----------------+--------------------------------------------------------+-------------------------------+
| **story**      | A story_ that was shared with this photo               | Optional                      |
+----------------+--------------------------------------------------------+-------------------------------+

And support the following filters:

+--------------+-----------------------------------------------------------+
| **order_by** | Accepts: **created**, **updated**, **score** or **likes** |
+--------------+-----------------------------------------------------------+
| **page**     | Sets the page number, defaults to 1                       |
+--------------+-----------------------------------------------------------+
| **per_page** | Sets the number per page, max of 50                       |
+--------------+-----------------------------------------------------------+

Creating Photos
---------------

**POST** http://api.motsditsquebec.com/api/v2/photos/

Photos can be created by sending a **Multipart/Form-data** POST request to the endpoint.

Your POST data should look like:

.. code-block:: javascript

    {
        "photo": <attached photo>,
        "motdit": 1
    }


Deleting Photos
---------------

**DELETE** http://api.motsditsquebec.com/api/v2/photos/:ID/

Users may delete any photos that belong to them. This endpoint will respond with HTTP 204 if successful, otherwise with a 403 (forbidden)


Liking Photos
-------------

**POST** http://api.motsditsquebec.com/api/v2/photos/:ID/like/

This will create a new like for the photo. A user can only like a photo once, but the request will always succeed

**DELETE** http://api.motsditsquebec.com/api/v2/photos/:ID/like/

This will delete a like on a photo. It will always succeed, even if the user doesn't yet like the photo 


.. _item: items.html
.. _motsdits: motsdits.html
.. _score: scores.html
.. _photo: photos.html
.. _story: stories.html
