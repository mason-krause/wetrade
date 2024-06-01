.. _market_hours:

========================================
Getting market hours
========================================

Unfortunately, the E-Trade API does not provide an endpoint for looking up
market hours, so `we created an API with this information <https://markethours.info/>`__.
We also created a handful of useful tools for localizing to EST and referencing
the market schedule. Since `markethours.info <https://markethours.info/>`__ 
doesn't require an E-Trade account, you don't need an :class:`APIClient <wetrade.api.APIClient>` 
to use :class:`MarketHours <wetrade.market_hours.MarketHours>`.

See below for examples for using :class:`MarketHours <wetrade.market_hours.MarketHours>`:

++++++++++++++++
Example usage
++++++++++++++++

.. code-block:: python

  from wetrade.market_hours import MarketHours


  def main():
    todays_hours = MarketHours()

    # Check if the market has opened
    print(todays_hours.market_has_opened())

    # Check if the market has closed
    print(todays_hours.market_has_closed())

    # Wait for the market to open
    todays_hours.wait_for_market_open()

    # See the number of seconds until open
    print(todays_hours.seconds_till_open())

    # Do something if there's less than a minute before
    # close. Something like this could be used in a loop
    if todays_hours.seconds_till_close() < 60:
      print('Hurry up!')

    # Show open, close, and current time in EST
    print(todays_hours.open)
    print(todays_hours.close)
    print(todays_hours.now_est())


  if __name__ == '__main__':
    main()

++++++++++++++++
Detailed usage
++++++++++++++++

.. autoclass:: wetrade.market_hours.MarketHours
  :members:
  :undoc-members: