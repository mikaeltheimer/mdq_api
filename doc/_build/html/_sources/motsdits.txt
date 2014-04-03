Mots-dits
=========

http://api.motsditsquebec.com/api/v2/motsdits/

The motsdits endpoint is one of the two most central features of the API, and provides much of the core interaction that the application relies on


Creating Mots-dits
------------------

**POST** http://api.motsditsquebec.com/api/v2/motsdits/

Each mot-dit has 4 basic attributes:

+------------+----------------------------------------------------------------------------------------------+
|  **what**  |                  The object/action being referenced (eg. A burger, skiing)                   |
+------------+----------------------------------------------------------------------------------------------+
| **where**  | Where the object is (eg. Burger Royal, Le Plateau)                                           |
+------------+----------------------------------------------------------------------------------------------+
| **action** | One of the core available actions (aller, sortir, visiter, faire, manger, magasiner, dormir) |
+------------+----------------------------------------------------------------------------------------------+
| **tags**   | Free-form meta-tags about the motdit (eg. Awesome, Great night out)                          |
+------------+----------------------------------------------------------------------------------------------+


These are the basic requirement for creating a new mots-dit, of which only **two** are required:

1. One of **what** or **where** (can also be both)
2. The **action**

All other attributes are non-mandatory. A sample mot-dit creation request may look like:

.. code-block:: javascript

    {
        'what': 'create an example motsdits',
        'where': 'api documentation',
        'action': 'visiter',
        'tags': ['created', 'new', 'motdit']
    }

Retrieving Mots-dits
--------------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/**{id}**/

Retrieves a mot-dit by ID, looks like:

.. code-block:: javascript

    {
        "id": 1, 
        "created_by": {
            "id": 1, 
            "username": "hownowstephen"
        }, 
        "action": "test", 
        "what": {
            "id": 1, 
            "name": "test an api", 
            "score": 0.0
        }, 
        "where": {
            "id": 2, 
            "name": "montreal", 
            "score": 0.0
        }, 
        "score": 0.0, 
        "likes": 2, 
        "favourites": 0, 
        "tags": [
            "created", 
            "new", 
            "awesome"
        ]
    }

One thing to note: **the mot-dit object is slightly different when retrieving** - both the "what" and the "where" fields are references to item_ objects, and so after being created, they are displayed with their name, score and id within the mot-dit


Retrieving Many Mots-dits (under development)
---------------------------------------------

**GET** http://api.motsditsquebec.com/api/v2/motsdits/

Motsdits are loaded in a paginated list, and requests can be filtered using GET parameters

+--------------+--------------------------------------------------------------------------------------------------+
| **order_by** | Sets the sorting of the motsdits, accepts: **created**, **updated**, **likes** or **favourites** |
+--------------+--------------------------------------------------------------------------------------------------+
| **page**     | Sets the page number, defaults to 1                                                              |
+--------------+--------------------------------------------------------------------------------------------------+
| **per_page** | Sets the number per page, max of 50                                                              |
+--------------+--------------------------------------------------------------------------------------------------+


.. _item: item.html
