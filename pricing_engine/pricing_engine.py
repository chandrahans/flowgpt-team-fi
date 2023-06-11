from enum import Enum
import math
from pricing_engine.bid_ask_spread_handler import BidAskSpreadHandler
from pricing_engine.currency_rate_converter import CurrencyRateConverter
from pricing_engine.market_volatility_monitor import MarketVolatilityMonitor
from pricing_engine.positions_handler import PositionsHandler
from pricing_engine.skew_handler import SkewCalculator
from pricing_engine.theoretical_price_handler import TheoreticalPriceHandler
from pricing_engine.yahoo_ticker_resolver import YahooTickerResolver 
from rfq_bot.query import Query, Quote, Denomination, PriceType

DEFAULT_SPREAD_BPS = 100
CONST_TEN_THOUSAND = 10000

one_sided_quote_sides_list = ['buy','sell']
two_sided_quote_sides_list = ['two_way']

positions_handler = PositionsHandler()

def resolve_denomination(denomination):
    if denomination.value == Denomination.INSTRUMENT.value:
        return "instrument"
    if denomination.value == Denomination.USD.value:
        return "USD"
    if denomination.value == Denomination.EUR.value:
        return "EUR"
    if denomination.value == Denomination.GBP.value:
        return "GBP"

def resolve_side(quote): 
    cpty_side = "TWO_WAY"
    if quote.value ==  Quote.BID.value:
       cpty_side = "SELL"
    elif quote.value ==  Quote.ASK.value:
       cpty_side = "BUY"
    elif quote.value == quote.BOTH.value:
       cpty_side = "TWO_WAY" 
    return cpty_side

def resolve_quote_type(price_type):
    if price_type.value == PriceType.SPOT.value:
        price_type = "RISK"
    elif price_type.value == PriceType.NAV.value:
        price_type = "NAV"
    elif price_type.value == PriceType.TWAP.value:
        price_type = "TWAP"
    elif price_type.value == PriceType.VWAP.value:
       price_type = "VWAP"
    return price_type
     
class PricingEngine:

    def __init__(self,query,ticker="AAPL",quantity=1,side="BUY",quote_type="RISK",sentiment=1,counterparty='unknown'):

        ticker = query.instrument
        quantity = query.quantity
        denomination = resolve_denomination(query.denomination)
        side = resolve_side(query.quote)
        quote_type = resolve_quote_type(query.price_type)
        self.cpty_side = side
        self.quote_type = quote_type
      
        ticker = YahooTickerResolver(ticker).retrieve_yahoo_ticker()
        theo = TheoreticalPriceHandler(ticker).theo_price
        if theo is None:
            print(f"Unable to retrieve a theo price for {ticker}.")
            self.final_output = f"We don't quote {ticker} unfortunately :(."
            return
        if denomination == "USD":
           quantity = math.floor(quantity/theo)

        if denomination == "EUR":
           currency_rate_converter = CurrencyRateConverter(from_currency='EUR',
                                                        to_currency='USD')
           exchange_rate = currency_rate_converter.get_exchange_rate()
           quantity = math.floor(exchange_rate * quantity/theo)

        if denomination == "GBP":
           currency_rate_converter = CurrencyRateConverter(from_currency='GBP',
                                                        to_currency='USD')
           exchange_rate = currency_rate_converter.get_exchange_rate()
           quantity = math.floor(exchange_rate * quantity/theo)

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
        
        if self.quote_type == "RISK":
            if self.cpty_side == "BUY":
                self.final_output = f"offer: {self.ask_price}"
            elif self.cpty_side == "SELL":
                self.final_output = f"bid: {self.bid_price}"
            elif self.cpty_side == "TWO_WAY":
                self.final_output = f"bid: {self.bid_price}, offer {self.ask_price}"
        else:
            if self.cpty_side == "BUY":
                self.final_output = f"offer: +{self.ask_price_skew_bps} bps"
            elif self.cpty_side == "SELL":
                self.final_output = f"bid: {self.quote_type} - {self.bid_price_skew_bps} bps"
            elif self.cpty_side == "TWO_WAY":
                self.final_output = f"bid: {self.quote_type} - {self.bid_price_skew_bps} bps, offer {self.quote_type} +{self.ask_price_skew_bps} bps"

    def calculate_bid_price(self, theo, bid_skew, bid_ask_price_spread):
        bid_price = theo - bid_skew*bid_ask_price_spread
        return bid_price

    def calculate_ask_price(self, theo, ask_skew, bid_ask_price_spread):
        ask_price = theo + ask_skew*bid_ask_price_spread
        return ask_price

    def calculate_bid_skew_bps(self,bid_price,theo):
        self.bid_price_skew_bps = round((theo-bid_price)/theo*CONST_TEN_THOUSAND,0)
        return self.bid_price_skew_bps

    def calculate_ask_skew_bps(self,ask_price,theo):
        self.ask_price_skew_bps = round((ask_price-theo)/theo*CONST_TEN_THOUSAND,0)
        return self.ask_price_skew_bps

    def get_bid_price(self):
        return self.bid_price

    def get_ask_price(self):
        return self.ask_price

    def get_bid_price_skew_bps(self):
        return self.bid_price_skew_bps

    def get_ask_price_skew_bps(self):
        return self.ask_price_skew_bps

    def __str__(self):
        return self.final_output


