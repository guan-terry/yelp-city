from distutils.core import setup
setup(
  name = 'YelpCity',
  packages = ['YelpCity'],
  version = '0.1',
  license='MIT',
  description = 'Obtaining search queries of more than 1000 limited by the Yelp Fusion API',
  author = 'Terry',
  author_email = 'terryguan1@gmail.com',
  url = 'https://github.com/guan-terry/yelp-city',
  download_url = 'https://github.com/guan-terry/yelp-city/archive/v_01.tar.gz',
  keywords = ['Yelp', 'YelpFusion', 'searches', 'queries'],
  install_requires=[
          'pyzipcode',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)
