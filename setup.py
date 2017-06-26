from setuptools import setup
setup(
  name = 'upstox',
  packages = ['upstox_api'],
  version = '0.7',
  description = 'Official Python library for Upstox APIs',
  author = 'Upstox Development Team',
  author_email = 'support@upstox.com',
  url = 'https://github.com/upstox/upstox-python',
  install_requires=['future', 'enum', 'websocket_client', 'pycurl'],
  keywords = ['upstox', 'python', 'sdk', 'trading', 'stock markets'],
  classifiers=[
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
)