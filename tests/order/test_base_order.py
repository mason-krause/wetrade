import unittest
from wetrade.order import BaseOrder
from tests.mock_api import MockAPIClient as APIClient


class TestBaseOrder(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    client = APIClient()
    cls.order = BaseOrder(
      client = client, 
      account_key = 'vQMsebA1H5WltUfDkJP48g',
      symbol = 'IBM',
      action = 'BUY',
      quantity = 100,
      price = 120.00)

  def test_preview_order(self):
    preview = self.order.preview_order()
    preview_id = preview['PreviewIds'][0]['previewId']
    self.assertEqual(
      preview_id,
      1627181131,
      'Error getting order preview')
    
  def test_place_order(self):
    response = self.order.place_order()
    order_id = response['OrderIds'][0]['orderId']
    self.assertEqual(
      order_id,
      529,
      'Error placing order')

  def test_preview_update_price(self):
    new_price = 120
    preview = self.order.preview_update_price(new_price)
    preview_id = preview['PreviewIds'][0]['previewId']
    self.assertEqual(
      preview_id,
      1627181131,
      'Error getting order update preview')
    
  def test_update_price(self):
    new_price = 120
    response = self.order.update_price(new_price)
    order_id = response['OrderIds'][0]['orderId']
    self.assertEqual(
      order_id,
      529,
      'Error placing order update')  
      
  def test_to_market_order(self):
    response = self.order.to_market_order()
    order_id = response['OrderIds'][0]['orderId']
    self.assertEqual(
      order_id,
      529,
      'Error placing order update- convert to market')
      
  def test_cancel_order(self):
    canceled = self.order.cancel_order()
    self.assertEqual(
      canceled,
      True,
      'Error canceling order')   
       
  def test_check_status(self):
    status = self.order.check_status()
    self.assertEqual(
      status,
      'OPEN',
      'Error getting order status')
