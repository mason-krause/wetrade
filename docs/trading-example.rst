.. _trading_example:

==================================
``wetrade`` in action
==================================

Check out the example below for some inspiration on how you can use ``wetrade``
for live stock trading. This is provided for illustrative purposes only, and it
is not intended to be used with live trading nor is it a recommendation for a 
specific investment strategy. This is simply an illustration of something you 
could create using ``wetrade``.

We're going to be creating a new Class called TradingSession and running a new 
trading session from our entry point, *main.py*. This trading session will buy
a single share if the price rises 1% from open or sell a single share if the
price falls 1% and close any opened position one minute before market close.

++++++++++++++++++++++++++++
Example TradingSession
++++++++++++++++++++++++++++

Our application will consist of our TradingSession (contained in 
*trading_session.py*) and our entry point *main.py* :

**main.py**

.. code-block:: python

  from wetrade.utils import setup_cloud_logging
  from trading_session import TradingSession


  def main():
    setup_cloud_logging() # if you're using Google Cloud
    session = TradingSession('META')
    session.run()

  
  if __name__ == '__main__':
    main()

**trading_session.py**

.. literalinclude:: ../wetrade/project_template/trading_session.py
  :language: python

++++++++++++++++++++++++++++
Walkthrough
++++++++++++++++++++++++++++

----------
main.py
----------

This file is fairly straightforward. We have a single function *main()* which
optionally sets up :ref:`Google Cloud Logging <gcloud>`, then creates a new 
*TradingSession()* using the class defined in **trading_session.py** and the
symbol 'META', then runs our *TradingSession().run()* method.

--------------------------
trading_session.py
--------------------------

In this file, we're creating a new *TradingSession()* class incorporating different
parts of the ``wetrade`` library.

We start out by importing the time library and :ref:`APIClient <api_client>`,
:ref:`Account <account>`, :ref:`Quote <quote>`, :ref:`StopOrder, MarketOrder <order>`,
and :ref:`MarketHours <market_hours>`:

.. code-block:: python

  import time
  from wetrade.api import APIClient
  from wetrade.account import Account
  from wetrade.quote import Quote
  from wetrade.order import StopOrder, MarketOrder
  from wetrade.market_hours import MarketHours

We then define our class and initialize our *TradingSession* in the
__init__() method where we'll set up our :ref:`APIClient <api_client>`,
:ref:`Account <account>`, :ref:`Quote <quote>`, and :ref:`MarketHours <market_hours>`
which we'll reuse throughout the day.

**Initializing your TradingSession**

.. code-block:: python

  class TradingSession:
    def __init__(self, symbol):
      self.symbol = symbol
      self.client = APIClient()
      self.account = Account(self.client)
      self.quote = Quote(self.client, self.symbol)
      self.market_hours = MarketHours()
      self.buy_order = None
      self.sell_order = None
      self.exit_order = None
      self.position = 0

**Defining your run() method**

Next, you can define your *run()* method which is the primary function for your
trading activity.

.. code-block:: python

  class TradingSession:
  ...
    def run(self):
      self.market_hours.wait_for_market_open()
      opening_price = self.quote.get_open()
      self.buy_order = StopOrder(
        client = self.client,
        account_key = self.account.account_key,
        symbol = self.symbol,
        action = 'BUY',
        quantity = 1,
        price = round(1.01 * opening_price, 2))
      self.sell_order = StopOrder(
        client = self.client,
        account_key = self.account.account_key,
        symbol = self.symbol,
        action = 'SELL_SHORT',
        quantity = 1,
        price = round(99 * opening_price, 2))
      self.buy_order.place_order()
      self.sell_order.place_order()
      self.buy_order.run_when_status('EXECUTED', self.after_buy_order)
      self.sell_order.run_when_status('EXECUTED', self.after_sell_order)
      time.sleep(self.market_hours.seconds_till_close() - 60)
      self.close_position()
  ...

In this function, we first wait for the market to open and get the opening price
for our security. We then place 2 stops orders: one to buy at 1 percent above open,
and one to sell at 1 percent below open. We also set two callbacks: *after_buy_order()*,
and *after_sell_order()* (which we'll define below) to run after their associated orders
are executed. Finally, we wait until 60 seconds before markets close then close out our
position with *close_position()* .

This is a very simple example of a run() method, and for advanced strategies, 
your logic is likely to be much more complex. You may, for example, utilize
:meth:`Quote.monitor_in_background() <wetrade.quote.Quote.monitor_in_background>`
and run a loop to update the price of an open stop loss order based on price 
changes in the underlying security.  

**Handling order execution**

You'll often want to run specific actions when a placed order has executed and,
in our example, we've created the *after_buy_order()*, *after_sell_order()*, and
*after_order()* methods to help us deal with this.

.. code-block:: python

  class TradingSession:
  ...
    def after_buy_order(self):
      self.sell_order.cancel_order()
      self.position += self.buy_order.quantity
      self.after_order(self.buy_order)

    def after_sell_order(self):
      self.buy_order.cancel_order()
      self.position -= self.sell_order.quantity
      self.after_order(self.sell_order)

    def after_order(self, order):
      log_in_background(
        called_from = 'after_order',
        tags = ['user-message'], 
        account_key = self.account.account_key,
        symbol = self.symbol,
        message = '{}: Order {} executed to {} {} shares of {} for {} (Account: {})'.format(
          time.strftime('%H:%M:%S', time.localtime()),
          order.order_id,
          order.action,
          order.quantity,
          order.symbol,
          order.price,
          order.account_key))
  ...

In *after_buy_order()*, we're first canceling our sell order, then updating our 
position by adding our order quantity, then we're running *after_order()*.
In *after_sell_order()*, we're first canceling our buy order, then updating our 
position by adding our order quantity, then we're running *after_order()*.
In *after_order()*, we can set logic to run after each order. In our example,
we're simply logging an update that the order is executed, but you're likely to
include additional steps for a different strategy. 

**Closing out your position**

We've also created a function to close out our position at the end of the day.

.. code-block:: python

  class TradingSession:
  ...
    def close_position(self):
      quantity = abs(self.position)
      if self.position == 0:
        self.buy_order.cancel_order()
        self.sell_order.cancel_order()
      elif self.position > 0:
        self.exit_order = MarketOrder(
          client = self.client,
          account_key = self.account.account_key,
          symbol = self.symbol,
          action = 'SELL',
          quantity = quantity)
        self.exit_order.place_order()
      elif self.position < 0:
        self.exit_order = MarketOrder(
          client = self.client,
          account_key = self.account.account_key,
          symbol = self.symbol,
          action = 'BUY_TO_COVER',
          quantity = quantity)
        self.exit_order.place_order()

If our position is 0, then neither of our orders has executed, so we'll need to 
cancel both orders. Otherwise, if our position is positive, we place a market
order to sell our entire position, and we place a market order to buy to cover
if our position is negative.