import copy
from unittest.mock import MagicMock
from . import account_responses, quote_responses, order_responses


def generate_quote_response(symbol='GOOG', last_prices=[577.51]):
  quote_list = []
  quote_template = quote_responses.quote_response['QuoteResponse']['QuoteData'][0]
  for i, sym in enumerate(symbol.split(',')):
    quote = copy.deepcopy(quote_template)
    quote['Product']['symbol'] = sym
    quote['All']['lastTrade'] = last_prices[i]
    quote_list.append(quote)
  return {'QuoteResponse': {'QuoteData': quote_list}}

def generate_order_detail_response(status='OPEN'):
  r = copy.deepcopy(order_responses.order_detail_response)
  r['OrdersResponse']['Order'][0]['OrderDetail'][0]['status'] = status
  return r

class MockAPIClient:
  def __init__(self, session=None):
    self.session = MagicMock()
    self.reset_quote_queue()
    self.reset_multiquote_queue()
    self.reset_order_detail_queue()

  def reset_quote_queue(self):
    self.quote_response_queue = iter((
      *(quote_responses.quote_response, ) * 2,
      *(generate_quote_response('GOOG', [200.10]), ) * 2,
      *(generate_quote_response('GOOG', [700.50]), ) * 2 ))
    
  def next_quote_response(self):
    return next(
      self.quote_response_queue,
      generate_quote_response('GOOG', [800.75]))
  
  def reset_multiquote_queue(self):  
    self.multiquote_response_queue = iter((
      *(generate_quote_response('TSLA,NVDA', [175.50, 750.45]), ) * 2,
      *(generate_quote_response('TSLA,NVDA', [50.50, 550.45]), ) * 2,
      *(generate_quote_response('TSLA,NVDA', [190.50, 850.45]), ) * 2))
    
  def next_multiquote_response(self):
    return next(
      self.multiquote_response_queue, 
      generate_quote_response('TSLA,NVDA', [210.50, 1050.45]))

  def reset_order_detail_queue(self):
    self.order_detail_response_queue = iter(
      (order_responses.order_detail_response, ) * 4)
    
  def next_order_detail_response(self):
    return next(
      self.order_detail_response_queue, 
      generate_order_detail_response('EXECUTED'))

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
    assert symbol in ('GOOG', 'NVDA,TSLA', 'TSLA,NVDA')
    if symbol == 'GOOG':
      return (self.next_quote_response(), 200)
    elif ',' in symbol:
      return (self.next_multiquote_response(), 200)
  
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
  
  def request_order_detail(self, account_key, order_id, symbol=''):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    assert order_id == 529
    assert symbol == 'IBM'
    return (self.next_order_detail_response(), 200)