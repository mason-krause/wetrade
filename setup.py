import setuptools

with open('README.rst', 'r') as f:
  long_description = f.read()

setuptools.setup(
  name = 'wetrade',
  version = '0.1.1',
  author = 'Mason Krause',
  description = 'An E-Trade python library built for active stock trading',
  long_description = long_description,
  packages = setuptools.find_packages(),
  include_package_data = True,
  python_requires = '>=3.7',
  install_requires = [
    'authlib',
    'playwright',
    'urllib3==1.26.16',
    'xmltodict',
    'pyotp==2.9.0',
    'google-cloud-logging', 
    'google-cloud-storage', 
    'polars', 
    'pandas', 
    'pyarrow'])