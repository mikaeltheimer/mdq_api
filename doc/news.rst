News
====

http://api.motsditsquebec.com/api/v2/news/

News items **will be** auto-generated whenever a user performs certain actions within the application (see actions_ below)


Listing News
------------

**GET** http://api.motsditsquebec.com/api/v2/news/

News items have the following attributes:

+----------------+--------------------------------------------------------+------------------------------+
|   **action**   |            The action this news represents             | See actions_ for description |
+----------------+--------------------------------------------------------+------------------------------+
| **motdit**     | The motdit_ object this news is related to             |                              |
+----------------+--------------------------------------------------------+------------------------------+
| **photo**      | The photo_ object this news is related to              | optional, context-dependent  |
+----------------+--------------------------------------------------------+------------------------------+
| **story**      | The story_ object this news is related to              | optional, context-dependent  |
+----------------+--------------------------------------------------------+------------------------------+
| **created_by** | A condensed user_ object                               |                              |
+----------------+--------------------------------------------------------+------------------------------+
| **score**      | The overall static score_ that this story has received |                              |
+----------------+--------------------------------------------------------+------------------------------+

And support the following filters:

+--------------+-----------------------------------------------------------+
| **order_by** | Accepts: **created**, **updated**, **score** or **likes** |
+--------------+-----------------------------------------------------------+
| **page**     | Sets the page number, defaults to 1                       |
+--------------+-----------------------------------------------------------+
| **per_page** | Sets the number per page, max of 50                       |
+--------------+-----------------------------------------------------------+

Actions
-------

News actions come in several different types, and each has a different set of properties

+--------------------+-----------------------+-------------------+
|       Action       |    Models Attached    |    Action value   |
+====================+=======================+===================+
| Created Mot-Dit    | **motdit**            | motdit-created    |
+--------------------+-----------------------+-------------------+
| Updated Mot-Dit    | **motdit**            | motdit-updated    |
+--------------------+-----------------------+-------------------+
| Liked Mot-Dit      | **motdit**            | motdit-liked      |
+--------------------+-----------------------+-------------------+
| Favourited Mot-Dit | **motdit**            | motdit-favourited |
+--------------------+-----------------------+-------------------+
| Liked Photo        | **motdit**, **photo** | photo-liked       |
+--------------------+-----------------------+-------------------+
| Liked Story        | **motdit**, **story** | story-liked       |
+--------------------+-----------------------+-------------------+

News Comments
--------------

**GET** http://api.motsditsquebec.com/api/v2/news/:ID/comments/

This endpoint provides a **paginated** list of compact comment_ objects that are related to this specific News item, See the comment_   documentation for a full list of query parameters available


.. _item: items.html
.. _motsdits: motsdits.html
.. _score: scores.html
.. _photo: photos.html
.. _user: users.html
.. _actions: #actions
