Stories
=======

http://api.motsditsquebec.com/api/v2/stories/

Stories are descriptions of a user_'s relationship to a Mot-dit, by way of recommendation, anecdote etc.


Listing Stories
--------------

**GET** http://api.motsditsquebec.com/api/v2/stories/

Stories have the following attributes:

+----------------+--------------------------------------------------------+-------------------------------+
|    **text**    |                 The text of the story                  |                               |
+----------------+--------------------------------------------------------+-------------------------------+
| **motdit**     | The motdit_ object this photo is related to            | when compact, just the **ID** |
+----------------+--------------------------------------------------------+-------------------------------+
| **user_likes** | Does the acting user like this story?                  |                               |
+----------------+--------------------------------------------------------+-------------------------------+
| **created_by** | A condensed user_ object                               |                               |
+----------------+--------------------------------------------------------+-------------------------------+
| **score**      | The overall static score_ that this story has received |                               |
+----------------+--------------------------------------------------------+-------------------------------+

And support the following filters:

+--------------+-----------------------------------------------------------+
| **order_by** | Accepts: **created**, **updated**, **score** or **likes** |
+--------------+-----------------------------------------------------------+
| **page**     | Sets the page number, defaults to 1                       |
+--------------+-----------------------------------------------------------+
| **per_page** | Sets the number per page, max of 50                       |
+--------------+-----------------------------------------------------------+

Creating Stories
----------------

**POST** http://api.motsditsquebec.com/api/v2/stories/

Your POST data should look like:

.. code-block:: javascript

    {
        "photo": <attached photo>,
        "motdit": 1
    }


Deleting Stories
---------------

**DELETE** http://api.motsditsquebec.com/api/v2/stories/:ID/

Users may delete any stories that belong to them. This endpoint will respond with HTTP 204 if successful, otherwise with a 403 (forbidden)


Liking Stories
-------------

**POST** http://api.motsditsquebec.com/api/v2/stories/:ID/like/

This will create a new like for the story. A user can only like a story once, but the request will always succeed

**DELETE** http://api.motsditsquebec.com/api/v2/stories/:ID/like/

This will delete a like on a story. It will always succeed, even if the user doesn't yet like the story 


.. _item: items.html
.. _motsdits: motsdits.html
.. _score: scores.html
.. _photo: photos.html
.. _user: users.html
