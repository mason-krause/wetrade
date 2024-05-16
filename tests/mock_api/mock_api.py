from unittest.mock import MagicMock
from . import account_responses, quote_responses, order_responses


class MockAPIClient(MagicMock):
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
    assert symbol == 'GOOG'
    return (quote_responses.quote_response, 200)
  
  def request_order_preview(self, account_key, order_data):
    assert account_key == 'vQMsebA1H5WltUfDkJP48g'
    assert 'PreviewOrderRequest' in order_data
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
    return (order_responses.order_status_response, 200)