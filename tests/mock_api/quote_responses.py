quote_response = {
  'QuoteResponse': {
    'QuoteData': [{
      'All': {
        'adjustedFlag': False,
        'ask': 579.73,
        'askSize': 100,
        'askTime': '16:00:00 EDT 06-20-2012',
        'averageVolume': 13896435,
        'beta': 0.93,
        'bid': 574.04,
        'bidExchange': '',
        'bidSize': 100,
        'bidTime': '16:00:00 EDT 06-20-2012',
        'cashDeliverable': 0,
        'changeClose': 0.0,
        'changeClosePercentage': 0.0,
        'companyName': 'GOOGLE INC CL A',
        'contractSize': 0.0,
        'daysToExpiration': 0,
        'declaredDividend': 0.0,
        'dirLast': '1',
        'dividend': 0.0,
        'dividendPayableDate': 0,
        'eps': 32.99727,
        'estEarnings': 43.448,
        'exDividendDate': 1344947183,
        'expirationDate': 0,
        'high': 0.0,
        'high52': 670.25,
        'intrinsicValue': 0.0,
        'lastTrade': 577.51,
        'low': 0.0,
        'low52': 473.02,
        'marketCap': 188282697750.0,
        'nextEarningDate': '',
        'open': 578.89,
        'openInterest': 0,
        'optionMultiplier': 0.0,
        'optionStyle': '',
        'pe': 17.5017,
        'previousClose': 577.51,
        'previousDayVolume': 2433786,
        'primaryExchange': 'NASDAQ NM',
        'sharesOutstanding': 326025,
        'symbolDescription': 'GOOGLE INC CL A',
        'timeOfLastTrade': 1341334800,
        'timePremium': 0.0,
        'totalVolume': 0,
        'upc': 0,
        'week52HiDate': 1325673870,
        'week52LowDate': 1308908670,
        'yield': 0.0 },
      'Product': {
        'securityType': 'EQ',
        'symbol': 'GOOG' },
      'ahFlag': 'false',
      'dateTime': '16:00:00 EDT 06-20-2012',
      'dateTimeUTC': 1340222400,
      'quoteStatus': 'REALTIME'}]}}

options_chain_response = {
  'OptionChainResponse': {
    'OptionPair': [
      {
        'Call': {
          'optionCategory': 'STANDARD',
          'optionRootSymbol': 'GOOG',
          'timeStamp': 1363975980,
          'adjustedFlag': False,
          'displaySymbol': "GOOG Mar 22 '13 $485 Call",
          'optionType': 'CALL',
          'strikePrice': 485.0,
          'symbol': 'GOOG',
          'bid': 0.02,
          'ask': 0.01,
          'bidSize': 0,
          'askSize': 25,
          'inTheMoney': 'n',
          'volume': 178,
          'openInterest': 2782,
          'netChange': -0.01,
          'lastPrice': 0.01,
          'quoteDetail': 'https://api.sit.etrade.com/v1/market/quote/GOOG:2013:3:22:CALL:485.000000',
          'osiKey': 'GOOG--130322C00485000',
          'OptionGreeks': {
            'rho': 0.0095,
            'vega': 0.0751,
            'theta': -0.018,
            'delta': 0.0848,
            'gamma': 0.0316,
            'iv': 0.1407,
            'currentValue': False
          }
        },
        'Put': {
          'optionCategory': 'STANDARD',
          'optionRootSymbol': 'GOOG',
          'timeStamp': 1363974660,
          'adjustedFlag': False,
          'displaySymbol': "GOOG Mar 22 '13 $485 Put",
          'optionType': 'PUT',
          'strikePrice': 485.0,
          'symbol': 'GOOG',
          'bid': 23.6,
          'ask': 23.9,
          'bidSize': 4,
          'askSize': 2,
          'inTheMoney': 'y',
          'volume': 81,
          'openInterest': 273,
          'netChange': -8.95,
          'lastPrice': 23.7,
          'quoteDetail': 'https://api.sit.etrade.com/v1/market/quote/GOOG:2013:3:22:PUT:485.000000',
          'osiKey': 'GOOG--130322P00485000',
          'OptionGreeks': {
            'rho': 0.0095,
            'vega': 0.0751,
            'theta': -0.018,
            'delta': 0.0848,
            'gamma': 0.0316,
            'iv': 0.1407,
            'currentValue': False
          }
        }
      }
    ],
    'SelectedED': {
      'month': 3,
      'year': 2013,
      'day': 22
    }
  }
}
