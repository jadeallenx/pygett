from distutils.core import setup

setup(author='Mark Allen',
      author_email='mrallen1@yahoo.com',
      description='Gett API bindings'
      long_description='A client for the REST API provided by the Ge.tt filesharing service.'
      fullname='pygett',
      name='pygett',
      url='https://github.com/mrallen1/pygett',
      download_url='https://github.com/mrallen1/pygett',
      version='0.1',
      license='MIT',
      platforms=['Linux','Windows']
      packages=['pygett'],
      requires=['simplejson', 'requests']
)
