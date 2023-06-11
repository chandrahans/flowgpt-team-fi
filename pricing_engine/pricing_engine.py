from bid_ask_spread_handler import BidAskSpreadHandler
from currency_rate_converter import CurrencyRateConverter
from market_volatility_monitor import MarketVolatilityMonitor
from positions_handler import PositionsHandler
from skew_handler import SkewCalculator
from theoretical_price_handler import TheoreticalPriceHandler
from yahoo_ticker_resolver import YahooTickerResolver 

DEFAULT_SPREAD_BPS = 100
CONST_TEN_THOUSAND = 10000

# RFQ data should come here with ticker, sides, and quantity
# and quoteType (it can be RISK or NAV)

one_sided_quote_sides_list = ['buy','sell']
two_sided_quote_sides_list = ['two_way']

one_sided_quote_sides_list = ['buy','sell']
two_sided_quote_sides_list = ['two_way']

positions_handler = PositionsHandler()
class PricingEngine:

    def __init__(self,ticker,quantity,side,quote_type,sentiment=1,counterparty='unknown'):
        ticker = YahooTickerResolver(ticker).retrieve_yahoo_ticker() 
        theo = TheoreticalPriceHandler(ticker).theo_price
        print(theo)
        if theo is None:
            print(f"Unable to retrieve a theo price for {ticker}.")
            return

        bid_ask_price_spread = BidAskSpreadHandler(ticker).bid_ask_spread
        if bid_ask_price_spread is None:
            bid_ask_price_spread = DEFAULT_SPREAD_BPS*theo/CONST_TEN_THOUSAND
            print(f"Unable to retrieve a bid_ask price for {ticker}, defaulting to {DEFAULT_SPREAD_BPS}")

        if side.lower() in one_sided_quote_sides_list:
            number_of_sides = 1
        elif side.lower() in two_sided_quote_sides_list:
            number_of_sides = 2

        position_to_ticker_limit_ratio = positions_handler.get_position_limit_ratio(ticker)
        notional_order_value = quantity*theo
        market_volatility_monitor = MarketVolatilityMonitor()
        global_market_conditions = market_volatility_monitor.get_market_volatility()

        skew_calculator = SkewCalculator(counterparty=counterparty,
                                 market_conditions=global_market_conditions,
                                 order_value=notional_order_value,
                                 sentiment=sentiment,
                                 number_of_sides=number_of_sides,
                                 positions_to_limit_ratio=position_to_ticker_limit_ratio)

        bid_skew = skew_calculator.bid_skew 
        ask_skew = skew_calculator.ask_skew

        bid_price = self.calculate_bid_price(theo,bid_skew,bid_ask_price_spread)
        ask_price = self.calculate_ask_price(theo,ask_skew,bid_ask_price_spread)

        self.bid_price_skew_bps = self.calculate_bid_skew_bps(bid_price,theo)
        self.ask_price_skew_bps = self.calculate_ask_skew_bps(ask_price,theo)

        currency_rate_converter = CurrencyRateConverter(from_currency='USD',
                                                        to_currency='EUR')
        exchange_rate = currency_rate_converter.get_exchange_rate()
        self.bid_price = round(bid_price*exchange_rate,2)
        self.ask_price = round(ask_price*exchange_rate,2)
      
        if quote_type in ['RISK','CASH']:
            print("bid: " + str(self.bid_price) + " ask: "+ str(self.ask_price))

        if quote_type == "NAV":
            print("NAV -" + str(self.bid_price_skew_bps) + "bps, NAV +" + str(self.ask_price_skew_bps)+"bps")

    def calculate_bid_price(self, theo, bid_skew, bid_ask_price_spread):
        bid_price = theo - bid_skew*bid_ask_price_spread
        return bid_price

    def calculate_ask_price(self, theo, ask_skew, bid_ask_price_spread):
        ask_price = theo + ask_skew*bid_ask_price_spread
        return ask_price

    def calculate_bid_skew_bps(self,bid_price,theo):
        self.bid_price_skew_bps = round((theo-bid_price)/theo*CONST_TEN_THOUSAND,2)
        return self.bid_price_skew_bps

    def calculate_ask_skew_bps(self,ask_price,theo):
        self.ask_price_skew_bps = round((ask_price-theo)/theo*CONST_TEN_THOUSAND,2)
        return self.ask_price_skew_bps

    def get_bid_price(self, x):
        return self.bid_price

    def get_ask_price(self, x):
        return self.ask_price

    def get_bid_price_skew_bps(self, x):
        return self.bid_price_skew_bps

    def get_ask_price_skew_bps(self, x):
        return self.ask_price_skew_bps
