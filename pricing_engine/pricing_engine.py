from bid_ask_spread_handler import BidAskSpreadHandler
from positions_handler import PositionsHandler
from skew_handler import SkewCalculator
from theoretical_price_handler import TheoreticalPriceHandler

DEFAULT_SPREAD_BPS = 100
maximum_bid_skew = 2.5
maximum_ask_skew = 2.5

# RFQ data should come here with ticker, sides, and quantity
# and quoteType (it can be RISK or NAV)
# optional field counterparty

positions_handler = PositionsHandler()
class PricingEngine:

    def __init__(self,ticker,quantity,side,quote_type,counterparty='unknown'):
        theo = TheoreticalPriceHandler(ticker).theo_price
        if theo is None:
            print(f"Unable to retrieve a theo price for {ticker}.")

        bid_ask_price_spread = BidAskSpreadHandler(ticker).bid_ask_spread
        if bid_ask_price_spread is None:
            bid_ask_price_spread = DEFAULT_SPREAD_BPS
            print(f"Unable to retrieve a bid_ask price for {ticker}, defaulting to {DEFAULT_SPREAD_BPS}")

        if side.lower() in ['buy','sell']:
            number_of_sides = 1
        else:
            number_of_sides = 2
        position_to_ticker_limit_ratio = positions_handler.get_position_limit_ratio(ticker)
        notional_order_value = quantity*theo

        skew_calculator = SkewCalculator(counterparty="unknown",
                                 market_conditions="volatile",
                                 order_value=notional_order_value,
                                 sentiment=1,
                                 number_of_sides=1,
                                 positions_to_limit_ratio=position_to_ticker_limit_ratio)

        bid_skew = skew_calculator.bid_skew 
        ask_skew = skew_calculator.ask_skew
        bid_skew = min(maximum_bid_skew,bid_skew)
        ask_skew = min(maximum_ask_skew,ask_skew)
        bid_price = theo - bid_skew*bid_ask_price_spread
        ask_price = theo + ask_skew*bid_ask_price_spread

        ask_price_skew_bps = round((ask_price-theo)/theo*10000,2)
        bid_price_skew_bps = round((theo-bid_price)/theo*10000,2)

        self.bid_price = round(bid_price,2)
        self.ask_price = round(ask_price,2)  ###can make safe ticksizerounding here	
      
        if quote_type in ['RISK','CASH']:
            print("bid: " + str(self.bid_price) + " ask: "+ str(self.ask_price))

        if quote_type == "NAV":
            print("NAV: -"+str(bid_price_skew_bps) + "bps, NAV " + str(ask_price_skew_bps)+"bps")

        def get_bid_price(x):
            return self.bid_price

        def get_ask_price(x):
            return self.ask_price

