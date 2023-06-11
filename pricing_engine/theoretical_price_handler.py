import requests

class TheoreticalPriceHandler:

    def __init__(self, ticker):
        self._ticker = ticker 
        self._url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        self._user_agent_key = "User-Agent"
        self._user_agent_value = "Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.theo_price = self.get_yahoo_price()

    def get_yahoo_price(self):
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
        if data['chart']['result'] is None:
            print(f"No data found for {self._ticker}")
            return None
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        return price
