from distutils.core import setup
setup(
  name = 'acl2_bridge',
  packages = ['acl2_bridge'],
  version = '0.1',
  license='bsd-3-clause',
  description = 'Connect to an ACL2 Server from Python',
  author = 'Ruben Gamboa',
  author_email = 'ruben@uwyo.edu',
  url = 'https://github.com/rubengamboa/acl2_bridge',
  download_url = 'https://github.com/rubengamboa/acl2_bridge/archive/v0_1.zip',
  keywords = ['ACL2', 'theorem proving', 'verification'],
  install_requires = [],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Education',
    'Topic :: Education',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3.8',
  ],
)
