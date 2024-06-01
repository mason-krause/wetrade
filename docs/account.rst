.. _account:

==================================
Accessing account details
==================================

A ``wetrade`` :class:`Account <wetrade.account.Account>` object can be used 
to access information on a given E-Trade brokerage account. 

++++++++++++++++++++++++++++
Example usage
++++++++++++++++++++++++++++

-------------------------------------
Manually setting account_key
-------------------------------------

By default, your account_key is set to that of the first brokerage account tied
to your E-Trade user account, but this can be changed by setting account_key either 
during or after creating an :class:`Account <wetrade.account.Account>` object.

.. code-block:: python
    
  # automatically set to first account_key
  my_account = Account(client=my_api_client)
  # set account_key manually
  my_account = Account(client=my_api_client, account_key='my-account-key')
  # set to second account_key
  my_account = Account(client=my_api_client)
  my_account.account_key = my_account.list_accounts()[1]['accountIdKey']

-------------------------------------
Accessing Account information
-------------------------------------

After creating a new :class:`Account <wetrade.account.Account>`, you can check
your balance, view your portfolio, and list other brokerage accounts connected
to your E-Trade user account.

.. code-block:: python

  from wetrade.api import APIClient
  from wetrade.account import Account


  def main():
    my_api_client = APIClient()
    my_account = Account(client=my_api_client)
    # Get your balance
    balance = my_account.check_balance()
    print(f'My balance: {balance}')
    # Get your portfolio
    portfolio = my_account.view_portfolio()
    print(f'My portfolio: {portfolio}')
    # Get your list of brokerage accounts
    account_list = my_account.list_accounts()
    print(f'My accounts: {account_list}')


  if __name__ == '__main__':
    main()
    
++++++++++++++++
Detailed usage
++++++++++++++++

.. autoclass:: wetrade.account.Account
  :members:
  :undoc-members: