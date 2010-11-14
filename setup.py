from setuptools import setup

__author__ = 'ssteinerX'

setup(name='loggingserver',
      version='0.1',
      zip_safe=False,
      packages=[
             "loggingserver",
             "twisted.plugins",
         ],
      author=__author__,
      author_email="ssteinerX@gmail.com",
      url="http://https://github.com/ssteinerx/python-loggingserver",
      )
