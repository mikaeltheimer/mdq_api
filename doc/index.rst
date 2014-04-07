.. MDQ Api documentation master file, created by
   sphinx-quickstart on Wed Apr  2 17:01:24 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mots-Dits Quebec API Documentation
==================================


.. cssclass:: table-striped
+-----------+------------+-----------+
|           |  General   |  Actions  |
+===========+============+===========+
| oauth2_   |            |           |
+-----------+------------+-----------+
| auth_     | register   | login     |
|           |            |           |
|           |            | logout    |
|           |            |           |
+-----------+------------+-----------+
| motsdits_ | photos     | like      |
|           |            |           |
|           | stories    | favourite |
|           |            |           |
|           |            | flag      |
+-----------+------------+-----------+
| items_    | related    |           |
|           |            |           |
|           | photos     |           |
+-----------+------------+-----------+
| photos_   |            | like      |
+-----------+------------+-----------+
| stories_  |            | like      |
+-----------+------------+-----------+
| news_     | comments   |           |
+-----------+------------+-----------+
| comments_ |            |           |
+-----------+------------+-----------+
| users_    | self       | follow    |
|           |            |           |
|           | news       |           |
|           |            |           |
|           | favourites |           |
|           |            |           |
|           | likes      |           |
|           |            |           |
|           | followers  |           |
|           |            |           |
|           | following  |           |
+-----------+------------+-----------+

.. toctree::
    :maxdepth 2

    items
    motsdits
    javascript


.. _auth: auth.html
.. _oauth2: oauth2.html
.. _motsdits: motsdits.html
.. _items: items.html
.. _photos: photos.html
.. _stories: stories.html
.. _news: news.html
.. _comments: comments.html
.. _users: users.html
