import setuptools


setuptools.setup(
  name = 'wetrade',
  version = '0.1.0',
  author='Mason Krause',
  description='An E-trade python library built for active stock trading',
  packages = setuptools.find_packages(),
  python_requires = '>=3.7',
  install_requires=[
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