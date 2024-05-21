.. _getting_started:

===============
Getting Started
===============

Check out this page for tips on getting started with ``wetrade``!


++++++++++++++++++++++++++++++
Setting up E-Trade API Access
++++++++++++++++++++++++++++++

In order to access the E-Trade API, you'll need to follow the 4 steps detailed on the
`E-Trade developer getting started page <https://developer.etrade.com/getting-started/>`__
then request an API key through `the linked page <https://us.etrade.com/etx/ris/apikey/>`__.
It's also recommended that you enable real-time data in 
`the subscription center <https://us.etrade.com/etx/pxy/my-profile/subscription-center/>`__
so that you don't receive delayed quotes. 

+++++++++++++++++++++++++++++++++++++++++++++++++++++++
Installing ``wetrade`` and setting up your project
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

In this tutorial, we'll be setting up a new trading application using ``wetrade``


It's a good idea to create a new virtual environment for a new Python project

.. code-block:: shell

  # create venv
  python3 -m venv venv
  # enter venv
  source venv/bin/activate

We can then install ``wetrade`` into our venv. For automatic login, we'll also
need to install our browser.

.. code-block:: shell

  pip install wetrade
  playwright install firefox

Next, you'll get going in no time using our automated new project script!

.. code-block:: shell

  python -m wetrade new-project

You'll now see a handful of files in your project directory including a *settings.py*
file where you'll enter your user and API info and have the option to configure various
``wetrade`` settings. In this file, you'll enter your username, password, client_key, 
and client_secret so ``wetrade`` can log into your account.

In addition to *settings.py*, we've also created a *Dockerfile* for easy deployment as 
well as a *requirements.txt* and an example file *main.py* which demonstrates some basic 
wetrade usage:

**main.py**

.. code-block:: python

  from wetrade.api import APIClient
  from wetrade.account import Account
  from wetrade.quote import Quote
  from wetrade.order import LimitOrder
  from wetrade.utils import setup_logging


  def main():
    # Setup logging (optional) and APIClient
    setup_logging()
    client = APIClient()

    # Check out your account
    account = Account(client=client)
    print('My Account Key: ', account.account_key)
    print('My Balance: ', account.check_balance())

    # Get a stock quote
    quote = Quote(client=client, symbol='IBM')
    print(f'Last {quote.symbol} Quote Price: ', quote.get_last_price())

    # Place some orders and stuff
    order1 = LimitOrder(
        client = client,
        account_key = account.account_key,
        symbol = 'NVDA',
        action = 'BUY',
        quantity = 1,
        price = 50.00)
    order1.place_order()
    order1.run_when_status(
        'CANCELLED', 
        func = print, 
        func_args = ['Test message'])
    
    order2 = LimitOrder(
        client = client,
        account_key = account.account_key,
        symbol = 'NFLX',
        action = 'BUY',
        quantity = 1,
        price = 50.00)
    order2.place_order()
    order2.run_when_status(
        'CANCELLED',
        order1.cancel_order)
    
    order2.cancel_order()


  if __name__ == '__main__':
    main()

From here, you're ready to build your app. If you're having trouble getting
the above script to work, you can check out the documentation on
:ref:`how to configure your settings <settings>`.