account_list_response = {
  'AccountListResponse': {
    'Accounts': {
      'Account': [
        { 'accountDesc': 'Brokerage',
          'accountId': '823145980',
          'accountIdKey': 'dBZOKt9xDrtRSAOl4MSiiA',
          'accountMode': 'IRA',
          'accountName': 'NickName-1',
          'accountStatus': 'ACTIVE',
          'accountType': 'MARGIN',
          'closedDate': 0,
          'fcManagedMssbClosedAccount': False,
          'institutionType': 'BROKERAGE',
          'shareWorksAccount': False}, 
        { 'accountDesc': 'Complete Savings',
          'accountId': '583156360',
          'accountIdKey': 'vQMsebA1H5WltUfDkJP48g',
          'accountMode': 'CASH',
          'accountName': 'NickName-2',
          'accountStatus': 'ACTIVE',
          'accountType': 'INDIVIDUAL',
          'closedDate': 0,
          'fcManagedMssbClosedAccount': False,
          'institutionType': 'BROKERAGE',
          'shareWorksAccount': False},
        { 'accountDesc': 'INDIVIDUAL',
          'accountId': '707004180',
          'accountIdKey': '6_Dpy0rmuQ9cu9IbTfvF2A',
          'accountMode': 'CASH',
          'accountName': 'NickName-3',
          'accountStatus': 'ACTIVE',
          'accountType': 'INDIVIDUAL',
          'closedDate': 0,
          'fcManagedMssbClosedAccount': False,
          'institutionType': 'BROKERAGE',
          'shareWorksAccount': False},
        { 'accountDesc': 'INDIVIDUAL',
          'accountId': '835151430',
          'accountIdKey': 'xj1Dc18FTqWPqkEEVUr5rw',
          'accountMode': 'CASH',
          'accountName': '',
          'accountStatus': 'CLOSED',
          'accountType': 'CASH',
          'closedDate': 1521027780,
          'fcManagedMssbClosedAccount': False,
          'institutionType': 'BROKERAGE',
          'shareWorksAccount': False}]}}}

balance_response = {
  'BalanceResponse': {
    'Cash': {
      'fundsForOpenOrdersCash': 0.0, 
      'moneyMktBalance': 0.0},
    'Computed': {
      'OpenCalls': {
        'cashCall': 0.0},
      'RealTimeValues': {
        'netMv': -454.22,
        'netMvLong': 0.0,
        'totalAccountValue': 0.0},
      'cashAvailableForInvestment': 5000.0,
      'cashAvailableForWithdrawal': 0.0,
      'cashBalance': 5000.0,
      'fundsWithheldFromPurchasePower': 0.0,
      'fundsWithheldFromWithdrawal': 0.0,
      'netCash': -740.450013,
      'settledCashForInvestment': 0.0,
      'unSettledCashForInvestment': 0.0},
    'accountDescription': '',
    'accountId': '833535350',
    'accountType': 'MARGIN',
    'optionLevel': 'LEVEL_4'}}

