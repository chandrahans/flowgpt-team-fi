import requests

class BidAskSpreadHandler:

    def __init__(self, ticker):
        self._ticker = ticker
        self._url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=summaryDetail"
        self._user_agent_key = "User-Agent"
        self._user_agent_value = "Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.bid_ask_spread = self.get_yahoo_bid_ask_spread()

    def get_yahoo_bid_ask_spread(self):
        url = self._url
        headers = {
            self._user_agent_key: self._user_agent_value
        }
        
        try:
            response = requests.get(url, headers=headers)
        except:
            print(f"Could not complete API request for {self._ticker}")
            return None

        if response.status_code != requests.codes.ok:
            print(f"No data found for {self._ticker}")
            return None
        data = response.json()
        if not data['quoteSummary']['result']:
            print(f"Security not available {self._ticker}!")
            return None
        ask_dict = data['quoteSummary']['result'][0]['summaryDetail']['ask']
        bid_dict = data['quoteSummary']['result'][0]['summaryDetail']['bid']
        if not ask_dict or not bid_dict:
            print("Could not find bid and ask prices.")
            return None 
        ask_price = ask_dict['raw']
        bid_price = bid_dict['raw']
        if bid_price == 0 or ask_price == 0:
            print("One of the bid/ask prices is zero")
            return None 
        if ask_price <= bid_price:
            print("Sommething went wrong with the prices")
        self.bid_ask_spread = ask_price - bid_price
        return self.bid_ask_spread
