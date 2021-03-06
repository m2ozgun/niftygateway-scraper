search_headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': 'Bearer search-oowt2dvb47buyvdo1yia3gwb',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://niftygateway.com',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,tr;q=0.7',
}
nifty_headers = {
    'authority': 'api.niftygateway.com',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'accept': 'application/json, text/plain, */*',
    'authorization': 'Bearer U62jWUufJzl5fpIcdimNcZetlj95Ax',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'content-type': 'application/json',
    'origin': 'https://niftygateway.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,tr;q=0.7',
}


def get_proxies():
    proxies_file = open('http_proxies.txt', 'r')
    return proxies_file.readlines()


def get_proxy_string(proxy_item):
    """
    Select a random proxy from the test file
    """
    proxy_item = proxy_item.rstrip()
    line_split = proxy_item.split(':')
    proxy = {
        "ip": line_split[0],
        "port": line_split[1],
        "username": line_split[2],
        "password": line_split[3]
    }
    return f'http://{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'