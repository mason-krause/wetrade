from .test_quote import TestQuote
from wetrade.quote import DataFrameQuote
from tests.mock_api import MockAPIClient as APIClient


class TestDataFrameQuote(TestQuote):
  def setup_class(self):
    client = APIClient()
    self.quote = DataFrameQuote(client=client, symbol='GOOG')