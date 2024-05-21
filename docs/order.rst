.. _order:

==================================
Placing orders with ``wetrade``
==================================

``wetrade`` makes it easy to place stock trades using **StopOrder**, 
**LimitOrder**, **StopLimitOrder**, **MarketOrder** objects. There is also a
provided **ConvertingStopOrder** which converts from a stop order to a market
order when out of range or rejected. 


.. autoclass:: wetrade.order.BaseOrder
  :members:
  :undoc-members:
  :exclude-members: preview_order, preview_update_price

.. autoclass:: wetrade.order.StopOrder

.. autoclass:: wetrade.order.LimitOrder

.. autoclass:: wetrade.order.StopLimitOrder

.. autoclass:: wetrade.order.MarketOrder

.. autoclass:: wetrade.order.ConvertingStopOrder