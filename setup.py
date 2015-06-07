import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-model-options',
    version='1.0',
    packages=['model_options'],
    include_package_data=True,
    license='GNU License',
    description='Django app for an extra model options.',
    long_description=README,
    url='https://github.com/jar3k/django-model-options',
    author='Jaroslaw Macko',
    author_email='jarek@forthewin.io',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    tests_require=['Django >= 1.8', 'mock'],
    test_suite="tests.runtests.runtests",
)
