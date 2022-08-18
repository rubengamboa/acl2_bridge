from distutils.core import setup
setup(
  name = 'acl2_bridge',
  packages = ['acl2_bridge'],
  version = '1.0',
  license='bsd-3-clause',
  description = 'Connect to an ACL2 Server from Python',
  long_description = """This package allows you to control an ACL2 process from Python, using the ACL2 Bridge. The ACL2 process must already be executing.""",
  long_description_content_type = "text/markdown",
  author = 'Ruben Gamboa',
  author_email = 'ruben@uwyo.edu',
  url = 'https://github.com/rubengamboa/acl2_bridge',
  download_url = 'https://github.com/rubengamboa/acl2_bridge/archive/v1.0.zip',
  keywords = ['ACL2', 'theorem proving', 'verification'],
  install_requires = [],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Topic :: Education',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3.8',
  ],
)
