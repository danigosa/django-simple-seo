import os

from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-simple-seo',
    version='0.4.1',
    packages=['simple_seo', 'simple_seo.templatetags'],
    include_package_data=True,
    license='MIT License',  # example license
    description='Simple SEO Module for Django',
    long_description=README,
    url='https://github.com/danigosa/django-simple-seo',
    author='danigosa',
    author_email='danigosa@gmail.com',
    install_requires=[

    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
