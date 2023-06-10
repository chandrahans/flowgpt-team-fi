from theoretical_price_handler import TheoreticalPriceHandler

class MarketVolatilityMonitor:
    
    def __init__(self):
        self.volatility_index_str = "^VIX" 
        self.default_vix_level= 17
   
    def get_vix_level(self):
        try:
            self.vix_level = TheoreticalPriceHandler("^VIX").theo_price
        except Exception as e:
            self.vix_level = self.default_vix_level
        return self.vix_level

    def get_market_volatility(self):
        vix_level = self.get_vix_level()
        if vix_level < 13:
            return "very_calm"
        elif vix_level >= 13 and vix_level < 19:
            return "calm"
        elif vix_level >= 19 and vix_level< 28: 
            return "volatile"
        else:
            return "very_volatile"
 
        
