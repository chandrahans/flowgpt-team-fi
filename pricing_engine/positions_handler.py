class PositionsHandler:

    def __init__(self):
        self.current_positions = {'AMZN':0,
                                  'TSLA':0,
                                  'MSFT':0,
                                  'BTC-EUR':0,
                                  'EURUSD=X':0,
                                  'SGDUSD=X':0,  
                                  'SPY':0}

        self.positions_limits = {'AMZN':100,
                                 'TSLA':100,
                                 'MSFT':10,
                                 'BTC-EUR':10,
                                 'EURUSD=X':10,
                                 'SGDUSD=X':10} 
 
        self.default_position_limit = 10
    
    def change_position(self,ticker,quantity):
        if ticker not in self.current_positions:
            self.current_positions[ticker] = quantity
        self.current_positions[ticker] += quantity

    def get_all_positions(self):
        return self.current_positions

    def get_all_positions_limits(self):
        return self.positions_limits

    def get_position(self,ticker):
        if ticker not in self.current_positions:
            return 0
        return self.current_positions[ticker]

    def get_position_limit_ratio(self,ticker):
        if ticker not in self.current_positions:
            return 0
        ticker_quantity = self.current_positions[ticker]
        position_limit = self.default_position_limit
        if ticker not in self.positions_limits:
            position_limit = self.default_position_limit
        else:
            position_limit = self.positions_limits[ticker]
        if position_limit == 0 or abs(ticker_quantity)>=position_limit:
            position_limit_ratio = 1
        else:
            position_limit_ratio = ticker_quantity/position_limit
        return position_limit_ratio
