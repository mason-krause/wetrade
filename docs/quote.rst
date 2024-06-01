.. _quote:

==================================
Getting quotes
==================================

``wetrade`` provides a few different types of quotes for different trading 
needs. A :class:`Quote <wetrade.quote.Quote>` can be used to track an 
individual stock, while :class:`DataFrameQuote <wetrade.quote.DataFrameQuote>`
and :class:`MultiQuote <wetrade.quote.MultiQuote>` have additional functionality 
for performing complex calculations and tracking multiple securities at once.

See below for examples on getting quotes with ``wetrade``:

++++++++++++++++++++++++++++++
Example usage
++++++++++++++++++++++++++++++

After creating a new :class:`Quote <wetrade.quote.Quote>`, you can get detailed
quotes or access just the opening or latest price. You can also the price updated 
throughout the day so that Quote().last_price always stays current.

.. code-block:: python

  import time
  from wetrade.api import APIClient
  from wetrade.quote import Quote


  def main():
    my_api_client = APIClient()
    my_quote = Quote(client=client, symbol='IBM')
    # Get the most recent quote details
    quote = my_quote.get_quote()
    print(f'Quote details: {quote}')
    # Get the opening price or the last price
    open = my_quote.get_open()
    last_price = my_quote.get_last_price()
    print(f'Opening price: {open}; Last price:{last_price}')
    # Keep my_quote.last_price up to date
    my_quote.monitor_in_background()
    for i in range(5):
      print(f'Price {i+1}: {my_quote.last_price}')
      time.sleep(2)


  if __name__ == '__main__':
    main()

++++++++++++++++
Detailed usage
++++++++++++++++

.. autoclass:: wetrade.quote.Quote
  :members:
  :undoc-members:

.. autoclass:: wetrade.quote.DataFrameQuote
  :members:
  :undoc-members:

.. autoclass:: wetrade.quote.MultiQuote
  :members:
  :undoc-members: