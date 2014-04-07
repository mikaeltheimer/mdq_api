Items
=====

http://api.motsditsquebec.com/api/v2/items/

Items are the building blocks of mots-dits, and represent either the **what** or the **where** fields. They are name-unique, and cannot be created directly, instead they get created or referenced when creating a new mot-dit


Listing Items
-------------

**GET** http://api.motsditsquebec.com/api/v2/items/

Items have the following attributes:

+----------------+-------------------------------------------------------------------+
|    **name**    |     The object/action being referenced (eg. A burger, skiing)     |
+----------------+-------------------------------------------------------------------+
| **address**    | The address of the item (gets resolved to a lat/lng value)        |
+----------------+-------------------------------------------------------------------+
| **website**    | The website for accessing this item                               |
+----------------+-------------------------------------------------------------------+
| **tags**       | Free-form meta-tags about the item (eg. Awesome, Great night out) |
+----------------+-------------------------------------------------------------------+
| **created_by** | A condensed user_ object                                          |
+----------------+-------------------------------------------------------------------+
| **score**      | The overall static score_ that this item has received             |
+----------------+-------------------------------------------------------------------+

And support the following filters:

+--------------+--------------------------------------------------------------------------------------------------+
| **order_by** | Sets the sorting of the motsdits, accepts: **created**, **updated**, **likes** or **favourites** |
+--------------+--------------------------------------------------------------------------------------------------+
| **page**     | Sets the page number, defaults to 1                                                              |
+--------------+--------------------------------------------------------------------------------------------------+
| **per_page** | Sets the number per page, max of 50                                                              |
+--------------+--------------------------------------------------------------------------------------------------+

Item Autocomplete
-----------------

**GET** http://api.motsditsquebec.com/api/v2/items/autocomplete/encoded%20query/

Auto-completing items provides a simple interface for querying a list of item names, and returns a ranked list
of results, like:

.. code-block:: javascript

    // after GET http://api.motsditsquebec.com/api/v2/items/autocomplete/test/

    [
        "test",
        "test item",
        "item test"
    ]

Since autocomplete should be a lightweight action, this ensures it can be developed to be highly responsive

Updating Items
--------------

**PATCH** http://api.motsditsquebec.com/api/v2/items/:ID/

Items can be updated to set either their **address** or their **website**

.. code-block:: javascript

    // after GET http://api.motsditsquebec.com/api/v2/items/autocomplete/test/

    {
        "address": "1234 Fake Street",
        "website": "http://fake-restaurant.com"
    ]

Related Mots-dits
-------------

**GET** http://api.motsditsquebec.com/api/v2/items/:ID/related/

Retrieves a full list of motsdits_ objects in which this item appears

Photos (Under Development)
--------------------------

**GET** http://api.motsditsquebec.com/api/v2/items/:ID/photos/

Retrieves a list of photo_ objects related to this item. Since photos are connected to Mots-Dits and not to Items, these represent photos that are matched to any mot-dit this item is matched to.


.. _item: items.html
.. _motsdits: motsdits.html
.. _score: scores.html
.. _photo: photos.html
