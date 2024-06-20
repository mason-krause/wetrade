import pytest
import time
from wetrade.order import BaseOrder
from tests.mock_api import MockAPIClient as APIClient

 
class TestBaseOrder:
  @classmethod
  def setup_class(cls):
    client = APIClient()
    cls.order = BaseOrder(
      client = client, 
      account_key = 'vQMsebA1H5WltUfDkJP48g',
      symbol = 'IBM',
      action = 'BUY',
      quantity = 100,
      price = 120.00)
    
  @classmethod
  def teardown_class(cls):
    cls.order.disable_await_status = True

  def test_preview_order(self):
    preview = self.order.preview_order()
    preview_id = preview['PreviewIds'][0]['previewId']
    assert preview_id == 1627181131, 'Error getting order preview'
    
  def test_place_order(self):
    response = self.order.place_order()
    order_id = response['OrderIds'][0]['orderId']
    assert order_id == 529, 'Error placing order'

  def test_preview_update_price(self):
    new_price = 120
    preview = self.order.preview_update_price(new_price)
    preview_id = preview['PreviewIds'][0]['previewId']
    assert preview_id == 1627181131, 'Error getting order update preview'
    
  def test_update_price(self):
    new_price = 120
    response = self.order.update_price(new_price)
    order_id = response['OrderIds'][0]['orderId']
    assert order_id == 529, 'Error placing order update'
      
  def test_to_market_order(self):
    response = self.order.to_market_order()
    order_id = response['OrderIds'][0]['orderId']
    assert order_id == 529, 'Error placing order update - convert to market'
      
  def test_cancel_order(self):
    if self.order.order_id == 0:
      self.order.place_order()
    canceled = self.order.cancel_order()
    assert canceled == True, 'Error canceling order'
       
  def test_check_status(self):
    if self.order.order_id == 0:
      self.order.place_order()
    status = self.order.check_status()
    assert status in ('OPEN', 'EXECUTED'), 'Error getting order status'

  @pytest.mark.timeout(10)
  def test_wait_for_status(self):
    self.order.client.reset_order_detail_queue()
    if self.order.order_id == 0:
      self.order.place_order()
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.order.wait_for_status('EXECUTED', then=func)
    assert waiting == False, 'Error waiting for status'

  def test_run_when_status(self):
    self.order.client.reset_order_detail_queue()
    if self.order.order_id == 0:
      self.order.place_order()
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.order.run_when_status('EXECUTED', func=func)
    time.sleep(2)
    assert waiting == False, 'Error waiting for status'
