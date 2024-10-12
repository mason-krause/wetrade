.. _order:

==================================
Placing orders
==================================

``wetrade`` makes it easy to place stock trades using **StopOrder**, 
**LimitOrder**, **StopLimitOrder**, **MarketOrder** objects. There is also a
provided **ConvertingStopOrder** which converts from a stop order to a market
order when out of range or rejected. 

See below for examples on placing orders with ``wetrade``:

++++++++++++++++++++++++++++++
Example usage
++++++++++++++++++++++++++++++

After creating a new Order object, you'll need to run place_order() to place 
the order with E-Trade. You can then check your status, cancel or update your
order and react to order updates.


.. code-block:: python

  import time
  from wetrade.api import APIClient
  from wetrade.account import Account
  from wetrade.order import LimitOrder


  def main():
    my_api_client = APIClient()
    account = Account(client=my_api_client)
    # Create then place order
    my_order = LimitOrder(
      client = my_api_client,
      account_key = account.account_key,
      symbol = 'NVDA',
      action = 'BUY',
      quantity = 1,
      price = 50.00)
    my_order.place_order()
    # Update your order's price
    my_order.update_price(55.00)
    # Check your order status
    status = my_order.check_status()
    print(f'Order status: {status}')
    # Print an update when your order is canceled
    my_order.run_when_status(
        'CANCELLED', 
        func = print, 
        func_args = ['Your order has been canceled'])
    # Cancel your order
    my_order.cancel_order()


  if __name__ == '__main__':
    main()

++++++++++++++++
Detailed usage
++++++++++++++++

.. autoclass:: wetrade.order.BaseOrder
  :members:
  :undoc-members:
  :exclude-members: preview_order, preview_update_price

.. autoclass:: wetrade.order.StopOrder

.. autoclass:: wetrade.order.LimitOrder

.. autoclass:: wetrade.order.StopLimitOrder

.. autoclass:: wetrade.order.MarketOrder

.. autoclass:: wetrade.order.ConvertingStopOrder