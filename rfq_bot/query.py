import asyncio
import os
import time
import openai
from enum import Enum
import json
import configparser
import sys

API_KEY = os.getenv("OPENAI_API_KEY")
API_4_KEY = os.getenv("OPENAI_4_API_KEY")


class Quote(Enum):
    BID = 1,
    ASK = 2,
    BOTH = 3,
    SWAP = 4


class Denomination(Enum):
    INSTRUMENT = 1,
    USD = 2,
    EUR = 3,
    GBP = 4


class PriceType(Enum):
    SPOT = 1,
    NAV = 2,
    TWAP = 3,
    VWAP = 4


class Query():
    @classmethod
    def from_json(cls, params):
        if params["Instrument"] == "Unspecified":
            return None

        quote = Quote.BOTH
        if params["Quote"] == "Bid":
            quote = Quote.BID
        elif params["Quote"] == "Ask":
            quote = Quote.ASK

        price_type = PriceType.SPOT
        if params["PriceType"] == "NAV":
            price_type = PriceType.NAV
        elif params["PriceType"] == "TWAP":
            price_type = PriceType.TWAP
        elif params["PriceType"] == "VWAP":
            price_type = PriceType.VWAP

        denomination = Denomination.INSTRUMENT
        if params["Denomination"] == "USD":
            denomination = Denomination.USD
        elif params["Denomination"] == "EUR":
            denomination = Denomination.EUR
        elif params["Denomination"] == "GBP":
            denomination = Denomination.GBP

        return cls(params["Instrument"], params["Quantity"], denomination, quote, price_type)

    def __init__(
        self,
        instrument: str,
        quantity: float,
        denomination: Denomination = Denomination.INSTRUMENT,
        quote: Quote = Quote.BOTH,
        price_type: PriceType = PriceType.SPOT
    ):
        self.instrument = instrument
        self.quantity = quantity
        self.denomination = denomination
        self.quote = quote
        self.price_type = price_type

    def __repr__(self) -> str:
        return f'Instrument: {self.instrument}, Quantity: {self.quantity}, Denomination: {self.denomination} Quote: {self.quote}, PriceType: {self.price_type}'


class QueryHandler:
    def __init__(self, config, verbose: bool = False) -> None:
        self.verbose = verbose
        openai.api_key = config['OPENAI-4']['api-key']

    def parse(self, raw_query: str) -> Query:
        content = f'We received a query from a client intending to make a trade in a financial instrument.\
                The client might be looking for a Bid, Ask (Offer) or Both for the financial instrument.\
                Your task is to extract the details of the tarding intention, namely, the financial instrument specified, \
                whether they are looking for a Bid or Offer or Both, and the required Quantity \
                from the query inside triple quotes: """{raw_query}""".\
                The client might be looking for a price against (or interms of) NAV, TWAP or VWAP.\
                If the client wants to buy an instrument, they are looking for an offer on that instrument.\
                Similarly, if the client wants to sell, they are looking for a bid on that instrument.\
                Also, if the client wants to swap some amount of A to B, they are looking for a Bid on the instrument A/B.\
                The client might also be using trading slang. For example, if the query mentions 2w or 2way quote, \
                it usually means they are looking for Both Bid and Ask on that instrument.\
                The denomination for the query is usually the instrument itself, but sometimes the query could \
                specify a currency as well. Typically, the denomination currencies could be are USD($), EUR(€), GBP(£) etc.\
                Respond in a strict JSON format with Instrument, Denomination, PriceType, Quantity and Quote as keys,\
                with following constraints on possible values:\n\
                \t PriceType: NAV, SPOT, TWAP, VWAP and Unspecified\n\
                \t Quote: Bid, Ask, Both, and Unspecified.\n\
                \t Denomination: USD, EUR, GBP, and Unspecified'

        messages = [{"role": "user", "content": content}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0)

        if self.verbose:
            print(f'Model response: {response.choices[0].message["content"]}')
        try:
            return Query.from_json(json.loads(response.choices[0].message["content"]))
        except Exception as e:
            if self.verbose:
                print(
                    f"Exception {e} occured while handling the query: {raw_query}")
            return None


def _main():
    raw_querries = [
        "2w 500 BTC",
        "Can I have an offer in 10 BTC",
        "Id like to buy 20 BTC",
        "NAV 2w 20 BTCE GY todays NAV settlement t+2",
        "Can i have a 2way in 10,000,000$ BTC",
        "Can i have 2w 10000 BTC against 1d twap",
        "What can you show 2w 10000 BTC against 1d vwap",
        "I would like to swap 1,000,000 $ BTC to ETH",
        "I wanna sell 1,000,000 € BTC",
        "Can I get a quote please, I want to sell 1,000,000 Pounds worth of BTC",
    ]

    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    query_handler = QueryHandler(config)

    for r in raw_querries:
        print(f"Raw query: {r}")
        query = query_handler.parse(r)
        print(f"Formatted query: {query}")
        time.sleep(5)


if __name__ == "__main__":
    _main()
