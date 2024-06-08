``wetrade``: An E-Trade Python library built for automated stock trading 
=========================================================================

``wetrade`` overview
--------------------

``wetrade`` is an unofficial `E-Trade API <https://developer.etrade.com/home/>`__ 
library initially created for use in headless trading systems. It provides a lot 
of helpful built-in functionality, and was designed to be flexible and extensible
and to accommodate a wide variety of stock trading needs.

Features include:

* Automated login and authentication supporting 2FA
* Easy setup and configuration
* Quotes, account info, and custom ordering
* Callback functionality for order and quote updates 
* Convenient tools to check and localize trading hours 
* Easy deployment with Docker template
* Robust logging with optional Google Cloud integration

``wetrade`` documentation
-------------------------

For our full documentation, check out: 
`https://wetrade.readthedocs.io/en/latest/ <https://wetrade.readthedocs.io/en/latest/>`__.

Getting started with ``wetrade``
---------------------------------

In order to access the E-Trade API, you'll need to follow the 4 steps detailed on the
`E-Trade developer getting started page <https://developer.etrade.com/getting-started/>`__
then request an API key through `the linked page <https://us.etrade.com/etx/ris/apikey/>`__.
It's also recommended that you enable real-time data in the 
`the subscription center <https://us.etrade.com/etx/pxy/my-profile/subscription-center/>`__
so that you don't receive delayed quotes. 

Install ``wetrade``:

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

You'll now see a handful of files in your project directory including a `settings.py 
<https://wetrade.readthedocs.io/en/latest/settings.html>`__ file where you'll enter your 
user and API info and have the option to configure various ``wetrade`` settings. In this
file, you'll enter your username, password, client_key, and client_secret so ``wetrade`` 
can log into your account.

In addition to `settings.py <https://wetrade.readthedocs.io/en/latest/settings.html>`__
, we've also created a *Dockerfile* `for easy deployment 
<https://wetrade.readthedocs.io/en/latest/deployment.html>`__  as well as 
a *requirements.txt* and an example file *main.py* which demonstrates some basic wetrade 
usage:

**main.py**

.. code-block:: python

  from wetrade.api import APIClient
  from wetrade.account import Account
  from wetrade.quote import Quote
  from wetrade.order import LimitOrder
  from wetrade.utils import setup_cloud_logging


  def main():
    # Setup cloud logging (optional) and APIClient
    setup_cloud_logging()
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

Other info
-------------

``wetrade`` was initially designed to run headlessly and has built-in handling for 
most expected brokerage, server, and API errors. This and the majority of other 
``wetrade`` functionality is entirely optional to use, and our modular structure 
allows you to utilize as much or as little of the library as you'd like. Our goal 
is to consistently add new functionality to support additional use cases. If you 
have any comments or suggestions for new features, don't hesitate to create an 
issue or reach out to: `wetrade.inbox@gmail.com <mailto:wetrade.inbox@gmail.com>`__.


**Disclaimer:** *wetrade is an unofficial API library and comes with no warranty
of any kind. It is in no way endorsed by or affiliated with E\*TRADE Financial 
or any associated organization. Make sure to read and understand the terms of 
service of the underlying API before using this package. The authors accept 
no responsibility for any damage that might stem from use of this package. 
See the LICENSE file for more details.*