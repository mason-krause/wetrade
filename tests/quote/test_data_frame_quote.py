import unittest
from wetrade.quote import DataFrameQuote
from tests.mock_api import MockAPIClient as APIClient


class TestDataFrameQuote(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    client = APIClient()
    cls.quote = DataFrameQuote(client=client, symbol='GOOG')