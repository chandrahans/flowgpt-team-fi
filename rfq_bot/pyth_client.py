import asyncio

from pythclient.pythclient import PythClient
from pythclient.pythaccounts import PythPriceAccount
from pythclient.utils import get_key


async def main() -> None:
    solana_network = "devnet"
    async with PythClient(
            first_mapping_account_key=get_key(solana_network, "mapping"),
            program_key=None,
    ) as c:
        await c.refresh_all_prices()
        products = await c.get_products()
        for p in products:
            print(p.attrs)
            prices = await p.get_prices()
            for _, pr in prices.items():
                print(
                    pr.price_type,
                    pr.aggregate_price_status,
                    pr.aggregate_price,
                    "p/m",
                    pr.aggregate_price_confidence_interval,
                )


if __name__ == '__main__':
    asyncio.run(main())