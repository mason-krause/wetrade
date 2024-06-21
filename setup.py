import setuptools

with open('README.rst', 'r') as f:
  long_description = f.read()

setuptools.setup(
  name = 'wetrade',
  version = '1.0.1',
  author = 'Mason Krause',
  description = 'An E-Trade python library built for active stock trading',
  long_description = long_description,
  long_description_content_type='text/x-rst',
  url='https://github.com/mason-krause/wetrade',
  packages = setuptools.find_packages(),
  include_package_data = True,
  python_requires = '>=3.7',
  install_requires = [
    'authlib',
    'playwright',
    'urllib3==1.26.16',
    'xmltodict',
    'pytz',
    'pyotp==2.9.0',
    'google-cloud-logging', 
    'google-cloud-storage', 
    'google-cloud-secret-manager',
    'polars', 
    'pandas', 
    'pyarrow'],
    extras_require={
      'dev': [
        'pytest',
        'pytest-timeout',
        'sphinx',
        'sphinx_rtd_theme']},)