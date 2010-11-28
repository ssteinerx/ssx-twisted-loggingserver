from setuptools import setup

__author__ = 'ssteinerX@gmail.com'

setup(name='loggingserver',
      version='0.1',
      zip_safe=False,
      packages=[
         "loggingserver",
         "twisted.plugins",
      ],
      package_data = {
         'twisted' : ['plugins/loggingplugin.py',],
      },
      author=__author__,
      author_email="ssteinerX@gmail.com",
      url="http://github.com/ssteinerx/ssx-twisted-loggingserver",
)
