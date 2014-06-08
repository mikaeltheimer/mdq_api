Mots-dits
=========

http://api.motsditsquebec.com/api/v2/motsdits/

The motsdits endpoint is one of the two most central features of the API, and provides much of the core interaction that the application relies on


Listing Mots-dits
-----------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/

Mots-dits have the following attributes:

+----------------+---------------------------------------------------------------+-------------------------------------------------+
|   Attribute    |                          Description                          |                      Notes                      |
+================+===============================================================+=================================================+
| **action**     | The action of this motdit                                     |                                                 |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **what**       | The compact item_ object representing the descriptive action  | will have at least one of **what** or **where** |
+----------------+---------------------------------------------------------------+-------------------------------------------------+
| **where**      | The compact item_ object representing the location            | will have at least one of **what** or **where** |
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
| **score**      | The overall static score_ that this motdit has received       | Equal to the number of favourites               |
+----------------+---------------------------------------------------------------+-------------------------------------------------+

Motsdits are loaded in a paginated list, and requests can be filtered using GET parameters

+--------------+---------------------------------------------------------------------------------------------------------------------+
|    Param     |                                                     Description                                                     |
+==============+=====================================================================================================================+
| **order_by** | Sets the sorting of the motsdits, accepts: **created**, **updated**, **score**, **likes** or **favourites**         |
+--------------+---------------------------------------------------------------------------------------------------------------------+
| **page**     | Sets the page number, (default: 1)                                                                                  |
+--------------+---------------------------------------------------------------------------------------------------------------------+
| **per_page** | Sets the number per page, max of 50                                                                                 |
+--------------+---------------------------------------------------------------------------------------------------------------------+
| **nearby**   | A lat,lng pair to search nearby  (eg. 41.0500,-122.300) - searches the lat/lng of the **what** and **where** fields |
+--------------+---------------------------------------------------------------------------------------------------------------------+
| **radius**   | **used only with nearby** Sets the radius to search (default: 100km)                                                |
+--------------+---------------------------------------------------------------------------------------------------------------------+
| **action**   | Action of the mots-dits to return, if specified must be the exact action name                                       |
+--------------+---------------------------------------------------------------------------------------------------------------------+

**Note**: You may only use **one** of **order_by** or **nearby**. If **order_by** is specified, **nearby** will be ignored.

Creating Mots-dits
------------------

**POST** http://api.motsditsquebec.com/api/v2/motsdits/

Each mot-dit has 4 basic attributes:

+-------------+----------------------------------------------------------------------------------------------+-----------+
|  Attribute  |                                         Description                                          |           |
+=============+==============================================================================================+===========+
| **what**    | The object/action being referenced (eg. A burger, skiing)                                    | required* |
+-------------+----------------------------------------------------------------------------------------------+-----------+
| **where**   | Where the object is (eg. Burger Royal, Le Plateau)                                           | required* |
+-------------+----------------------------------------------------------------------------------------------+-----------+
| **action**  | One of the core available actions (aller, sortir, visiter, faire, manger, magasiner, dormir) | required  |
+-------------+----------------------------------------------------------------------------------------------+-----------+
| **address** | The address of the **where** item                                                            |           |
+-------------+----------------------------------------------------------------------------------------------+-----------+
| **website** | The website of the **where** item                                                            |           |
+-------------+----------------------------------------------------------------------------------------------+-----------+
| **tags**    | Free-form meta-tags about the motdit (eg. Awesome, Great night out)                          |           |
+-------------+----------------------------------------------------------------------------------------------+-----------+
| **story**   | A longform text story to share with the motdit                                               |           |
+-------------+----------------------------------------------------------------------------------------------+-----------+
| **photo**   | A photo file to attach to the motdit when creating                                           |           |
+-------------+----------------------------------------------------------------------------------------------+-----------+

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

**note**: If you create **both** a story_ and a photo_ when creating a motdit, these two will be linked

Retrieving Mots-dits
--------------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/:ID/

Retrieves a mot-dit by ID, with the fields above_

Updating a Mots-dit
-------------------

**PATCH** http://api.motsditsquebec.com/api/v2/motsdits/:ID/

Sending a patch request allows you to partially update a mot-dit, supplying one of the following fields:

+-------------+----------------------------------------------------------------------------------------------+-----------+
|  Attribute  |                                         Description                                          |           |
+=============+==============================================================================================+===========+
| **address** | The address of the **where** item                                                            |           |
+-------------+----------------------------------------------------------------------------------------------+-----------+
| **website** | The website of the **where** item                                                            |           |
+-------------+----------------------------------------------------------------------------------------------+-----------+

.. code-block:: javascript

    {
        'address': '1234 fake street',
        'website': 'http://fakeplace.com'
    }


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
---------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/:ID/stories/

This endpoint provides a **paginated** list of story_ objects that are related to this specific Mot-dit. See the story_ documentation for a full list of query parameters available


Mot-dit News
------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/:ID/news/

This endpoint provides a **paginated** list of news_ objects that are related to this specific Mot-dit. See the news_ documentation for a full list of query parameters available


Searching for Mots-Dits
-----------------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/search/?q=SEARCH

The Mot-Dit search endpoint integrates searching via haystack_, using the elasticsearch_ backend. This queries directly the elasticsearch database at http://es.motsditsquebec.com/. Searches currently search for matches on the following fields:

+-------------+-----------------------------------+
|    Field    |            Description            |
+=============+===================================+
| **what**    | The full value of the what field  |
+-------------+-----------------------------------+
| **where**   | The full value of the where field |
+-------------+-----------------------------------+
| **action**  | The action verb                   |
+-------------+-----------------------------------+
| **address** | The address of the where field    |
+-------------+-----------------------------------+
| **website** | The website of the where field    |
+-------------+-----------------------------------+
| **tags**    | All the tags on this motdit       |
+-------------+-----------------------------------+

Search results are paginated, and each result looks like the following:

.. code-block:: javascript

    {
        "motdit": {
            "id": 8, 
            "created_by": {
                "id": 1, 
                "username": "admin"
            }, 
            "action": "eat", 
            "what": {
                "id": 3, 
                "name": "awesome lunch", 
                "score": 0.0
            }, 
            "where": {
                "id": 2, 
                "name": "test where", 
                "score": 0.0
            }, 
            "score": 0.0, 
            "likes": 0, 
            "favourites": 0, 
            "tags": [
                "vegan", 
                "daily", 
                "healthy"
            ], 
            "user_likes": false
        }, 
        "score": 0.16608897
    }

Where the motdit is a standard serialized motdit object, as above, and the score is the **search engine ranking score**, which is a relative value from 0 to 1 representing how good the match was (where 1 is a perfect match)

.. _item: items.html
.. _photo: photos.html
.. _story: stories.html
.. _above: #Listing Mots-Dits
.. _haystack: http://django-haystack.readthedocs.org/en/latest/
.. _elasticsearch: http://www.elasticsearch.org/
