import html
import re
import json
from curl_cffi import requests


def iewc(pdp_url, sku, vendor='iewc'):
    try:
        if 'www.iewc.com' not in pdp_url:
            # The function should return a dictionary having statusCode: 404;
            # If pdp_url provided does not belong to the respective store or if url is not a product url
            return {"statusCode": 404,
                    "error_message": "Product not found"}

        # dictionary for final output :-
        product_dict = dict()
        product_dict['pdp_url'] = pdp_url
        link = pdp_url.replace("https://www.iewc.com", "")
        pdp_url = link.replace("/", "%2F")
        # Requests for product_id :-
        product_id_url = f"https://www.iewc.com/api/v1/catalogpages?path={pdp_url}"

        # main Requests :-
        max_retires = 5
        for i in range(max_retires):
            response_main = requests.get(url=product_id_url)
            if response_main.status_code == 200:
                break
        else:
            # The function must have logic for retries Max. 5
            # If request fails after 5 retries it should return following
            return {"statusCode": 408,
                    "error_message": "Request timeout, failed to reach host"}

        final_dict = json.loads(re.sub("\s+", " ", response_main.text.replace("\n", "").replace("\r", "")))

        product_id = final_dict["productId"]

        pdp_url_data = f"https://www.iewc.com/api/v1/products/{product_id}?addToRecentlyViewed=true&applyPersonalization=true&expand=documents,specifications,styledproducts,htmlcontent,attributes,crosssells,pricing,relatedproducts,brand&includeAlternateInventory=true&includeAttributes=IncludeOnProduct&replaceProducts=false"

        # Second requests :-
        max_retires = 5
        for i in range(max_retires):
            response_minimum = requests.get(url=pdp_url_data)
            if response_minimum.status_code == 200:
                break
        else:
            # The function must have logic for retries Max. 5
            # If request fails after 5 retries it should return following
            return {"statusCode": 408,
                    "error_message": "Request timeout, failed to reach host"}

        minimumorder = json.loads(response_minimum.text)['product']['minimumOrderQty']

        # sku :-
        product_dict['sku'] = html.unescape(json.loads(response_minimum.text)['product']['modelNumber']).strip()

        # if sku not get mpn will take as a sku as per ics guidelines :-
        mpn = json.loads(response_minimum.text)['product']['properties']["materialVendorNumber"]
        if not product_dict['sku']:
            product_dict['sku'] = mpn

        if product_dict['sku'] != sku:
            # The function should return a dictionary having statusCode: 404;
            # If scraped sku does not match sku passed in input parameter
            return {"statusCode": 404,
                    "error_message": f"Scraped SKU:{product_dict['sku']} does not match input SKU:{sku}"}

        Instock = json.loads(response_minimum.text)['product']['availability']

        if 'in stock' in Instock['message'].lower():
            product_dict['in_stock'] = True
        elif 'quote required' in Instock['message'].lower():
            product_dict['in_stock'] = False
        else:
            product_dict['in_stock'] = False

        add_to_cart = json.loads(response_minimum.text)['product']['canAddToCart']

        product_dict['available_to_checkout'] = add_to_cart

        # price requests :-
        cookies = {
            'CurrentLanguageId': 'a26095ef-c714-e311-ba31-d43d7e4e88b2',
            'SetContextLanguageCode': 'en-us',
            'CurrentCurrencyId': '30b432b9-a104-e511-96f5-ac9e17867f77',
            '_gcl_au': '1.1.550231141.1698322641',
            '_gid': 'GA1.2.315919975.1698322650',
            'hubspotutk': 'adc8736cf9f8e1aaae01ae7c7e4c4f9c',
            '_lo_uid': '125102-1698322654705-ced4078bf7ef2a34',
            '__lotl': 'https%3A%2F%2Fwww.iewc.com%2F',
            '__lotr': 'https%3A%2F%2Fwww.google.com%2F',
            'InsiteCacheId': '61c041f5-22b1-466a-a1e8-d5859f012d8a',
            'SetContextPersonaIds': 'd06988c0-9358-4dbb-aa3d-b7be5b6a7fd9',
            'CurrentFulfillmentMethod': 'Ship',
            'FirstPage': 'false',
            '__hssrc': '1',
            '_lo_v': '10',
            'RecentlyViewedProducts': '%5b%7b%22Key%22%3a%22FLRYA.35-9%22%2c%22Value%22%3a%222023-10-27T06%3a11%3a17.6817805%2b00%3a00%22%7d%2c%7b%22Key%22%3a%22M16878%2f2-BLE-5%22%2c%22Value%22%3a%222023-10-27T06%3a06%3a27.3125208%2b00%3a00%22%7d%5d',
            '__hstc': '81101128.adc8736cf9f8e1aaae01ae7c7e4c4f9c.1698322654210.1698383542925.1698387074754.5',
            '__hssc': '81101128.1.1698387074754',
            '_dc_gtm_UA-42516321-1': '1',
            '_ga_V4T8V89BWL': 'GS1.1.1698386583.3.1.1698387337.0.0.0',
            '_uetsid': 'a2324a5073f911eeb3dc21c5175ae2d8',
            '_uetvid': 'a232899073f911ee8b1ecbacad748741',
            '_ga_7L1EJC3632': 'GS1.1.1698386583.3.1.1698387338.0.0.0',
            '_ga': 'GA1.2.1061780182.1698322650',
        }

        headers = {
            'authority': 'www.iewc.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': 'CurrentLanguageId=a26095ef-c714-e311-ba31-d43d7e4e88b2; SetContextLanguageCode=en-us; CurrentCurrencyId=30b432b9-a104-e511-96f5-ac9e17867f77; _gcl_au=1.1.550231141.1698322641; _gid=GA1.2.315919975.1698322650; hubspotutk=adc8736cf9f8e1aaae01ae7c7e4c4f9c; _lo_uid=125102-1698322654705-ced4078bf7ef2a34; __lotl=https%3A%2F%2Fwww.iewc.com%2F; __lotr=https%3A%2F%2Fwww.google.com%2F; InsiteCacheId=61c041f5-22b1-466a-a1e8-d5859f012d8a; SetContextPersonaIds=d06988c0-9358-4dbb-aa3d-b7be5b6a7fd9; CurrentFulfillmentMethod=Ship; FirstPage=false; __hssrc=1; _lo_v=10; RecentlyViewedProducts=%5b%7b%22Key%22%3a%22FLRYA.35-9%22%2c%22Value%22%3a%222023-10-27T06%3a11%3a17.6817805%2b00%3a00%22%7d%2c%7b%22Key%22%3a%22M16878%2f2-BLE-5%22%2c%22Value%22%3a%222023-10-27T06%3a06%3a27.3125208%2b00%3a00%22%7d%5d; __hstc=81101128.adc8736cf9f8e1aaae01ae7c7e4c4f9c.1698322654210.1698383542925.1698387074754.5; __hssc=81101128.1.1698387074754; _dc_gtm_UA-42516321-1=1; _ga_V4T8V89BWL=GS1.1.1698386583.3.1.1698387337.0.0.0; _uetsid=a2324a5073f911eeb3dc21c5175ae2d8; _uetvid=a232899073f911ee8b1ecbacad748741; _ga_7L1EJC3632=GS1.1.1698386583.3.1.1698387338.0.0.0; _ga=GA1.2.1061780182.1698322650',
            'origin': 'https://www.iewc.com',
            'referer': f'{pdp_url}',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        payload = {
            'productPriceParameters': [
                {
                    'productId': product_id,
                    'unitOfMeasure': json.loads(response_minimum.text)["product"]["unitOfMeasure"],
                    'qtyOrdered': '1',
                },
            ],
        }

        max_retires = 5
        for i in range(max_retires):
            response_price = requests.post(
                url='https://www.iewc.com/api/v1/realtimepricing',
                cookies=cookies,
                headers=headers,
                json=payload
            )
            if response_price.status_code == 200:
                break
        else:
            # The function must have logic for retries Max. 5
            # If request fails after 5 retries it should return following
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}

        price_dict = json.loads(response_price.text)
        price_information = price_dict['realTimePricingResults'][0]['unitRegularBreakPrices']
        price_list = list()

        if price_information:
            count = 1
            for price in price_information:
                min_quantity = int(price['breakQty']) * int(price['breakPriceWithVat'])
                price = price['breakPriceDisplay'].replace('$', '').replace(',', '')
                pricing = dict()
                if count == 1:
                    pricing['min_qty'] = int(min_quantity) if isinstance(min_quantity, str) else min_quantity
                    pricing['price'] = float(price) if not isinstance(price, float) else price
                    pricing['currency'] = 'USD'
                    count += 1
                else:
                    pricing['min_qty'] = int(min_quantity)
                    pricing['price'] = float(price) if not isinstance(price, float) else price
                    pricing['currency'] = 'USD'


                price_list.append(pricing)

        else:
            pricing = dict()
            if float(price_dict["realTimePricingResults"][0]["actualPriceDisplay"].replace("$", "").replace(
                    ",", "")) != 0:
                minimum_quantity = price_dict['realTimePricingResults'][0]["additionalResults"]["perQuantity"].replace(",","")
                price = json.loads(response_price.text)["realTimePricingResults"][0]["actualPriceDisplay"].replace("$", "")\
                    .replace(",", "")
                pricing['min_qty'] = int(minimum_quantity) if isinstance(minimum_quantity, str) else minimum_quantity
                pricing['price'] = float(price) if price else price
                pricing['currency'] = 'USD'

                price_list.append(pricing)

            else:
                min_qtys = int(minimumorder) if isinstance(minimumorder, str) else minimumorder
                pricing['min_qty'] = 1 if min_qtys == 0 else min_qtys
                pricing['price_string'] = "Call For Price"
                price_list.append(pricing)

        product_dict['price'] = price_list

        product_dict['vendor'] = str(vendor)

        product_dict['lead_time'] = None

        # The function should return a dictionary having statusCode: 200;
        # If all above given headers are scraped properly
        return {"statusCode": 200,
                "data": product_dict}

    except Exception as e:
        # The function should return a dictionary having statusCode: 500;
        # If any internal error occurs. i.e If any Exception is caught inside try-except.
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}
