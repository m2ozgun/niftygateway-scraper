import asyncio
import aiohttp
import datetime
import pandas as pd
import sys
from itertools import cycle

from utils import search_headers, nifty_headers, get_proxies, get_proxy_string

search_url = 'https://host-vdgrw7.api.swiftype.com/api/as/v1/engines/nifties-search/search'
ranked_stats_url = 'https://api.niftygateway.com//market/ranked-stats/'
proxies = get_proxies()
proxy_pool = cycle(proxies)
worker_count = 30
nifty_responses = []
final_nifties = []


async def fetch(nifty):
    """
    Get stats for given nifty object
    :param nifty: Nifty json object
    :return:
    """
    data = f'{{"query":"","page":{{"current":1,"size":2}},"filters":{{"all":[{{"contract_address":["{nifty["unminted_nifty_obj"]["contractObj"]["contractAddress"]}"]}},{{"nifty_type_that_created":"1"}},{{"currently_on_sale":"true"}}]}},"sort":{{"price_in_cents":"asc"}}}}'
    proxy = next(proxy_pool)

    async with aiohttp.ClientSession(headers=search_headers) as session:
        async with session.get(search_url, data=data, proxy=get_proxy_string(proxy)) as response:
            res = await response.json()

            # There might be no price for item
            if res["meta"]["page"]["total_results"] != 0:
                price = res["results"][0]["price_in_cents"]["raw"]
            else:
                price = None

            # Create variables for all stats. You can create your own stats such as SM / PM ratio.
            contract_address = nifty["unminted_nifty_obj"]["contractObj"]["contractAddress"]
            contract_url = f'https://niftygateway.com/itemdetail/primary/{contract_address}/1'
            contract_name = nifty["unminted_nifty_obj"]["niftyTitle"]
            nifty_name = nifty["unminted_nifty_obj"]["niftyTitle"]
            store_url = f'https://niftygateway.com/collections/{nifty["unminted_nifty_obj"]["contractObj"]["storeURL"]}'
            nifty_date_created = nifty["date_created"]
            num_pm_sales = nifty["number_of_pm_sales"]
            num_sm_sales = nifty["number_of_sm_sales"]
            avg_resale_price = nifty["average_secondary_market_sale_price_in_cents"]
            highest_active_bid = nifty["highest_bid_in_cents"]
            lowest_active_ask = nifty["lowest_ask_in_cents"]
            sm_market_volume = nifty["sum_of_primary_market_sales_in_cents"]

            nifty_obj_dict = {
                "contract_address": contract_address,
                "contract_url": contract_url,
                "contract_name": contract_name,
                "nifty_name": nifty_name,
                "store_url": store_url,
                "nifty_date_created": nifty_date_created,
                "num_pm_sales": num_pm_sales,
                "num_sm_sales": num_sm_sales,
                "avg_resale_price": avg_resale_price,
                "highest_active_bid": highest_active_bid,
                "lowest_active_ask": lowest_active_ask,
                "sm_market_volume": sm_market_volume,
                "price": price,
            }

            # Append dictionary to nifties list
            final_nifties.append(nifty_obj_dict)


async def worker(queue):
    """
    Asynchronous worker that receives items from queue
    :param queue:
    :return:
    """
    print('START WORKER')
    while True:
        # Each time, get a nifty object from queue
        nifty = await queue.get()
        await fetch(nifty)
        queue.task_done()
        if len(final_nifties) == len(nifty_responses):
            # Finally, add all of them into a dataframe and save as csv
            df = pd.DataFrame(final_nifties)
            df.to_csv("nifty_prices.csv")
            sys.exit()


async def control(queue):
    """
    Control mechanism for asynchronous queue.
    :param queue:
    :return:
    """
    for nifty in nifty_responses:
        print(datetime.datetime.now())
        queue.put_nowait(nifty)

        # Sleep to slow down execution a bit.
        await asyncio.sleep(0.02)


async def main():
    await get_nifties()
    queue = asyncio.Queue()
    await asyncio.gather(
        control(queue),
        asyncio.gather(*[worker(queue) for _ in range(worker_count)])
    )


async def get_nifties():
    global nifty_responses

    page = 1
    while True:
        data = f'{{"size":100,"current":{page},"ranking_type":"number_of_sm_sales","order_by":"asc","cancelToken":{{"promise":{{}}}},"timeout":30000}}'
        proxy = next(proxy_pool)
        async with aiohttp.ClientSession() as session:
            async with session.post(ranked_stats_url, headers=nifty_headers, data=data, proxy=get_proxy_string(proxy)) as response:
                response_json = await response.json()
                response_json_updated = response_json["data"]["results"]

                nifty_responses.extend(response_json_updated)
                if response_json["data"]["meta"]["page"]["total_pages"] == page:
                    break
                else:
                    page += 1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
