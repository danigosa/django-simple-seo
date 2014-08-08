=============================
Simple Seo Backend for Django
=============================

Simple seo backend for Django. Inspired by django-seo ( https://github.com/willhardy/django-seo ) but found it quite
complex for the simple functionality it was intended for.

django-simple-seo aims to attach a model to your views with just 4 simple lines of code and everything configured by the admin.

What's in django-simple-seo
***************************

 * Python 2.7, 3.2, 3.3, 3.4 and Django 1.4, 1.5 and 1.6
 * View Autodiscovering
 * Pure Django Models and Django Fields implementation, no metaclasses in action
 * Don't reinvent the wheel: as long as they are django models you can use the goodies out there
 * i18n with django-vinaigrette, django-linguo, django-modeltranslation, etc.
 * Cache can be activated internally, but can also be used with johnny-cache, django-cache-machine, etc.
 * Easily extendible as far as it's all about simple django models and fields
 * Support for UrlFields and ImageFields in admin
 * Test app included (.testapp)

 .. image:: assets/simple_seo_admin.png

What's NOT in django-simple-seo
*******************************

 * Only implements view based backend. Maybe in future releases it will include Model and Path backend like in DjangoSeo. The attribute 'populate_from' is neither implemented yet.

Installation
------------

You can use pip like this:

.. code-block:: sh

    $ pip install django-simple-seo

You can use pip with git master code instead of pypi version:

.. code-block:: sh

    $ pip install git+https://github.com/danigosa/django-simple-seo.git

Add to your settings:

.. code-block:: python

    INSTALLED_APPS = (
    ...
    'simple_seo',
    ...
    )

Requeriments
------------

 * staticfiles
 * south (optional, if migrations)
 * admin (this includes auth, sessions and contenttypes)
 

1. Create your SEO Model
------------------------

Create a model subclassing the classes BaseMetada(title, author, description, keywords), OpenGraphMetada(includes facebook tags) or AllMetadata(Facebook and Twitter). You must use **register** to register the model.

.. code-block:: python

    from simple_seo.models import AllMetadata
    from simple_seo import register


    class MyMetadata(AllMetadata):
        """
        My Seo Model
        """

    # Register SEO Model
    register(MyMetadata)


2. Synchronize your DB
----------------------

Synchronize your database with **syncdb** or **migrate** depending on your case:

.. code-block:: sh

    $ ./manage.py syncdb

3. Register your model for administration
-----------------------------------------

Add this lines to your admin.py:

.. code-block:: python

    from simple_seo.admin import BaseMetadataAdmin
    from django.contrib import admin
    from .models import MyMetadata


    class MyMetadataAdmin(BaseMetadataAdmin):
        pass

    admin.site.register(MyMetadata, MyMetadataAdmin)


4. Add metadata for your views
------------------------------

Your views are autodiscovered for your convenience, create a metadata object for every view you want to administer

 .. image:: assets/simple_seo_admin2.png
    :width: 100%


5. Add metadata to your template
--------------------------------

Just include this template tag in your **<head>** section:

.. code-block:: html

    {% load simple_seo %}
    <!DOCTYPE html>
    <html>
    <head lang="en">
        <meta charset="UTF-8">
        {% view_metadata %}
    </head>
    <body>
    TEST
    </body>
    </html>

6. Extend/Override default behaviour
------------------------------------

*"I prefer to have images as URLs, not static files in my server"*

Just override **og_image** attribute. You can find all base models in **simple_seo.models**, and all tag fields in **simple_seo.fields**:

.. code-block:: python

    from simple_seo.fields import URLMetaTagField, MetaTagField
    from simple_seo.models import AllMetadata
    from simple_seo import register


    class MyMetadata(AllMetadata):
        """
        My Seo Model
        """
        og_image = URLMetaTagField(name="og:image")  # Overrides default og:image field
        another_meta_tag = MetaTagField(name="myvariable", max_length="25")  #  Creates a new custom meta tag for the views

    # Register SEO Model
    register(MyMetadata)

7. App Settings
---------------

Some settings are provided to enable caching directly in the app:

.. code-block:: python

    SEO_CACHE_PREFIX = getattr(settings, 'SEO_CACHE_PREFIX', 'simple_seo:')
    SEO_CACHE_TIMEOUT = getattr(settings, 'SEO_CACHE_PREFIX', 60 * 60 * 24)
    SEO_USE_CACHE = getattr(settings, 'SEO_CACHE_PREFIX', False)


8. Sample App
-------------

You have a complete sample app in **testapp** module in this repository.


9. Contribute!
--------------

Then add to the root of the project your **local_settings.py** for everything your need, for instance adding debug toolbar local setting:

.. code-block:: python

    INTERNAL_IPS = ('10.0.2.2', )
    
To execute the project with **vagrant** and **virtualbox** you can add this Vagrantfile and receipes to the local project and execute **vagrant up**:

https://gist.github.com/danigosa/c2ac2d349c4fcf823cb7

After box is provisioned you'll have an Ubuntu 14.04 with a Python 3.4 virtualenv.

You can find more info of how to develop with remote vagrant servers and the awesome Pycharm IDE here: http://codeispoetry.me/index.php/remote-server-with-pycharm-and-vagrant/



Changelog
=========

**version 0.2.2**

 * Bufix errors in view  autodiscover in some cases

**Version 0.2.1**

 * Bugfixes
 * Support for South Migrations


**Version 0.2**

 * Added support for namespaced views
 * Added support for ImageField based Image Metatags (og:image, twitter:image)
 * Added support for UrlField based URL Metatags (og:url, twitter:url)
 * Added more base classes to ease setup
