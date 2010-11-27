from setuptools import setup

__author__ = 'ssteinerX@gmail.com'

setup(name='loggingserver',
      version='0.1',
      zip_safe=False,
      packages=[
         "loggingserver",
      ],
      package_data = {
         # If any package contains *.txt or *.rst files, include them:
         '': ['*.conf', '*.rst'],
         'twisted_plugin': ['twisted'],
      },
      author=__author__,
      author_email="ssteinerX@gmail.com",
      url="http://https://github.com/ssteinerx/ssx-twisted-loggingserver",
)
