from theoretical_price_handler import TheoreticalPriceHandler

class CurrencyRateConverter:
   
    def __init__(self,from_currency,to_currency):
        self.from_currency = from_currency
        self.to_currency = to_currency
        pair_name_string = from_currency + to_currency +"=X"
        self.exchange_rate = TheoreticalPriceHandler(pair_name_string).theo_price
   
    def get_exchange_rate(self):
        return self.exchange_rate
