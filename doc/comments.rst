Comments
========

http://api.motsditsquebec.com/api/v2/comments/

Comments are messages users have created in relation to _news objects, allowing for a discussion about actions happening within the application


Listing Comments
----------------

**GET** http://api.motsditsquebec.com/api/v2/comments/

News items have the following attributes:

+----------------+--------------------------------------------------------+-----------------------------+
|    **text**    |                  Text of the comment                   |                             |
+----------------+--------------------------------------------------------+-----------------------------+
| **news_item**  | The news_ object this comment is related to            |                             |
+----------------+--------------------------------------------------------+-----------------------------+
| **created_by** | A condensed user_ object                               |                             |
+----------------+--------------------------------------------------------+-----------------------------+
| **score**      | The overall static score_ that this story has received |                             |
+----------------+--------------------------------------------------------+-----------------------------+

And support the following filters:

+--------------+-----------------------------------------------------------+
| **order_by** | Accepts: **created**, **updated**, **score** or **likes** |
+--------------+-----------------------------------------------------------+
| **page**     | Sets the page number, defaults to 1                       |
+--------------+-----------------------------------------------------------+
| **per_page** | Sets the number per page, max of 50                       |
+--------------+-----------------------------------------------------------+

Creating Comments
-----------------

**POST** http://api.motsditsquebec.com/api/v2/comments/

To create a comment, you just need to POST the **text** of the comment and the **id** of the news_ item to the comments endpoint. All other fields are auto-generated

.. code-block:: javascript

    {
        'text': 'text of your comment',
        'news_item': 1,
    }

.. _item: items.html
.. _motsdits: motsdits.html
.. _score: scores.html
.. _photo: photos.html
.. _user: users.html
.. _news: news.html
