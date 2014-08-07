==============================
Simple Seo Backend for Django
==============================

Simple cache backend for Django. Inspired by django-seo ( https://github.com/willhardy/django-seo ) but found it quite
complex for the simple functionality it was intended for.

What's in django-simple-seo
------------------------------

 * Python 2.7, 3.2, 3.3, 3.4 and Django 1.4, 1.5 and 1.6
 * View Autodiscovering
 * Pure Django Models and Django Fields implementation, no metaclasses in action
 * Don't reinvent the wheel: as long as they are django models you can use the goodies out there
 * i18n with django-vinaigrette, django-linuo, django-modeltranslation, etc.
 * Cache can be activated internally, but can also be used with johnny-cache, django-cache-machine, etc.
 * Easily extendible as far as it's all about simple django models and fields
 * Support for UrlFields and ImageFields in admin
 * Test app included (.testapp)

 .. image:: assets/simple_seo_admin.png

What's NOT in django-simple-seo
----------------------------------------

 * Only implements view based backend. Maybe in future releases it will include Model and Path backend like in DjangoSeo.


Changelog
----------

**Version 0.2**

 * Added support for namespaced views
 * Added support for ImageField based Image Metatags (og:image, twitter:image)
 * Added support for UrlField based URL Metatags (og:url, twitter:url)
 * Added more base classes to ease setup
