import datetime
import json
import time
from concurrent.futures import ThreadPoolExecutor

import requests

import api_key

MAX_RETRIES = 5
token=api_key.scraperDo_key

# PROXY = "http://2d76727898034978a3091185c24a5df27a030fdc3f8:customHeaders=true@proxy.scrape.do:8080"
# PROXY = "http://2d76727898034978a3091185c24a5df27a030fdc3f8:@proxy.scrape.do:8080"
PROXY = f"http://{token}:geoCode=us@proxy.scrape.do:8080"
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Wed, 07 May 2025 02:44:14 GMT',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': '__cf_bm=_HTMWu3rqsu38vB5CA8sDBByxG5d_CwlMou0.cuqExc-1747726013-1.0.1.1-jaRYb0uBqfSZMexzdtC.l.9bRw.98.vHKnSXqOsYj94_uF29lIXZKXSqSaWFu2SodupGshgQW1Xl.Pd.rZjskyxCdO.LMmOPzL1AvgebifOHC6MJJH3c4fiTWRZTb_Jo; _cfuvid=H2gXL_W1IKpypNM7.aXHqhQBN635LdXEluOwz8GoUVg-1747726013067-0.0.1.1-604800000; at_check=true; mboxEdgeCluster=35; cf_clearance=IuorlQ_XsRFbmoN52iP1w.qGFUgalpvRQa_wEPa9JE0-1747726018-1.2.1.1-Jyci.8lLbs4n8ME.sEBiBamJoMDfyzr6qDr6AU0kYRwmqWOABo1V5nmSbvcxVNzYlVjB4sKKcMuTgZVqht7IegrGYlkQk6aKCaj5FkXnIDtV7Zw_ALpwfMIJMzHH0Y7EVR0civURa3pgORfZ0CVUFvke63P1Mzm9S9Vf6uq1wz1eucSqjl6IeElCRS5aoROy9rKRIVOdlNsC8NbU3sHGdumQPK1jT7DLX.AI4LIjAAe6FY7NfZZnckKlpFnKIvamdIlag0SxOUDDIT9k4IKBjvXyBwxxCVKUKEo33RZ7zcqMniKqnmFV5NZg3eAOXfaYkPi3jzE932Rlpkf21lAgxijIFHgCIy.r2ka.iAx.WSs; AMCVS_C1D7337B54F62DE60A4C98A1%40AdobeOrg=1; AMCV_C1D7337B54F62DE60A4C98A1%40AdobeOrg=179643557%7CMCIDTS%7C20229%7CMCMID%7C87282890408921437382867121008838532222%7CMCAAMLH-1748330819%7C7%7CMCAAMB-1748330819%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1747733219s%7CNONE%7CvVersion%7C5.5.0; JSESSIONID=0000_rIQTzb4xhGWwrqsyJnQ6q8:-1; BVBRANDID=27acad62-9f41-4368-9156-25a966d50a09; BVBRANDSID=02e52396-e802-44c6-b60b-93238c19d38e; mp_northern_tool_mixpanel=eyJkaXN0aW5jdF9pZCI6ICIxOTZlYzk2Yjg5NWEwNC0wMDU2ZGQyYzAyNGVkMjgtMjYwMTFmNTEtZTEwMDAtMTk2ZWM5NmI4OTYyZDY2IiwiYmNfcGVyc2lzdF91cGRhdGVkIjogMTc0NzcyNjAyMjgwN30; bc_invalidateUrlCache_targeting=1747726022866; page_site_section=pdp | lawn + garden; s_cc=true; __ogfpid=f126e83e-633f-43e5-8c13-5b08e8a42999; utag_main=v_id:0196ec9698db0012e630d64f0e450506f0067067007e8$_sn:1$_se:2$_ss:0$_st:1747727823405$ses_id:1747726014684%3Bexp-session$_pn:1%3Bexp-session$vapi_domain:northerntool.com$customer_id:%3Bexp-session; bluecoreNV=true; s_sq=ntool-dev%3D%2526pid%253Dpdp%252520%25257C%252520lawn%252520%25252B%252520garden%252520%25257C%252520replacement%252520batteries%252520%25257C%252520item%25252063986%2526pidt%253D1%2526oid%253Dfunctionzr%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DBUTTON; forterToken=2ec6574311d346f68b6da8b08c2bd63d_1747726013642__UDF43-mnf-a4_11ck_; mbox=session#19ae857e5a62478e838a38c4f82df287#1747727889|PC#19ae857e5a62478e838a38c4f82df287.35_0#1810970821; _gcl_au=1.1.1706605645.1747726030; _uetsid=d78df830354b11f09f46a5007dc0fabe; _uetvid=d78e16c0354b11f0a9e967283837b384; cto_bundle=7Y7PKV8lMkZzRWhENVg2SnZveUJxWTRzNjd6VyUyRmEwV3JyWmFuU3lTQ3RrNmQyR0RxS0hLS3hYVjhRbmVCV3NPUHFwWVdJc0FkUXo2V1JDS0JPJTJCTWNOZFlLREdBZHhPU3ZKS1g1SHd1JTJGZCUyRjZnWVpiT3VtJTJGWjlpS1hXbEJwbzhoNmlCaSUyRlFVRXdCWWpMTWJ2dkFEU2pZS1FkT2pDbUJNYXl1akJRQWdRZnRBbSUyRnY2SWx3JTNE',
}


