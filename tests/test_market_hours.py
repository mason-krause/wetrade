import datetime
import pytest
from wetrade.market_hours import MarketHours
from unittest.mock import patch, MagicMock


@patch('wetrade.market_hours.datetime', wraps=datetime)
class TestMarketHours:
  @classmethod
  def setup_class(cls):
    cls.market_hours = MarketHours('2024-06-03')

  def test_check_market_hours(self, mock_dt):
    hours = self.market_hours.check_market_hours()
    assert hours['open'] == '09:30:00'
    assert hours['close'] == '16:00:00'
  
  def test_change_date(self, mock_dt):
    self.market_hours.change_date('2024-06-05')
    assert self.market_hours.date_str == '2024-06-05'
    assert self.market_hours.open == datetime.datetime.strptime(
      '2024-06-05 09:30:00-04:00',
      '%Y-%m-%d %H:%M:%S%z')
    self.market_hours.change_date('2024-06-03')

  def test_market_has_closed(self, mock_dt):
    mock_dt.datetime.now = MagicMock(return_value=datetime.datetime.strptime(
      '2024-06-03 13:00:00-04:00',
      '%Y-%m-%d %H:%M:%S%z'))
    assert self.market_hours.market_has_closed() == False
    mock_dt.datetime.now = MagicMock(return_value=datetime.datetime.strptime(
      '2024-06-03 17:00:00-04:00',
      '%Y-%m-%d %H:%M:%S%z'))
    assert self.market_hours.market_has_closed() == True

  def test_market_has_opened(self, mock_dt):
    mock_dt.datetime.now = MagicMock(return_value=datetime.datetime.strptime(
      '2024-06-03 08:00:00-04:00',
      '%Y-%m-%d %H:%M:%S%z'))
    assert self.market_hours.market_has_opened() == False
    mock_dt.datetime.now = MagicMock(return_value=datetime.datetime.strptime(
      '2024-06-03 14:00:00-04:00',
      '%Y-%m-%d %H:%M:%S%z'))
    assert self.market_hours.market_has_opened() == True

  def test_seconds_till_close(self, mock_dt):
    mock_dt.datetime.now = MagicMock(return_value=datetime.datetime.strptime(
      '2024-06-03 13:00:00-04:00',
      '%Y-%m-%d %H:%M:%S%z'))
    sec_count = self.market_hours.seconds_till_close()
    assert sec_count == 10800.00

  def test_seconds_till_open(self, mock_dt):
    mock_dt.datetime.now = MagicMock(return_value=datetime.datetime.strptime(
      '2024-06-03 08:00:00-04:00',
      '%Y-%m-%d %H:%M:%S%z'))
    sec_count = self.market_hours.seconds_till_open()
    assert sec_count == 5400.00

  @pytest.mark.timeout(10)
  def test_wait_for_market_open(self, mock_dt):
    mock_dt.datetime.now = MagicMock(return_value=datetime.datetime.strptime(
      '2024-06-03 09:29:58-04:00',
      '%Y-%m-%d %H:%M:%S%z'))
    self.market_hours.wait_for_market_open()

  def test_now_est(self, mock_dt):
    mock_dt.datetime.now = datetime.datetime.now
    assert str(self.market_hours.now_est())[-6:] == '-04:00'
    