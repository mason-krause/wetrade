.. _options:

==================================
Trading options
==================================

You can trade options :ref:`Quotes <quote>` and :ref:`Orders <order>`

See below for examples on trading options with ``wetrade``:

++++++++++++++++++++++++++++++
Example usage
++++++++++++++++++++++++++++++

After creating a new :class:`Quote <wetrade.quote.Quote>` for a stock, you can
get an options chain using the Quote.get_options_chain() method. You can then 
place an order for a specific option by setting the security_type param to "OPTN"
and using the BUY_OPEN, BUY_CLOSE, SELL_OPEN, and SELL_CLOSE actions

.. code-block:: python

  import time
  from wetrade.api import APIClient
  from wetrade.quote import Quote
  from wetrade.account import Account
  from wetrade.order import LimitOrder


  def main():
    my_api_client = APIClient()
    account = Account(client=my_api_client)
    my_quote = Quote(client=my_api_client, symbol='IBM')
    # Get an options chain
    options_chain = my_quote.get_options_chain(expiry_date='2024-10-18', near_price=120)
    # Find your option symbol (eg: "IBM Oct 18 '24 $290 Put")
    my_symbol = options_chain[0]['Call']['displaySymbol']
    # Create and place a new order to purchase your options contract
    my_order = LimitOrder(
      client = my_api_client,
      account_key = account.account_key,
      symbol = my_symbol,
      security_type = 'OPTN',
      action = 'BUY_OPEN',
      quantity = 1,
      price = 5.00)
    my_order.place_order()
    my_order.cancel_order()


  if __name__ == '__main__':
    main()