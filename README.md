# RFQ Bot Alpha

RFQ Bot Alpha is a Telegram bot built using OpenAI's ChatGPT-4. The bot is designed to automatically respond to RFQ (Request for Quote) requests. Currently in its Alpha version, the bot can be run from the console using Python.

## Prerequisites

- Python 3.7 and above
- An API Key for Telegram
- An API Key for OpenAI (for accessing ChatGPT)
- An API Key for OpenAI-4 

## Installation

Before running the script, you need to install the required packages. Run the following command:

```shell
pip install -r requirements.txt
```

## Configuration

Before you run the RFQ Bot, you will need to set up a configuration file in the following format:

\`\`\`ini
[TELEGRAM]
api-key = Your-Telegram-API-Key

[OPENAI]
api-key = Your-OpenAI-API-Key

[OPENAI-4]
api-key = Your-OpenAI-4-API-Key
\`\`\`

Please replace \`Your-Telegram-API-Key\`, \`Your-OpenAI-API-Key\` and \`Your-OpenAI-4-API-Key\` with your actual keys. Save this configuration file as \`configuration.ini\`.

## Running the Bot

Once you have set up your \`configuration.ini\` file, you can run the bot using the following command:

\`\`\`shell
python -m rfq_bot ./configuration.ini
\`\`\`

## Contributions

This project is currently in Alpha, and contributions are welcome. Feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

RFQ Bot is open-source software licensed under the [Apache License 2.0](LICENSE).

## Contact

For any queries or concerns regarding the bot, please open an issue on this GitHub repository.