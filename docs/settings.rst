.. _settings:

==================================
Configuring ``wetrade`` settings
==================================

Check out the information below for details on configuring your ``wetrade`` 
settings. As detailed below, ``wetrade`` relies on a *settings.py* file in
the root directory of your project. 

++++++++++++++++++++++++++++++++++++++
Settings introduction
++++++++++++++++++++++++++++++++++++++

If you created your application using the *new-project* script detailed in 
:ref:`getting_started`, you'll see a *settings.py* file in your app directory. 
This file contains your account information and other important global 
``wetrade`` settings. Yours may look something like this: 

**settings.py**

.. code-block:: python

  # E-Trade settings
  login_method = 'auto' # 'auto', 'manual'
  use_2fa = False # needed to disable SMS auth - requires totp_secret
  config_id = 'sandbox'
  config_options = {
  'sandbox':{
    'base_url': 'https://apisb.etrade.com/',
    'client_key': 'SANDBOX_CLIENT_KEY',
    'client_secret': 'SANDBOX_CLIENT_SECRET',
    'username': 'USERNAME',
    'password': 'PASSWORD',
    'totp_secret': 'TOTP_SECRET'},
  'prod':{
    'base_url': 'https://api.etrade.com/',
    'client_key': 'PROD_CLIENT_KEY',
    'client_secret': 'PROD_CLIENT_SECRET',
    'username': 'USERNAME',
    'password': 'PASSWORD',
    'totp_secret': 'TOTP_SECRET'}}
  # Google Cloud settings (optional)
  # need GOOGLE_APPLICATION_CREDENTIALS env var set to json path
  enable_cloud_logging = False
  quote_bucket = 'your-quote-bucket'

  config = config_options[config_id]

Please note: the **config = config_options[config_id]** line is required to set
your configuration.

++++++++++++++++++++++++++++++++++++++
Definitions
++++++++++++++++++++++++++++++++++++++

---------------------------------
Required settings
---------------------------------


.. py:data:: login_method
  :type: str
  :value: 'auto'

Here you can set whether you want to login automatically (val='auto') with headless firefox,
or manually (val='manual') using a url that is supplied in your terminal which requires input
from the user. 

.. py:data:: use_2fa
  :type: bool
  :value: False

If you choose to login automatically, you have the option to authenticate with
an authenticator app. E-Trade forces users to use the much maligned Symantec 
VIP Access application which people smarter than I have argued degrades the 
security of the TOTP protocol. Luckily, we can get around this restriction and
bring our authenticator application by using  
`python-vipaccess <https://github.com/dlenski/python-vipaccess>`__
to generate a VIP Access ID as well as a secret we can include in our 
*settings.py* and load into our authenticator app of choice. 

.. py:data:: config_id
  :type: str
  :value: 'sandbox'

Here you can select between different config options listed in *config_options*
this is helpful for testing in the API sandbox or listing multiple accounts in 
the same *settings.py* file.

.. py:data:: config_options
  :type: dict

config_options is a dict containing the different options for configuring your 
application. The *new-project* template contains the pre-set keys 'sandbox' and 
'prod' for your default configurations. If you're using one account, you'd
generally want to set the came value for username, password, and totp_secret.

---------------------------------
Optional settings
---------------------------------


.. py:data:: enable_cloud_logging
  :type: bool
  :value: False

You can use this flag to enable Google Cloud Logging integration. This allows
you to access and store logs from Google's convenient web UI which makes it
easy to keep track of your trading activity especially when using multiple
accounts. 

.. py:data:: quote_bucket
  :type: str
  :value: 'your-quote-bucket'

If you're interested in storing data from a DataFrameQuote in the cloud, you 
can specify the name of a Google Cloud Storage bucket here to collect quote
data stored as a pkl of a pandas DataFrame. This is useful when reviewing
DataFrameQuote driven trading activity 

.. py:data:: headless_login
  :type: bool
  :value: True

If you're having a difficult time logging in using login_method='auto', you can
add headless_login=False in your *settings.py* to view the browser during login
and troubleshoot your issue. 