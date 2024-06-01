.. _gcloud:

==================================
Setting up Google Cloud features
==================================

We've integrated a few Google Cloud features into ``wetrade`` which are 
entirely optional to use. In general, we recommended :ref:`deploying with Docker
<deployment>`, and we don't advocate for any cloud provider in particular, but 
we are fans of `Google's Cloud Logging product <https://cloud.google.com/logging/>`__
which makes it to store, filter and review logs. This was our motivation for
including Google Cloud in the first place, and we've since added support for
`Google Cloud Storage <https://cloud.google.com/storage/>`__ for saving quote 
data and `Google Cloud Secret Manager 
<https://cloud.google.com/security/products/secret-manager/>`__ to provide a 
secure way to store and access passwords.

You can check out the instructions below for how to configure your Google Cloud
account and connect your ``wetrade`` application.

+++++++++++++++++++++++++++++++++++++++++++++++++++++
Creating a service account and generating a json key
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Since Google Cloud is tied to Google, there's a good chance that you don't have
to set up a new account and can just log in with your Gmail credentials. Once 
you have logged into the Google Cloud Console and created a project for your app, 
you'll need to `create a new service account 
<https://console.cloud.google.com/iam-admin/serviceaccounts/create>`__
and then generate your json key file by select this service account `from the
list <https://console.cloud.google.com/iam-admin/serviceaccounts>`__ and selecting
"KEYS" - "ADD KEY" - "Create new key". After selecting the "JSON" format, you'll
download the key file which you can save in your application root as *gcloud-creds.json*.

+++++++++++++++++++++++++++++++++++++++++++++++++++++
Assigning IAM roles to authorize access
+++++++++++++++++++++++++++++++++++++++++++++++++++++

After generating your key, we'll then assign the required roles to the associated
Principal that was created for your Service Account in the `Google Cloud IAM 
dashboard <https://console.cloud.google.com/iam-admin/iam>`__. 

For Logging, we'll need the "Logs Writer" role.

For Storage, we'll need the "Storage Object Admin" role.

For Secret Manager, we'll need the "Secret Manager Secret Accessor" role.

+++++++++++++++++++++++++++++++++++++++++++++++++++++
Locating your json key
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Google Cloud's python libraries use the **GOOGLE_APPLICATION_CREDENTIALS** 
environment variable to locate your json key file that may be saved as 
*gcloud-creds.json* in your application root. You'll need this set when running
your application, which you can do by running the follow command:

.. code-block:: shell

  export GOOGLE_APPLICATION_CREDENTIALS=gcloud-creds.json

This will set the environment variable for your individual shell session, and 
you'll need to rerun this command to set it again in a future session. As a 
shortcut, some python developers will add commands like this (eg: *"export 
GOOGLE_APPLICATION_CREDENTIALS=gcloud-creds.json"*) to the *venv/bin/activate*
file that is created when building your venv. When :ref:`deploying with
Docker <deployment>` we set *GOOGLE_APPLICATION_CREDENTIALS* in our Dockerfile.

+++++++++++++++++++++++++++++++++++++++++++++++++++++
Using Google Cloud features
+++++++++++++++++++++++++++++++++++++++++++++++++++++
-----------------------
Logging
-----------------------

In order to use Cloud Logging, you'll need to set **enable_logging = True** :ref:`in 
your *settings.py* file <settings>` and run **wetrade.utils.setup_cloud_logging()**
when initializing your application. Below we've included an example of a simple
*main.py* file where we're running **setup_cloud_logging()** before anything else.

**main.py**

.. code-block:: python

  from wetrade.api import APIClient
  from wetrade.account import Account
  from wetrade.utils import setup_cloud_logging


  def main():
    setup_cloud_logging()
    client = APIClient()

    account = Account(client=client)
    print('My Account Key: ', account.account_key)
    print('My Balance: ', account.check_balance())


  if __name__ == '__main__':
    main()

-----------------------
Cloud Storage
-----------------------

Cloud Storage currently only supports saving DataFrames from 
:class:`DataFrameQuotes <wetrade.quote.DataFrameQuote>` to the storage bucket of
your choice set with **quote_bucket = 'your-bucket-name'** :ref:`in your *settings.py*
file <settings>`.

After setting your *quote_bucket*, you can run 
:meth:`DataFrameQuote.upload_quote_data() <wetrade.quote.DataFrameQuote.upload_quote_data>`
to upload a .pkl file containing a pandas DataFrame of the quote data you've
collected to that bucket.

-----------------------
Secret Manager
-----------------------

You can access Google Cloud secrets which may include your E-Trade password or
other sensitive with the **wetrade.utils.get_gcloud_secret()** function. Below
is an example of using **get_gcloud_secret()** to access your passwords 
:ref:`from your *settings.py* file <settings>`. 

**settings.py**

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
  enable_logging = True
  quote_bucket = 'your-quote-bucket'

  config = config_options[config_id]