portfolio_response = {
  'PortfolioResponse': {
    'AccountPortfolio': [{
      'Position':[
        { 'Product':  {
            'expiryDay': 0,
            'expiryMonth': 0,
            'expiryYear': 0,
            'productId': {'symbol': 'BR'},
            'securityType': 'EQ',
            'strikePrice': 0,
            'symbol': 'BR'},
          'Quick': 
            {'change': -0.28,
            'changePct': -1.3346,
            'lastTrade': 20.7,
            'lastTradeTime': 1343160240,
            'volume': 431591},
          'commissions': 0,
          'costPerShare': 0,
          'dateAcquired': -57600000,
          'daysGain': -2.7999,
          'daysGainPct': -1.3346,
          'lotsDetails': 'https://apisb.etrade.com/v1/accounts/E5Nd4LJBsEi_UyHm4Vio9g/portfolio/27005131',
          'marketValue': 207,
          'otherFees': 0,
          'pctOfPortfolio': 0.0018,
          'positionId': 27005131,
          'positionIndicator': 'TYPE2',
          'positionType': 'LONG',
          'pricePaid': 0,
          'quantity': 10,
          'quoteDetails': 'https://apisb.etrade.com/v1/market/quote/BR',
          'symbolDescription': 'BR',
          'todayCommissions': 0,
          'todayFees': 0,
          'todayPricePaid': 0,
          'todayQuantity': 0,
          'totalCost': 0,
          'totalGain': 207,
          'totalGainPct': 0},
        {'Product': {'expiryDay': 0,
                    'expiryMonth': 0,
                    'expiryYear': 0,
                    'productId': {'symbol': 'GLD'},
                    'securityType': 'EQ',
                    'strikePrice': 0,
                    'symbol': 'GLD'},
          'Quick': {'change': 0.49,
                    'changePct': 0.3201,
                    'lastTrade': 153.52,
                    'lastTradeTime': 1343160000,
                    'volume': 6510878},
          'commissions': 5,
          'costPerShare': 3.5,
          'dateAcquired': 1335250800000,
          'daysGain': 0.9799,
          'daysGainPct': 0.3201,
          'lotsDetails': 'https://apisb.etrade.com/v1/accounts/E5Nd4LJBsEi_UyHm4Vio9g/portfolio/4709131',
          'marketValue': 307.04,
          'otherFees': 0,
          'pctOfPortfolio': 0.0028,
          'positionId': 4709131,
          'positionIndicator': 'TYPE1',
          'positionType': 'LONG',
          'pricePaid': 1,
          'quantity': 2,
          'quoteDetails': 'https://apisb.etrade.com/v1/market/quote/GLD',
          'symbolDescription': 'GLD',
          'todayCommissions': 0,
          'todayFees': 0,
          'todayPricePaid': 0,
          'todayQuantity': 0,
          'totalCost': 7,
          'totalGain': 300.04,
          'totalGainPct': 4286.2857},
        {'Product': {'expiryDay': 0,
                    'expiryMonth': 0,
                    'expiryYear': 0,
                    'productId': {'symbol': 'MSFT'},
                    'securityType': 'EQ',
                    'strikePrice': 0,
                    'symbol': 'MSFT'},
          'Quick': {'change': -0.13,
                    'changePct': -0.4439,
                    'lastTrade': 29.15,
                    'lastTradeTime': 1343160000,
                    'volume': 47711254},
          'commissions': 5,
          'costPerShare': 6,
          'dateAcquired': 1335250800000,
          'daysGain': -0.13,
          'daysGainPct': -0.4439,
          'lotsDetails': 'https://apisb.etrade.com/v1/accounts/E5Nd4LJBsEi_UyHm4Vio9g/portfolio/4729131',
          'marketValue': 29.1499,
          'otherFees': 0,
          'pctOfPortfolio': 0.0002,
          'positionId': 4729131,
          'positionIndicator': 'TYPE2',
          'positionType': 'LONG',
          'pricePaid': 1,
          'quantity': 1,
          'quoteDetails': 'https://apisb.etrade.com/v1/market/quote/MSFT',
          'symbolDescription': 'MSFT',
          'todayCommissions': 0,
          'todayFees': 0,
          'todayPricePaid': 0,
          'todayQuantity': 0,
          'totalCost': 6,
          'totalGain': 23.1499,
          'totalGainPct': 385.8333},
        {'Product': {'expiryDay': 0,
                    'expiryMonth': 0,
                    'expiryYear': 0,
                    'productId': {'symbol': 'MSFT'},
                    'securityType': 'EQ',
                      'strikePrice': 0,
                      'symbol': 'MSFT'},
          'Quick': {'change': -0.13,
                    'changePct': -0.4439,
                    'lastTrade': 29.15,
                    'lastTradeTime': 1343160000,
                    'volume': 47711254},
          'commissions': 0,
          'costPerShare': 0,
          'dateAcquired': -57600000,
          'daysGain': 1.3,
          'daysGainPct': -0.4439,
          'lotsDetails': 'https://apisb.etrade.com/v1/accounts/E5Nd4LJBsEi_UyHm4Vio9g/portfolio/23971131',
          'marketValue': -291.5,
          'otherFees': 0,
          'pctOfPortfolio': -0.0026,
          'positionId': 23971131,
          'positionIndicator': 'TYPE5',
          'positionType': 'SHORT',
          'pricePaid': 0,
          'quantity': -10,
          'quoteDetails': 'https://apisb.etrade.com/v1/market/quote/MSFT',
          'symbolDescription': 'MSFT',
          'todayCommissions': 0,
          'todayFees': 0,
          'todayPricePaid': 0,
          'todayQuantity': 0,
          'totalCost': 0,
          'totalGain': -291.5,
          'totalGainPct': 0},
        {'Product': {'expiryDay': 0,
                    'expiryMonth': 0,
                    'expiryYear': 0,
                    'productId': {'symbol': 'RBL'},
                    'securityType': 'EQ',
                    'strikePrice': 0,
                    'symbol': 'RBL'},
          'Quick': {'change': -0.26,
                    'changePct': -1.0252,
                    'lastTrade': 25.1,
                    'lastTradeTime': 1343159760,
                    'volume': 11827},
          'commissions': 5,
          'costPerShare': 3.5,
          'dateAcquired': 1335250800000,
          'daysGain': -0.52,
          'daysGainPct': -1.0252,
          'lotsDetails': 'https://apisb.etrade.com/v1/accounts/E5Nd4LJBsEi_UyHm4Vio9g/portfolio/4725131',
          'marketValue': 50.2,
          'otherFees': 0,
          'pctOfPortfolio': 0.0004,
          'positionId': 4725131,
          'positionIndicator': 'TYPE2',
          'positionType': 'LONG',
          'pricePaid': 1,
          'quantity': 2,
          'quoteDetails': 'https://apisb.etrade.com/v1/market/quote/RBL',
          'symbolDescription': 'RBL',
          'todayCommissions': 0,
          'todayFees': 0,
          'todayPricePaid': 0,
          'todayQuantity': 0,
          'totalCost': 7,
          'totalGain': 43.2,
          'totalGainPct': 617.1428},
        {'Product': {'expiryDay': 0,
                    'expiryMonth': 0,
                    'expiryYear': 0,
                    'productId': {'symbol': 'RPI'},
                    'securityType': 'EQ',
                    'strikePrice': 0,
                    'symbol': 'RPI'},
          'Quick': {'change': 0,
                    'changePct': 0,
                    'lastTrade': 1.43,
                    'lastTradeTime': 1343150700,
                    'volume': 1803},
          'commissions': 5,
          'costPerShare': 32.56,
          'dateAcquired': 1335250800000,
          'daysGain': 0,
          'daysGainPct': 0,
          'lotsDetails': 'https://apisb.etrade.com/v1/accounts/E5Nd4LJBsEi_UyHm4Vio9g/portfolio/20841131',
          'marketValue': 2.8599,
          'otherFees': 45,
          'pctOfPortfolio': 0.0,
          'positionId': 20841131,
          'positionIndicator': 'TYPE2',
          'positionType': 'LONG',
          'pricePaid': 7.5599,
          'quantity': 2,
          'quoteDetails': 'https://apisb.etrade.com/v1/market/quote/RPI',
          'symbolDescription': 'RPI',
          'todayCommissions': 0,
          'todayFees': 0,
          'todayPricePaid': 0,
          'todayQuantity': 0,
          'totalCost': 65.12,
          'totalGain': -62.2599,
          'totalGainPct': -95.6081},
        {'Product': {'expiryDay': 0,
                    'expiryMonth': 0,
                    'expiryYear': 0,
                    'productId': {'symbol': 'RXD'},
                    'securityType': 'EQ',
                    'strikePrice': 0,
                    'symbol': 'RXD'},
          'Quick': {'change': 0.432,
                    'changePct': 2.6799,
                    'lastTrade': 16.552,
                    'lastTradeTime': 1343157480,
                    'volume': 2200},
          'commissions': 2.99,
          'costPerShare': 0,
          'dateAcquired': 1335250800000,
          'daysGain': -1.296,
          'daysGainPct': 2.6799,
          'lotsDetails': 'https://apisb.etrade.com/v1/accounts/E5Nd4LJBsEi_UyHm4Vio9g/portfolio/4732131',
          'marketValue': -49.6559,
          'otherFees': 0.0099,
          'pctOfPortfolio': -0.0004,
          'positionId': 4732131,
          'positionIndicator': 'TYPE5',
          'positionType': 'SHORT',
          'pricePaid': 1,
          'quantity': -3,
          'quoteDetails': 'https://apisb.etrade.com/v1/market/quote/RXD',
          'symbolDescription': 'RXD',
          'todayCommissions': 0,
          'todayFees': 0,
          'todayPricePaid': 0,
          'todayQuantity': 0,
          'totalCost': 0,
          'totalGain': -49.6559,
          'totalGainPct': -827.6}],
    'accountId': '833597000',
    'totalPages': 1}]}}

