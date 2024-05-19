import unittest
from wetrade.api import APIClient
from wetrade.user_session import SimpleUserSession
from .sandbox_responses import account_responses, quote_responses, order_responses
try:
  from settings import config_options
except ModuleNotFoundError:
  from wetrade.project_template.settings import config_options


class TestAPIClient(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.user_session = SimpleUserSession(config=config_options['sandbox'])
    cls.client = APIClient(cls.user_session)

  def test_request_account_list(self):
    response = self.client.request_account_list()
    self.assertEqual(
      response,
      (account_responses.account_list_response, 200),
      'Incorrect account list response received')

  def test_request_account_balance(self):
    account_key = 'vQMsebA1H5WltUfDkJP48g'
    response = self.client.request_account_balance(account_key)
    self.assertEqual(
      response,
      (account_responses.balance_response, 200),
      'Incorrect account balance response received')

  def test_request_account_portfolio(self):
    account_key = 'vQMsebA1H5WltUfDkJP48g'
    response = self.client.request_account_portfolio(account_key)
    self.assertEqual(
      response,
      (account_responses.portfolio_response, 200),
      'Incorrect account portfolio response received')
    
  def test_request_account_orders(self):
    account_key = 'vQMsebA1H5WltUfDkJP48g'
    start_date = '05012024'
    end_date = '05012024'
    response = self.client.request_account_orders(account_key, start_date, end_date)
    self.assertEqual(
      response,
      (account_responses.orders_response, 200),
      'Incorrect account orders response received')
    
  def test_request_quote(self):
    symbol = 'GOOG'
    response = self.client.request_quote(symbol)
    self.assertEqual(
      response,
      (quote_responses.quote_response, 200),
      'Incorrect quote response received')
    
  def test_request_order_preview(self):
    account_key = 'vQMsebA1H5WltUfDkJP48g'
    order_data = {
      'PreviewOrderRequest': {
        'orderType': 'EQ', # [EQ, OPTN, SPREADS, BUY_WRITES, BUTTERFLY, IRON_BUTTERFLY, CONDOR, IRON_CONDOR, MF, MMF]
        'clientOrderId': 1000000000,
        'Order': {
          'allOrNone': 'false',
          'priceType': 'LIMIT', # [MARKET, LIMIT, STOP, STOP_LIMIT, TRAILING_STOP_CNST_BY_LOWER_TRIGGER, UPPER_TRIGGER_BY_TRAILING_STOP_CNST, TRAILING_STOP_PRCT_BY_LOWER_TRIGGER, UPPER_TRIGGER_BY_TRAILING_STOP_PRCT, TRAILING_STOP_CNST, TRAILING_STOP_PRCT, HIDDEN_STOP, HIDDEN_STOP_BY_LOWER_TRIGGER, UPPER_TRIGGER_BY_HIDDEN_STOP, NET_DEBIT, NET_CREDIT, NET_EVEN, MARKET_ON_OPEN, MARKET_ON_CLOSE, LIMIT_ON_OPEN, LIMIT_ON_CLOSE]
          'orderTerm': 'GOOD_FOR_DAY', # [GOOD_UNTIL_CANCEL, GOOD_FOR_DAY, GOOD_TILL_DATE, IMMEDIATE_OR_CANCEL, FILL_OR_KILL]
          'marketSession': 'REGULAR',
          'stopPrice': 120,
          'limitPrice': 120,
          'stopLimitPrice': 120,
          'Instrument': {
            'Product': {
              'securityType': 'EQ',
              'symbol': 'IBM'},
            'orderAction': 'BUY', # [BUY, SELL, BUY_TO_COVER, SELL_SHORT, BUY_OPEN, BUY_CLOSE, SELL_OPEN, SELL_CLOSE, EXCHANGE]
            'quantityType': 'QUANTITY',
            'quantity': 100}}}}
    response = self.client.request_order_preview(account_key, order_data)
    self.assertEqual(
      response,
      (order_responses.preview_order_response, 200),
      'Incorrect preview order response received')
    
  def test_request_order_place(self):
    account_key = 'vQMsebA1H5WltUfDkJP48g'
    order_data = {
        'PlaceOrderRequest': {
          'orderType': 'EQ',
          'clientOrderId': 1000000000,
          'PreviewIds': [{'previewId': 1627181131}],
          'Order': [{
            'Instrument': [{
              'Product': {
                'securityType': 'EQ',
                'symbol': 'IBM'},
              'orderAction': 'BUY',
              'quantity': 100,
              'quantityType': 'QUANTITY',
              'reserveOrder': False,
              'symbolDescription': ''}],
            'allOrNone': False,
            'egQual': 'EG_QUAL_OUTSIDE_GUARANTEED_PERIOD',
            'estimatedCommission': 6.99,
            'limitPrice': 120,
            'marketSession': 'EXTENDED',
            'orderTerm': 'GOOD_FOR_DAY',
            'priceType': 'LIMIT',
            'stopPrice': 0}]}}
    response = self.client.request_order_place(account_key, order_data)
    self.assertEqual(
      response,
      (order_responses.place_order_response, 200),
      'Incorrect place order response received')
    
  def test_request_order_change_preview(self):
    account_key = 'vQMsebA1H5WltUfDkJP48g'
    order_id = 529
    order_data = {
      'PreviewOrderRequest': {
        'orderType': 'EQ', # [EQ, OPTN, SPREADS, BUY_WRITES, BUTTERFLY, IRON_BUTTERFLY, CONDOR, IRON_CONDOR, MF, MMF]
        'clientOrderId': 1000000000,
        'Order': {
          'allOrNone': 'false',
          'priceType': 'LIMIT', # [MARKET, LIMIT, STOP, STOP_LIMIT, TRAILING_STOP_CNST_BY_LOWER_TRIGGER, UPPER_TRIGGER_BY_TRAILING_STOP_CNST, TRAILING_STOP_PRCT_BY_LOWER_TRIGGER, UPPER_TRIGGER_BY_TRAILING_STOP_PRCT, TRAILING_STOP_CNST, TRAILING_STOP_PRCT, HIDDEN_STOP, HIDDEN_STOP_BY_LOWER_TRIGGER, UPPER_TRIGGER_BY_HIDDEN_STOP, NET_DEBIT, NET_CREDIT, NET_EVEN, MARKET_ON_OPEN, MARKET_ON_CLOSE, LIMIT_ON_OPEN, LIMIT_ON_CLOSE]
          'orderTerm': 'GOOD_FOR_DAY', # [GOOD_UNTIL_CANCEL, GOOD_FOR_DAY, GOOD_TILL_DATE, IMMEDIATE_OR_CANCEL, FILL_OR_KILL]
          'marketSession': 'REGULAR',
          'stopPrice': 120,
          'limitPrice': 120,
          'stopLimitPrice': 120,
          'Instrument': {
            'Product': {
              'securityType': 'EQ',
              'symbol': 'IBM'},
            'orderAction': 'BUY', # [BUY, SELL, BUY_TO_COVER, SELL_SHORT, BUY_OPEN, BUY_CLOSE, SELL_OPEN, SELL_CLOSE, EXCHANGE]
            'quantityType': 'QUANTITY',
            'quantity': 100}}}}
    response = self.client.request_order_change_preview(account_key, order_id, order_data)
    self.assertEqual(
      response,
      (order_responses.preview_update_response, 200),
      'Incorrect preview order update response received')   
     
  def test_request_order_change_place(self):
    account_key = 'vQMsebA1H5WltUfDkJP48g'
    order_id = 529
    order_data = {
      'PlaceOrderRequest': {
        'orderType': 'EQ',
        'clientOrderId': 1000000000,
        'PreviewIds': [{'previewId': 1627181131}],
        'Order': [{
          'Instrument': [{
            'Product': {
              'securityType': 'EQ',
              'symbol': 'IBM'},
            'orderAction': 'BUY',
            'quantity': 100,
            'quantityType': 'QUANTITY',
            'reserveOrder': False,
            'symbolDescription': ''}],
          'allOrNone': False,
          'egQual': 'EG_QUAL_OUTSIDE_GUARANTEED_PERIOD',
          'estimatedCommission': 6.99,
          'limitPrice': 120,
          'marketSession': 'EXTENDED',
          'orderTerm': 'GOOD_FOR_DAY',
          'priceType': 'LIMIT',
          'stopPrice': 0}]}}
    response = self.client.request_order_change_place(account_key, order_id, order_data)
    self.assertEqual(
      response,
      (order_responses.place_update_response, 200),
      'Incorrect place order update response received')
        
  def test_request_order_cancel(self):
    account_key = 'vQMsebA1H5WltUfDkJP48g'
    order_id = 773
    symbol = 'IBM'
    response = self.client.request_order_cancel(account_key, order_id, symbol)
    self.assertEqual(
      response,
      (order_responses.cancel_order_response, 200),
      'Incorrect cancel order response received')      
         
  def test_request_order_status(self):
    account_key = 'vQMsebA1H5WltUfDkJP48g'
    order_id = 773
    symbol = 'IBM'
    response = self.client.request_order_status(account_key, order_id, symbol)
    self.assertEqual(
      response,
      (order_responses.order_status_response, 500),
      'Incorrect order status response received')   