def fetch_response(url):
    is_search_url = "www.northerntool.com/search/resources" in url
    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                proxies={"http": PROXY, "https": PROXY},
                verify=False
            )
            if response.status_code == 200:
                return {'statusCode': 200, 'Response': response}, is_search_url
            if response.status_code == 404:
                return {'statusCode': 410, 'error_message': 'Product not found'}, is_search_url
        except requests.RequestException as e:
            continue  # retry
    return {'statusCode': 408, 'error_message': 'Request timeout, failed to reach host'}, is_search_url


def parse_shipping_dates(shipping_data):
    try:
        lead_times = []
        for method in shipping_data.get('shipping_methods', []):
            items = json.loads(method['lineItems'])
            low = datetime.datetime.strptime(items[0]['expDeliveryLow'], '%Y-%m-%d').strftime('%a, %b %d')
            high = datetime.datetime.strptime(items[0]['expDeliveryHigh'], '%Y-%m-%d').strftime('%a, %b %d')
            lead_times.append({'min_qty': 1, 'time_to_arrive': {'raw_value': f"{low} - {high}"}})
        return lead_times
    except Exception:
        return lead_times


def northerntool(pdp_url, sku, vendor='northerntool'):
    if 'https://www.northerntool.com/' not in pdp_url:
        return {"statusCode": 410, "error_message": "Product not found"}

    product_url = f'https://www.northerntool.com/search/resources/api/v2/products?partNumber={sku}&storeId=6970&profileName=NTE_V2_findProductByPartNumber_Details'
    shipping_url = f'https://www.northerntool.com/wcs/resources/store/6970/cart/@self/usable_shipping_mode/extended?zipCode=10005&quantity=1&partNumber={sku}&lineType=D'

    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            responses = list(executor.map(fetch_response, [product_url, shipping_url]))

        pdp_json, shipping_json = None, None
        for res, is_product in responses:
            if res['statusCode'] != 200:
                return res
            if is_product:
                pdp_json = json.loads(res['Response'].text)['contents'][0]
            else:
                shipping_json = res['Response'].json()

        if not pdp_json:
            return {"statusCode": 408, "error_message": "Product data not received"}

        scraped_sku = pdp_json.get('partNumber')
        if scraped_sku != sku:
            return {"statusCode": 410, "error_message": f"Scraped SKU:{scraped_sku} does not match input SKU:{sku}"}

        price_info = pdp_json.get('price', [{}])[1]
        currency = price_info.get('currency')
        price = price_info.get('value')

        item = {
            'vendor': vendor,
            'pdp_url': pdp_url,
            'sku': scraped_sku,
            'price': [{"min_qty": 1, "price": float(price), "currency": currency}] if price else [{
                "min_qty": 1,
                "price_string": "Call For Price"
            }],
            'lead_time': parse_shipping_dates(shipping_json) if shipping_json else []
        }

        buyable = str(pdp_json.get('buyable', 'false')).lower() == "true"
        item['available_to_checkout'] = item['in_stock'] = buyable

        return {'statusCode': 200, 'data': item}

    except Exception as e:
        return {"statusCode": 500, "error_message": f"Internal server error: {str(e)}"}


# For testing
# if __name__ == '__main__':
#     start = time.time()
#     #     # test_event = {
#     #     #     "sku": "63986",
#     #     #     "vendor": "northerntool",
#     #     #     "pdp_url": "https://www.northerntool.com/products/stihl-ap-series-lithium-ion-battery-36v-6-0-ah-model-ap-300-63986"
#     #     # }
# 
#     # test_event = {
#     #     "sku": "1000583",
#     #     "vendor": "northerntool",
#     #     "pdp_url": "https://www.northerntool.com/products/flash-furniture-24in-h-metal-counter-stool-with-slat-back-and-wood-seat-100058"
#     # }
#     test_event={"sku": "100095", "vendor": "northerntool", "pdp_url": "https://www.northerntool.com/products/coxreels-combo-air-and-electric-hose-reel-with-quad-outlet-attachment-and-3-8in-x-50ft-pvc-hose-max-300-psi-model-c-l350-5012-b-100095"}
#     print(json.dumps(northerntool(**test_event), indent=2))
#     print(f"Time taken: {time.time() - start:.2f}s")
