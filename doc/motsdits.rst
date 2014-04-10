Mots-dits
=========

http://api.motsditsquebec.com/api/v2/motsdits/

The motsdits endpoint is one of the two most central features of the API, and provides much of the core interaction that the application relies on


Listing Mots-dits
-----------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/

Mots-dits have the following attributes:

+================+===============================================================+=================================================+
|   Attribute    |                          Description                          |                      Notes                      |
+================+===============================================================+=================================================+
| **action**     | The action of this motdit                                     |                                                 |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **what**       | The compact item_ object representing the descriptive action  | will have at least one of **what** or **where** |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **where**      | The compact item_ objet representing the location             | will have at least one of **what** or **where** |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **likes**      | The number of times this motdit has been liked                |                                                 |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **user_likes** | A bool representing whether the acting user likes this motdit |                                                 |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **favourites** | The number of times this motdit has been favourited           |                                                 |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **tags**       | A list of tag names for this motdit                           |                                                 |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **created_by** | A compact user_ object                                        |                                                 |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **score**      | The overall static score_ that this motdit has received       |                                                 |
+----------------+---------------------------------------------------------------+-------------------------------------------------+

Motsdits are loaded in a paginated list, and requests can be filtered using GET parameters

+--------------+--------------------------------------------------------------------------------------------------+
| **order_by** | Sets the sorting of the motsdits, accepts: **created**, **updated**, **likes** or **favourites** |
+--------------+--------------------------------------------------------------------------------------------------+
| **page**     | Sets the page number, defaults to 1                                                              |
+--------------+--------------------------------------------------------------------------------------------------+
| **per_page** | Sets the number per page, max of 50                                                              |
+--------------+--------------------------------------------------------------------------------------------------+


Creating Mots-dits
------------------

**POST** http://api.motsditsquebec.com/api/v2/motsdits/

Each mot-dit has 4 basic attributes:

+============+==============================================================================================+===========+
| Attribute  |                                         Description                                          |           |
+============+==============================================================================================+===========+
| **what**   | The object/action being referenced (eg. A burger, skiing)                                    | required* |
+------------+----------------------------------------------------------------------------------------------+-----------+
| **where**  | Where the object is (eg. Burger Royal, Le Plateau)                                           | required* |
+------------+----------------------------------------------------------------------------------------------+-----------+
| **action** | One of the core available actions (aller, sortir, visiter, faire, manger, magasiner, dormir) | required  |
+------------+----------------------------------------------------------------------------------------------+-----------+
| **tags**   | Free-form meta-tags about the motdit (eg. Awesome, Great night out)                          |           |
+------------+----------------------------------------------------------------------------------------------+-----------+
| **story**  | A longform text story to share with the motdit                                               |           |
+------------+----------------------------------------------------------------------------------------------+-----------+
| **photo**  | A photo file to attach to the motdit when creating                                           |           |
+------------+----------------------------------------------------------------------------------------------+-----------+

* only one of **what** or **where** is required to create a mots-dit

A simple example of creating a mot-dit would be:

.. code-block:: javascript

    {
        'what': 'an example motsdit',
        'where': 'api documentation',
        'action': 'create',
        'tags': ['created', 'new', 'motdit']
    }

**note**: tags can be supplied as either a list (when POSTing in JSON) or a comma-separated string (when using multipart/form-data)

Retrieving Mots-dits
--------------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/:ID/

Retrieves a mot-dit by ID, with the fields above_


Liking and Favouriting Mots-dits
--------------------------------

**POST** http://api.motsditsquebec.com/api/v2/motsdits/:ID/like/

This will create a new like for the mot-dit. A user can only like a mot-dit once, but the request will always succeed

**DELETE** http://api.motsditsquebec.com/api/v2/motsdits/:ID/like/

This will delete a like for the mot-dit. Will ensure there is no like, the request will always succeed (even if the user didn't previously like the object).

The API for favouriting is the exact same, so:

**POST** http://api.motsditsquebec.com/api/v2/motsdits/:ID/favourite/

**DELETE** http://api.motsditsquebec.com/api/v2/motsdits/:ID/favourite/


Mot-dit Photos
--------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/:ID/photos/

This endpoint provides a **paginated** list of compact photo_ objects that are related to this specific Mot-dit, See the photo_ documentation for a full list of query parameters available


Mot-dit Stories
--------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/:ID/stories/

This endpoint provides a **paginated** list of story_ objects that are related to this specific Mot-dit. See the story_ documentation for a full list of query parameters available



.. _item: items.html
.. _photo: photos.html
.. _story: stories.html
.. _above: #Listing Mots-Dits
