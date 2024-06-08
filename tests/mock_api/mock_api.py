import copy
from unittest.mock import MagicMock
from . import account_responses, quote_responses, order_responses

def generate_test_quote(last_price=577.51):
  r = copy.deepcopy(quote_responses.quote_response)
  r['QuoteResponse']['QuoteData'][0]['All']['lastTrade'] = last_price
  return r

class MockAPIClient:
  def __init__(self, session=None):
    self.session = MagicMock()

  def request_account_list(self):
    return (account_responses.account_list_response, 200)
  
  def request_account_balance(self, account_key):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    return (account_responses.balance_response, 200)
  
  def request_account_portfolio(self, account_key):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    return (account_responses.portfolio_response, 200)
  
  def request_account_orders(self, account_key, start_date='', end_date='', marker=''):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    return (account_responses.orders_response, 200)
      
  def request_quote(self, symbol):
    if ',' in symbol:
      if not hasattr(self, 'multiquote_response_queue'):
        self.multiquote_response_queue = iter(
          (quote_responses.multi_responses[0], ) * 4)
      next_response =next(
        self.multiquote_response_queue, 
        quote_responses.multi_responses[1])
    else:
      assert symbol == 'GOOG'
      if not hasattr(self, 'quote_response_queue'):
        self.quote_response_queue = iter((
          *(quote_responses.quote_response, ) * 2,
          *(generate_test_quote(700.50), ) * 2 ))
      next_response =next(
        self.quote_response_queue,
        generate_test_quote(800.75))
      return (next_response, 200)
  
  def request_order_preview(self, account_key, order_data):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    assert 'PreviewOrderRequest' in order_data
    assert order_data['PreviewOrderRequest']['orderType'] == 'EQ'
    return (order_responses.preview_order_response, 200)
  
  def request_order_place(self, account_key, order_data):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    assert 'PlaceOrderRequest' in order_data
    return (order_responses.place_order_response, 200)
  
  def request_order_change_preview(self, account_key, order_id, order_data):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    assert order_id == 529
    assert 'PreviewOrderRequest' in order_data
    return (order_responses.preview_update_response, 200)
    
  def request_order_change_place(self, account_key, order_id, order_data):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    assert order_id == 529
    assert 'PlaceOrderRequest' in order_data
    return (order_responses.place_update_response, 200)

  def request_order_cancel(self, account_key, order_id, symbol=''):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    assert order_id == 529
    assert symbol == 'IBM'
    return (order_responses.cancel_order_response, 200)
  
  def request_order_status(self, account_key, order_id, symbol=''):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    assert order_id == 529
    assert symbol == 'IBM'
    if not hasattr(self, 'order_status_response_queue'):
      self.order_status_response_queue = iter(
        (order_responses.order_status_responses[0], ) * 4)
    next_response =next(
      self.order_status_response_queue, 
      order_responses.order_status_responses[1])
    return (next_response, 200)