Dev_Blog2
====

Python Blog System. Powered by Tornado and MongoDB.

Features
--------

Dev_Blog2 is Python based CMS system, mainly for bloggers. It can help users to build their blog system easily and quickly.  Also it can be built easily with other web system:

* Light weight and high performance.

* Theme support.

* Plugin support.

* MondoDB database.

* Notification email. (Comment reply email & Crash error administrator email).

* Easy reading codes and fully in-code docs.

* And much more with continues development…

Get Started
-----------

To get started using Dev_Blog2, clone or fork the master branch or download the released packages. To live the edge, you can also use develop branch. BUT be careful with the crashes :.


Install independences:

    sudo apt-get install python-pip mongodb gcc openjdk-6-jre-headless lessc

    cd ~/dev_blog2/

    sudo pip install -r requirements.txt

Init website config:

    cp blog/config.py.sample  blog/config.py

    *** change the config with your own config***

    fab build

    *** It will generate a default admin account for you (username/password: admin) ***

Run Tests for blog functions:

    fab test

Start the website:

    fab start


Production config:

    Change the code in 'runserver.py' 
        "USED_CONF = 'config.DevelopmentConfig'"
    to
        "USED_CONF = 'config.ProductionConfig'"
    and enter more than 15 different random characters in 'config.py'
        "SECRET_KEY" = 'SomeWordsYouLike12345'


Much more detail about ***deploy*** in product environment please see ***Docs*** section — ***Build your site***



Browser Support and Testing
---------------------------

Dev_Blog2 is tested and works in:

* IE 7+
* Latest Stable: Firefox, Chrome, Safari
* iOS 6.x, 7.x
* Android 4.x
* window platform
* linux server platform

Much more detail about ***apperence*** please see ***Docs*** section — ***Custom your theme***

Docs and Website
----------------

[My own site](http://tuzii.me) is also open source with an custom theme, and also be include in the ***templates/theme*** folder.

Contributing
------------

See the  ***Docs*** section — ***Contributing*** for information on how to contribute to Dev_Blog2.


License
-------

This software is free to use under the BSD license.
See the [LICENSE file][] for license text and copyright information.

[LICENSE file]: https://github.com/ScenK/Dev_Blog2/blob/master/LICENSE

Dependencies
-------

Thanks to all other open-source projects(may not fully included).

[Flask](https://github.com/mitsuhiko/flask)

[Mongoengine](https://github.com/MongoEngine/mongoengine)


Changelog
-------

Thirdly release (Apr 8, 2015): Dev_blog2 (https://github.com/ScenK/Dev_Blog2/releases/tag/v0.2)
  
 + Flake 8 coding style
 + Folders tidy
 + Static files tidy
 + Theme support
 + Plugin support
 + README all english doc.
 + LICENSE change

Secondly release (Dec 7, 2013): Dev_Blog2 (https://github.com/ScenK/Dev_Blog2/releases/tag/1.0)

 + Flask foundation
 + MongoEngine ORM
 + New template and skin
 + Celery Email Queen
 + Fabric Auto Development
 + Powerful Admin
 + More friendly code and Tones of changes

Firstly release (Jul 19, 2013):  Dev_Blog

+ Pure Tornado and Pymongo Version (https://github.com/ScenK/Dev_Blog/releases) 

#### More installation detail see below:
  + MongoDB installation: http://docs.mongodb.org/manual/installation/
  + Lessc for windows: https://github.com/duncansmart/less.js-windows  
