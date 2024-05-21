.. _account:

==================================
Accessing account details
==================================

A ``wetrade`` **Account** object can be used to access information on a given 
E-Trade brokerage account. By default, your account_key is set to that of the
first brokerage account tied to your E-Trade user account, but this can be
changed by setting account_key either during or after creating an **Account** 
object

**Examples for manually setting account_key**

.. code-block:: python
    
  # automatically set to first account_key
  my_account = Account(client=my_api_client)
  # set account_key manually
  my_account = Account(client=my_api_client, account_key='my-account-key')
  # set to second account_key
  my_account = Account(client=my_api_client)
  my_account.account_key = my_account.list_accounts()[1]['accountIdKey']

.. autoclass:: wetrade.account.Account
  :members:
  :undoc-members: