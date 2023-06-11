# Responsible for calculating the price skew.
# The following factors are used in skewing:
# counterparty: "good", "neutral", "toxic"  
# current market_conditions  ("Very Calm","Calm","Volatile","Extremely Volatile") 
# notional value of the RFQ
# current market volatility
# sentiment related to instrument
# hedging costs (add x bps) to spread/configurable 
# current position 

maximum_bid_skew = 4.5
maximum_ask_skew = 4.5
neutral_counterparty_multiplier = 1
toxic_counterparty_multiplier = 1.5
good_counterparty_multiplier = 0.5
very_calm_market_conditions_multiplier = 0.3 
calm_market_conditions_multiplier = 1 
volatile_market_conditions_multiplier = 2
very_volatile_market_conditions_multiplier = 2.5 
low_value_multiplier = 1.2
medium_value_multiplier = 1
high_value_multiplier = 5.2
strong_buy_bid_multiplier = 0.1 
buy_bid_multiplier = 0.5
neutral_bid_multiplier = 1
sell_bid_multiplier = 2.25
strong_sell_bid_multiplier = 4.5
strong_buy_ask_multiplier = 4.5 
buy_ask_multiplier = 2.25
neutral_ask_multiplier = 1
sell_ask_multiplier = 0.75
strong_sell_ask_multiplier = 0.1
one_sided_multiplier = 1
two_sided_multiplier = 1.1
counterparty_dict = {'Flow Traders':'good',
                     'Max Kalinin Inc':'neutral',
                     'Alexandru Paraschiv Capital':'toxic'}

hedging_costs_default = 1
hedging_costs_per_instrument_bps = {'AMZN':1,
				    'MSFT':1}

big_long_position_bid_multiplier = 2
small_long_position_bid_multiplier = 1.25  
neutral_position_bid_multiplier = 1
small_short_position_bid_multiplier = 0.5
big_short_position_bid_multiplier = 0.25
big_long_position_ask_multiplier = 0.25
small_long_position_ask_multiplier = 0.5  
neutral_position_ask_multiplier = 1
small_short_position_ask_multiplier = 1.25
big_short_position_ask_multiplier = 2

class SkewCalculator:
    def __init__(self,
                 counterparty,
                 market_conditions,
                 order_value,
                 sentiment,
                 number_of_sides,
                 positions_to_limit_ratio):

        self.counterparty_multiplier = self.get_counterparty_multiplier(counterparty)
        self.market_conditions = self.get_market_conditions_multiplier(market_conditions)
        self.order_value_multiplier = self.get_order_value_multiplier(order_value)
        self.sentiment_multiplier = self.get_sentiment_multiplier(sentiment)
        self.sides_multiplier = self.get_sided_multiplier(number_of_sides)
        self.position_multiplier = self.get_current_position_multiplier(positions_to_limit_ratio)
    
        self.two_sided_multiplier = self.counterparty_multiplier*self.market_conditions*self.order_value_multiplier*self.sides_multiplier
        self.bid_skew = self.two_sided_multiplier*self.sentiment_multiplier[0]*self.position_multiplier[0]
        self.bid_skew = min(maximum_bid_skew,self.bid_skew)
        self.ask_skew = self.two_sided_multiplier*self.sentiment_multiplier[1]*self.position_multiplier[1]
        self.ask_skew = min(maximum_ask_skew,self.ask_skew)
        self.ask_skew = self.two_sided_multiplier*self.sentiment_multiplier[1]*self.position_multiplier[1]

    def get_bid_skew(self):
        return self.bid_skew
    
    def get_ask_skew(self):
        return self.ask_skew

    def get_counterparty_multiplier(self, counterparty='unknown'):
        if counterparty not in counterparty_dict:
            return neutral_counterparty_multiplier
        if counterparty_dict[counterparty] =='good':
            return good_counterparty_multiplier
        if counterparty_dict[counterparty]=='toxic':
            return toxic_counterparty_multiplier
        if counterparty_dict[counterparty]=='neutral':
            return neutral_counterparty_multiplier
        return neutral_counterparty_multiplier

    def get_market_conditions_multiplier(self,market_conditions='very volatile'):
        if market_conditions=='very_volatile':
            return very_volatile_market_conditions_multiplier
        if market_conditions=='volatile':
            return volatile_market_conditions_multiplier
        if market_conditions=='calm':
            return calm_market_conditions_multiplier
        if market_conditions=='very_calm':
            return very_calm_market_conditions_multiplier
        return calm_market_conditions_multiplier

    def get_order_value_multiplier(self,order_value_euros):
        if order_value_euros < 100000:
            return low_value_multiplier
        elif order_value_euros >= 1000000 and order_value_euros <= 1000000:
            return medium_value_multiplier
        else:
           return high_value_multiplier

    def get_sentiment_multiplier(self, sentiment):
        if sentiment<0 or sentiment>10 or sentiment is None:
            return (1,1)
        if sentiment in [0,1]:
            return strong_sell_bid_multiplier,strong_sell_ask_multiplier
        if sentiment in [2,3]:
            return sell_bid_multiplier,sell_ask_multiplier
        if sentiment in [4,5]:
            return neutral_bid_multiplier,neutral_ask_multiplier
        if sentiment in [6,7]:
            return buy_bid_multiplier,buy_ask_multiplier
        if sentiment in [8,9]:
            return strong_buy_bid_multiplier,strong_buy_ask_multiplier

    def get_sided_multiplier(self, number_of_sides):
        if number_of_sides == 2:
            return two_sided_multiplier
        return one_sided_multiplier

    def get_current_position_multiplier(self, position_to_limit_ratio):
        if position_to_limit_ratio < -0.8:
            return big_short_position_bid_multiplier,big_short_position_ask_multiplier
        if position_to_limit_ratio >= -0.8 and position_to_limit_ratio < -0.5:
            return small_short_position_bid_multiplier,small_short_position_ask_multiplier
        if position_to_limit_ratio >= -0.5 and position_to_limit_ratio < 0.5:
           return neutral_position_bid_multiplier,neutral_position_ask_multiplier
        if position_to_limit_ratio >= 0.5 and position_to_limit_ratio < 0.8:
           return small_long_position_bid_multiplier,small_long_position_ask_multiplier
        if position_to_limit_ratio >= 0.8:
           return big_long_position_bid_multiplier,big_long_position_ask_multiplier

