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
  enable_logging = False
  quote_bucket = 'your-quote-bucket'

  config = config_options[config_id]

Please note: the **config = config_options[config_id]** line is required to set
your configuration.

---------------------------------------------------
But I don't want to store my password in plain text
---------------------------------------------------

Fret not my friend, we've got you covered! We've thought of a few easy options 
to avoid storing passwords in plain text, and because *settings.py* is a python
file, you could potentially come up with many additional ways of accessing your
password.  

**Using Google Cloud Secret Manager**

We've integrated `Google Cloud Secret Manager 
<https://cloud.google.com/security/products/secret-manager/>`__ to provide a 
secure way to access passwords stored on this free service that's linked to 
your Google Account. 

After following the :ref:`instructions for setting up your Google Cloud account 
<gcloud>`, you can access Google Cloud secrets (eg: 'my-secret-id') in your 
*settings.py* file:

.. code-block:: python

  from wetrade.utils import get_gcloud_secret


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
    'password': get_gcloud_secret('your-secret-id'),
    'totp_secret': 'TOTP_SECRET'},
  'prod':{
    'base_url': 'https://api.etrade.com/',
    'client_key': 'PROD_CLIENT_KEY',
    'client_secret': 'PROD_CLIENT_SECRET',
    'username': 'USERNAME',
    'password': get_gcloud_secret('your-secret-id'),
    'totp_secret': 'TOTP_SECRET'}}
  # Google Cloud settings (optional)
  # need GOOGLE_APPLICATION_CREDENTIALS env var set to json path
  enable_logging = False
  quote_bucket = 'your-quote-bucket'

  config = config_options[config_id]

**Using environment variables**

For certain situations including cloud deployment, it may make sense to set your
passwords in environment variables. Please note: we DO NOT recommend saving 
passwords in your shell config (eg: .bashrc, .profile, .zshrc) or in your
venv/bin/activate file as this is no more secure than storing your passwords
directly in *settings.py* . If you have to use environment variables locally,
we'd recommended hiding your password env var from your shell history with a 
pattern and then setting environment variables in your individual terminal 
session as demonstrated below:

*Hiding a pattern from your shell history*

.. code-block:: shell

  # bash / linux
  export HISTIGNORE="*WETRADE_VAR*" 
  # zsh / mac
  export HISTORY_IGNORE="*WETRADE_VAR*" 

*Setting an environment variable*

.. code-block:: shell

  export WETRADE_VAR=my-password

You can then access this environment variable in your *settings.py* file:

.. code-block:: python

  import os 


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
    'password': os.environ['WETRADE_VAR'],
    'totp_secret': 'TOTP_SECRET'},
  'prod':{
    'base_url': 'https://api.etrade.com/',
    'client_key': 'PROD_CLIENT_KEY',
    'client_secret': 'PROD_CLIENT_SECRET',
    'username': 'USERNAME',
    'password': os.environ['WETRADE_VAR'],
    'totp_secret': 'TOTP_SECRET'}}
  # Google Cloud settings (optional)
  # need GOOGLE_APPLICATION_CREDENTIALS env var set to json path
  enable_logging = False
  quote_bucket = 'your-quote-bucket'

  config = config_options[config_id]

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


.. py:data:: enable_logging
  :type: bool
  :value: False

You can use this flag to enable logging using python's *logging* module
if you've set up :ref:`Google Cloud integration <gcloud>` and run 
*setup_cloud_logging()*, this allows you to store and access logs in Google's
convenient web UI which makes it easy to keep track of your trading activity 
especially when using multiple accounts. 

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