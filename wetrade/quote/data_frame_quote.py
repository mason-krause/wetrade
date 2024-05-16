import time
import datetime
import pickle
import google.cloud.storage
import polars as pl 
import pandas as pd
from .quote import Quote
from wetrade.api import APIClient
from wetrade.utils import log_in_background, check_market_hours
try:
    from settings import quote_bucket
except ModuleNotFoundError:
  from unittest.mock import MagicMock as quote_bucket


class DataFrameQuote(Quote):
  def __init__(self, client:APIClient, symbol):
    super().__init__()
    self.data = pl.DataFrame(schema={ #maybe use numpy array instead of polars df
      'datetime': pl.Datetime,
      'datetime_epoch': pl.Int64,
      'ask': pl.Float64,
      'ask_size': pl.Int64,
      'ask_time': pl.Datetime,
      'bid': pl.Float64,
      'bid_size': pl.Int64,
      'bid_time': pl.Datetime,
      'last_trade': pl.Float64,
      'last_trade_time': pl.Int64,
      '30s_average': pl.Float64,
      '10s_average': pl.Float64})
    self.smoothed_price = 0.0

  def monitor_quote(self):
    if self.monitoring_active == False:
      market_close = check_market_hours()['close']
      if time.strftime('%H:%M', time.localtime()) > market_close:
        log_in_background(
          called_from = 'monitor_quote',
          tags = ['user-message'], 
          symbol = self.symbol,
          message = '{}: Markets are closed'.format(time.strftime('%H:%M:%S', time.localtime())))
      else:
        self.monitoring_active = True
      while self.monitoring_active == True and time.strftime('%H:%M', time.localtime()) < market_close:
        quote_data = self.get_quote()
        self.last_price = quote_data['All']['lastTrade']
        self.data.extend(pl.DataFrame({
          'datetime': datetime.datetime.strptime(quote_data['dateTime'], '%H:%M:%S %Z %m-%d-%Y'),
          'datetime_epoch': quote_data['dateTimeUTC'],
          'ask': quote_data['All']['ask'],
          'ask_size': quote_data['All']['askSize'],
          'ask_time': datetime.datetime.strptime(quote_data['All']['askTime'], '%H:%M:%S %Z %m-%d-%Y'),
          'bid': quote_data['All']['bid'],
          'bid_size': quote_data['All']['bidSize'],
          'bid_time': datetime.datetime.strptime(quote_data['All']['bidTime'], '%H:%M:%S %Z %m-%d-%Y'),
          'last_trade': quote_data['All']['lastTrade'],
          'last_trade_time': quote_data['All']['timeOfLastTrade'],
          '30s_average': 0.0,
          '10s_average': 0.0}))
        self.data = self.data.set_sorted('datetime').with_columns([
          pl.col('last_trade').rolling_mean(window_size='30s', by='datetime', closed='both').alias('30s_average'),
          pl.col('last_trade').rolling_mean(window_size='10s', by='datetime', closed='both').alias('10s_average')])
        self.smoothed_price = self.data[-1, '10s_average']
      time.sleep(.5)

  def export_data(self):
    filename = datetime.datetime.today().strftime('%Y_%m_%d') + '-' + self.ticker
    df = self.data.to_pandas()
    df.to_pickle('./export/data/{}.pkl'.format(filename))

  def upload_quote_data(self):
    log_in_background(
      called_from = 'upload_quote_data',
      tags = ['user-message'], 
      message = '{}: Uploading quote data to Google Cloud'.format(
        datetime.datetime.now().strftime('%H:%M:%S')))
    filename = datetime.datetime.today().strftime('%Y_%m_%d') + '-' + self.ticker
    df = self.data.to_pandas()
    storage_client = google.cloud.storage.Client()
    bucket = storage_client.bucket(quote_bucket)
    blob = bucket.blob(filename)
    with blob.open(mode='wb') as f:
      pickle.dump(df, f)

  def get_pd_data(self):
    return self.data.to_pandas()