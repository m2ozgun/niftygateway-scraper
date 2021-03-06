# Asynchronous Nifty Gateway Scraper
A Python based asynchronous Nifty Gateway scraper for receiving nifty stats.

Runs under 40 seconds (1805 nifties as of Mar 6, 2021) and scrapes all the stats in Nifty Gateway. You can use it to build your own NFT Monitor. You can find the example output in nifties_prices.csv
The script also scrapes the cheapest prices for NFTs in secondary markets.

Scrapes the features:
contract_address,
contract_url,
contract_name,
nifty_name,
store_url,
nifty_date_created,
num_pm_sales,
num_sm_sales,
avg_resale_price,
highest_active_bid,
lowest_active_ask,
sm_market_volume,
sm_lowest_price,

Instructions
- Create a virtual environment -> virtualenv venv
- Activate the virtual environment -> source venv/bin/activate on Mac/Linux, venv\Scripts\activate on Windows
- Install required libraries -> pip install -r requirements.txt
- Add proxies file named "http_proxies.txt"
- Run python main.py