orders_response = {
  'OrdersResponse': {
    'marker': '12345678999',
    'next': 'https://api.sit.etrade.com/accounts/E5Nd4LJBsEi_UyHm4Vio9g/orders?marker=12345678999',
    'Order': [{
      'orderId': 479,
      'details': 'https://api.etrade.com/accounts/E5Nd4LJBsEi_UyHm4Vio9g/orders/479',
      'orderType': 'OPTN',
      'OrderDetail': [{
        'placedTime': 123453456,
        'orderValue': 123.0,
        'status': 'OPEN',
        'orderTerm': 'GOOD_FOR_DAY',
        'priceType': 'LIMIT',
        'limitPrice': 1.5,
        'stopPrice': 0,
        'marketSession': 'REGULAR',
        'allOrNone': False,
        'netPrice': 0,
        'netBid': 0,
        'netAsk': 0,
        'gcd': 0,
        'ratio': '',
        'Instrument': [{
          'symbolDescription': 'RESEARCH IN MOTION LTD COM',
          'orderAction': 'BUY_OPEN',
          'quantityType': 'QUANTITY',
          'orderedQuantity': 5,
          'filledQuantity': 5,
          'averageExecutionPrice': 0,
          'estimatedCommission': 9.99,
          'estimatedFees': 0,
          'Product': {
            'symbol': 'RIMM',
            'securityType': 'OPTN',
            'callPut': 'CALL',
            'expiryYear': 2012,
            'expiryMonth': 3,
            'expiryDay': 9,
            'strikePrice': 12,
            'productId': {
              'symbol': 'RIMM'}}}]}]
    }, {
      'orderId': 477,
      'details': 'https://api.etrade.com/accounts/E5Nd4LJBsEi_UyHm4Vio9g/orders/477',
      'orderType': 'ONE_CANCELS_ALL',
      'totalOrderValue': 209.99,
      'totalCommission': 10.74,
      'OrderDetail': [{
        'orderNumber': 1,
        'placedTime': 1331699203122,
        'orderValue': 123.0,
        'status': 'OPEN',
        'orderTerm': 'GOOD_FOR_DAY',
        'priceType': 'LIMIT',
        'limitPrice': 2,
        'stopPrice': 0,
        'marketSession': 'REGULAR',
        'bracketedLimitPrice': 2,
        'initialStopPrice': 2,
        'allOrNone': False,
        'netPrice': 0,
        'netBid': 0,
        'netAsk': 0,
        'gcd': 0,
        'ratio': '',
        'Instrument': [{
          'symbolDescription': 'ETRADE Financials',
          'orderAction': 'BUY',
          'quantityType': 'QUANTITY',
          'orderedQuantity': 100,
          'filledQuantity': 0,
          'averageExecutionPrice': 0,
          'estimatedCommission': 9.99,
          'estimatedFees': 0,
          'Product': {
            'symbol': 'ETFC',
            'securityType': 'EQ',
            'productId': {
              'symbol': 'ETFC'}}}]
      }, {
        'orderNumber': 2,
        'placedTime': 1331699203,
        'orderValue': 231.0,
        'status': 'OPEN',
        'orderTerm': 'GOOD_FOR_DAY',
        'priceType': 'LIMIT',
        'limitPrice': 0.5,
        'stopPrice': 0,
        'marketSession': 'REGULAR',
        'initialStopPrice': 0.5,
        'allOrNone': False,
        'netPrice': 0,
        'netBid': 0,
        'netAsk': 0,
        'gcd': 0,
        'ratio': '',
        'Instrument': [{
          'symbolDescription': "MON Mar 9 '12 $85 Call",
          'orderAction': 'BUY_OPEN',
          'quantityType': 'QUANTITY',
          'orderedQuantity': 1,
          'filledQuantity': 0,
          'averageExecutionPrice': 0,
          'estimatedCommission': 9.99,
          'estimatedFees': 0,
          'Product': {
            'symbol': 'MON',
            'securityType': 'OPTN',
            'callPut': 'CALL',
            'expiryYear': 2012,
            'expiryMonth': 4,
            'expiryDay': 21,
            'strikePrice': 85,
            'productId': {
              'symbol': 'MON'}}}]}]
    }, {
      'orderId': 475,
      'details': 'https://api.etrade.com/accounts/E5Nd4LJBsEi_UyHm4Vio9g/orders/475',
      'orderType': 'SPREADS',
      'OrderDetail': [{
        'placedTime': 1331742953,
        'executedTime': 1331742955432,
        'orderValue': 4445.99,
        'status': 'EXECUTED',
        'orderTerm': 'GOOD_FOR_DAY',
        'priceType': 'NET_DEBIT',
        'limitPrice': 1.5,
        'stopPrice': 0,
        'marketSession': 'REGULAR',
        'allOrNone': False,
        'netPrice': 0,
        'netBid': 0,
        'netAsk': 0,
        'gcd': 0,
        'ratio': '',
        'Instrument': [{
          'symbolDescription': "REE Jul 21 '12 $7 Call",
          'orderAction': 'BUY_OPEN',
          'quantityType': 'QUANTITY',
          'orderedQuantity': 2,
          'filledQuantity': 2,
          'averageExecutionPrice': 1.5,
          'estimatedCommission': 7.24,
          'estimatedFees': 0,
          'Product': {
            'symbol': 'REE',
            'securityType': 'OPTN',
            'callPut': 'CALL',
            'expiryYear': 2012,
            'expiryMonth': 7,
            'expiryDay': 21,
            'strikePrice': 7,
            'productId': {
              'symbol': 'REE'}}
        }, {
          'symbolDescription': "REE Jan 19 '13 $12.50 Put",
          'orderAction': 'BUY_OPEN',
          'quantityType': 'QUANTITY',
          'orderedQuantity': 2,
          'filledQuantity': 2,
          'averageExecutionPrice': 1.5,
          'estimatedCommission': 7.24,
          'estimatedFees': 0,
          'Product': {
            'symbol': 'REE',
            'securityType': 'OPTN',
            'callPut': 'PUT',
            'expiryYear': 2013,
            'expiryMonth': 1,
            'expiryDay': 19,
            'strikePrice': 12.5,
            'productId': {
              'symbol': 'REE'}}}]}]}]}}