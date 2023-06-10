import json

import openai
from dataclasses import dataclass


@dataclass
class TickerSentiment:
    ticker = ""
    sentiment = 0


class TickerSentimentAnalyser:
    def __init__(self, config):
        openai.api_key = config['OPENAI']['api-key']

    def analyse_text(self, text, model="gpt-3.5-turbo"):
        content = f"""If text in square brackets is related to some financial instrument or multiple financial
        instruments like stock, cryptocurrency, 
        FX output me the ticker in the format how it is listed on exchange and analysis on 
        how positive is the financial sentiment of the text on the scale 0 to 9 where 0 is price of the subject will 
        probably go down and 9 price of the subject will probably go up for each of them. Here is the text:
        [{text}]
        Respond only in JSON format with list of all the instruments you found and sentiments for each. Like this:
        {{
            "result": [
                {{"ticker": <First instrument ticker>, "sentiment": 0}}
                {{"ticker": <Second instrument ticker>, "sentiment": 7}}
            ]
        }}
        """

        try:
            messages = [{"role": "user", "content": content}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0,
                timeout=10
            )
            js = json.loads(response.choices[0].message["content"])
            result = []
            for itm in js['result']:
                ts = TickerSentiment()
                ts.ticker = itm['ticker']
                ts.sentiment = itm['sentiment']
                result.append(ts)
            return result
        except Exception as e:
            return None

