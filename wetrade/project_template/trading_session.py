import time
from wetrade.api import APIClient
from wetrade.account import Account
from wetrade.quote import Quote
from wetrade.order import StopOrder, MarketOrder
from wetrade.market_hours import MarketHours
from wetrade.utils import log_in_background


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

  def after_buy_order(self):
    self.sell_order.cancel_order()
    self.position += self.buy_order.quantity
    self.after_order(self.buy_order)

  def after_sell_order(self):
    self.buy_order.cancel_order()
    self.position -= self.buy_order.quantity
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
