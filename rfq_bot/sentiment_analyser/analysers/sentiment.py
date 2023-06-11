import json

import openai
from dataclasses import dataclass


class SentimentAnalyser:
    def __init__(self, config):
        openai.api_key = config['OPENAI']['api-key']

    def analyse_text(self, text, model="gpt-3.5-turbo"):
        content = f"""Analyse the text in square brackets on 
        how positive is the financial sentiment of the text on the scale 0 to 9 where 0 is price of the subject will 
        probably go down and 9 price of the subject will probably go up for each of them. Here is the text:
        [{text}]
        Respond only with number 0 to 9.
        """

        try:
            messages = [{"role": "user", "content": content}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0,
                timeout=10
            )
            return int(response.choices[0].message["content"])
        except Exception as e:
            return None

