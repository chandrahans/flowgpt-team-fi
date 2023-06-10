import asyncio
import os
from pickle import NONE
import openai
from enum import Enum
import json
import requests

API_KEY = "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"
openai.api_key = API_KEY


def fine_tune_model(prompt, dataset, model_engine="davinci", num_epochs=3, batch_size=4):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    data = {"model": f"{model_engine}-0",
            "dataset": dataset,
            "prompt": prompt,
            "num_epochs": num_epochs,
            "batch_size": batch_size
            }

    url = "https://api.openai.com/v1/fine-tunes"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise ValueError("Failed to fine-tune the model.")

    model_id = response.json()["model_id"]
    return model_id


class Side(Enum):
    BUY = 1,
    SELL = 2,
    BOTH = 3


class Type(Enum):
    CASH = 1,
    NAV = 2


class Query():
    @classmethod
    def from_json(cls, params):
        side = Side.BOTH
        if params["Action"] == "Buy":
            side = Side.BUY
        elif params["Action"] == "Sell" or params["Action"] == "Offer":
            side = Side.SELL

        type = Type.NAV if params["Type"] == "NAV" else Type.CASH
        return cls(params["Instrument"], params["Quantity"], side, type)

    def __init__(
        self,
        instrument: str,
        quantity: int,
        side: Side = Side.BOTH,
        type: Type = Type.CASH
    ):
        self.instrument = instrument
        self.quantity = quantity
        self.side = side
        self.type = type

    def __repr__(self) -> str:
        return f'Instrument: {self.instrument}, Quantity: {self.quantity}, Side: {self.side}, Type: {self.type}'


def get_proper_query(query, model="gpt-3.5-turbo") -> Query:
    content = f'We received query from a client intending to make a trade in a financial instrument.\
                The instument could either be of NAV or Cash type.\
                The client might want to buy, sell or do both for the financial instrument.\
                The client might also be using slang terms typically used in the trading community. \
                For example bidding usually means buying, offering means selling etc.\
                It might be worthwhile to look up Investopedia for the tarding slang and jargon.\
                Your task is to extract the details of the tarding intention, namely, the financial instrument specified, \
                whether they want to buy or sell, and the required quantity \
                from the query inside triple quotes: """{query}""".\
                Respond in JSON format with Instrument, Type, Quantity and Action as keys,\
                where the Type is an enumeration among NAV, Cash and Unspecified,\
                and the Action is an enumeration among Buy, Sell, Both and Unspecified'

    messages = [{"role": "user", "content": content}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
        timeout=10
    )
    print(f'Response from the model: {response.choices[0].message["content"]}')
    return Query.from_json(json.loads(response.choices[0].message["content"]))


def _main():
    request = "Can i have a 2way in 10,000,000$ BTC"
    query = get_proper_query(request)
    print(query)


if __name__ == "__main__":
    _main()