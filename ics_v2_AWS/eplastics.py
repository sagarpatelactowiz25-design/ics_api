import requests
from parsel import Selector

def eplastics(pdp_url, sku='sku'):
    try:
        error = {}
        url_request = str()
        max_retries = 5
        for i in range(max_retries):
            url_request = requests.get(pdp_url, verify=False)
            if url_request.status_code == 200:
                break
        if url_request.status_code != 200:
            return {'statusCode': 408, 'error_message': 'Request timeout, failed to reach host'}

        response_text = url_request.text

        # selector = Selector(text=response_text)
        # if 'class="quantity-price-quantity-row"' not in response_text:
        #     return {'statusCode': 404, 'error_message': 'Product not found'}
        #
        # if 'class="discontinued"' in response_text:
        #     return {"statusCode": 410, "error_message": "Product is discontinued"}

        item = {}
        item['vendor'] = 'eplastic'
        # Sku Extracting
        cookies = {
            'NLVisitorId': 'ZQxd2Ow3Ay3dn88Y',
            '_gcl_au': '1.1.1815940042.1712259594',
            'NS_VER': '2024.1',
            'NLShopperId4': 'TDWp-Jk3AxE6HmbM',
            'invoca_session': '%7B%22ttl%22%3A%222024-06-05T08%3A56%3A27.185Z%22%2C%22session%22%3A%7B%7D%2C%22config%22%3A%7B%22ce%22%3Atrue%2C%22fv%22%3Atrue%7D%7D',
            'jsid_own': '621686.-262184967',
            'ak_bmsc': 'A62AF452CE1C05C074C18C0C623D7E77~000000000000000000000000000000~YAAQFFLbF3O0wjSPAQAA5T79XBe0nMJG5B5pWGI1LB0Nvl/9+vWN9+WF1eeBEBtAKDEINfrfDhKOTxvsmwpH95EWRlw0XZxw3JRbUIJ6TEyM9xTq6R6YSA99GznzDUct5hkrd9jBJ5zzs52uEP0UQlEiJ59Byw5tQddEpeZerWE+3ZOYDexWnQTeDf8n/TRiLeIWf7W4l01Tn6k3pkxjBFgLPk/kMwXvOTD9GK6uac5NbZ0z/lqUhrN6g0ahOjKJI2IhleJz/o6OqFPJOfIC0CgaUO9h6LGU+VoI4rsjFwmjaz3oMIh9kgXxBWthdEocuVxco8OK6PE+LF+TCXVsN7HU3c0pzx8p/lwz0I2+azpvuxqm1o2E7SnzftPCE3j6uk4JF4yX+910JTYd1g==',
            'version_id': '906',
            'recentlyViewedIds': '914%2C2320%2C33956%2C33173%2C31622%2C5597',
            '_gid': 'GA1.2.1260328756.1715252056',
            'JSESSIONID': 'ZUqRaFqTqcHx3S-WVpWPuSzh-qV2vJb-pv0CeMBlLTNLbUc9wsKPT1DS2eGPpsPaUqS9H66nIEf4WOj0l3JpoA_HFGfRMCYTu5eNZ_lUO8Vo_YXo3-9M826qI3Zkr_Pe!1232571649',
            '_ga': 'GA1.2.2051993501.1712259594',
            '_uetsid': '7a9fd7a00df211ef944459063ac33fc3',
            '_uetvid': '1c161d60f2bb11eeb4368303cd3ec925',
            'bm_sv': '6BCDF4A5A62486CEDAE6E62FA54787B8~YAAQFFLbF4ZpwzSPAQAAHkIoXRcywp0JtTEck/tVlxshc6yhvaWWpwemIVnd59cXdyfquW+dS/TjWiu4fjXcojaUzO7uySSVcAGURcZw+90fn0JLHrJQKvGfYHemNAZfizELhdzatKGl+zaybMRXxrxD1chg20xdRqJ0h5T2oLwMfQJdRk1yKxVaydpbsIF8v+tkTnQyArsPymshTr52LTYCQlGWGHMm36X5zczva4BtgBNjSMFd3TdFbaSHKmETzdzJ~1',
            '_ga_2X19SVEBCY': 'GS1.1.1715252050.13.1.1715254869.46.0.0',
            '_ga_PQZSN5FSGB': 'GS1.1.1715253919.11.1.1715254869.0.0.0',
            'SSPOperationId_ee464f23': '85dc43ce-570f-4f93-a921-74846002b42a',
        }

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            # 'cookie': 'NLVisitorId=ZQxd2Ow3Ay3dn88Y; _gcl_au=1.1.1815940042.1712259594; NS_VER=2024.1; NLShopperId4=TDWp-Jk3AxE6HmbM; invoca_session=%7B%22ttl%22%3A%222024-06-05T08%3A56%3A27.185Z%22%2C%22session%22%3A%7B%7D%2C%22config%22%3A%7B%22ce%22%3Atrue%2C%22fv%22%3Atrue%7D%7D; jsid_own=621686.-262184967; ak_bmsc=A62AF452CE1C05C074C18C0C623D7E77~000000000000000000000000000000~YAAQFFLbF3O0wjSPAQAA5T79XBe0nMJG5B5pWGI1LB0Nvl/9+vWN9+WF1eeBEBtAKDEINfrfDhKOTxvsmwpH95EWRlw0XZxw3JRbUIJ6TEyM9xTq6R6YSA99GznzDUct5hkrd9jBJ5zzs52uEP0UQlEiJ59Byw5tQddEpeZerWE+3ZOYDexWnQTeDf8n/TRiLeIWf7W4l01Tn6k3pkxjBFgLPk/kMwXvOTD9GK6uac5NbZ0z/lqUhrN6g0ahOjKJI2IhleJz/o6OqFPJOfIC0CgaUO9h6LGU+VoI4rsjFwmjaz3oMIh9kgXxBWthdEocuVxco8OK6PE+LF+TCXVsN7HU3c0pzx8p/lwz0I2+azpvuxqm1o2E7SnzftPCE3j6uk4JF4yX+910JTYd1g==; version_id=906; recentlyViewedIds=914%2C2320%2C33956%2C33173%2C31622%2C5597; _gid=GA1.2.1260328756.1715252056; JSESSIONID=ZUqRaFqTqcHx3S-WVpWPuSzh-qV2vJb-pv0CeMBlLTNLbUc9wsKPT1DS2eGPpsPaUqS9H66nIEf4WOj0l3JpoA_HFGfRMCYTu5eNZ_lUO8Vo_YXo3-9M826qI3Zkr_Pe!1232571649; _ga=GA1.2.2051993501.1712259594; _uetsid=7a9fd7a00df211ef944459063ac33fc3; _uetvid=1c161d60f2bb11eeb4368303cd3ec925; bm_sv=6BCDF4A5A62486CEDAE6E62FA54787B8~YAAQFFLbF4ZpwzSPAQAAHkIoXRcywp0JtTEck/tVlxshc6yhvaWWpwemIVnd59cXdyfquW+dS/TjWiu4fjXcojaUzO7uySSVcAGURcZw+90fn0JLHrJQKvGfYHemNAZfizELhdzatKGl+zaybMRXxrxD1chg20xdRqJ0h5T2oLwMfQJdRk1yKxVaydpbsIF8v+tkTnQyArsPymshTr52LTYCQlGWGHMm36X5zczva4BtgBNjSMFd3TdFbaSHKmETzdzJ~1; _ga_2X19SVEBCY=GS1.1.1715252050.13.1.1715254869.46.0.0; _ga_PQZSN5FSGB=GS1.1.1715253919.11.1.1715254869.0.0.0; SSPOperationId_ee464f23=85dc43ce-570f-4f93-a921-74846002b42a',
            'priority': 'u=1, i',
            'referer': f'{pdp_url}',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-sc-touchpoint': 'shopping',
        }
        pdp_split = pdp_url.split('/')[-1]
        params = {
            # 'c': '621686',
            'country': 'US',
            'currency': 'USD',
            'fieldset': 'details',
            'include': 'facets',
            'language': 'en',
            # 'n': '4',
            # 'pricelevel': '5',
            'url': f'{pdp_split}',
        }

        response = requests.get('https://www.eplastics.com/api/items', params=params, cookies=cookies, headers=headers)
        json_data = response.json()['items'][0]
        scrapped_sku = json_data['itemid'].strip()
        if scrapped_sku != sku:
            error['statusCode'] = 404
            error['error_message'] = f"Scraped SKU:{scrapped_sku} does not match input SKU:{sku}"
            return error

        # Pdp_url Extracting
        item['sku'] = sku
        item['pdp_url'] = pdp_url

        # Price Extraction
        item_price = []
        if 'priceschedule' in json_data['onlinecustomerprice_detail']:
            for price_list in json_data['onlinecustomerprice_detail']['priceschedule']:
                min_qty = price_list.get('minimumquantity', None)
                if min_qty is not None:
                    min_qty = int(min_qty)
                    if min_qty == 0:
                        min_qty = 1
                    price_value = float(price_list['price'])
                    item_price.append({'currency': 'USD', 'min_qty': min_qty, 'price': price_value})
        if len(item_price) > 1:
            min_qty_1_indices = [index for index, price_info in enumerate(item_price) if price_info['min_qty'] == 1]
            if len(min_qty_1_indices) > 1:
                del item_price[min_qty_1_indices[0]]
        elif not json_data['dontshowprice']:
            price_value = float(json_data['onlinecustomerprice_detail']['onlinecustomerprice'])
            item_price.append({'currency': 'USD', 'min_qty': 1, 'price': price_value})
        else:
            item_price.append({'min_qty': 1, 'price_string': 'Call For Price'})

        item['price'] = item_price if item_price else None
        if not item_price:
            item_price = None
        item['price'] = item_price

        # Lead Time Extraction
        item['lead_time'] = None
        in_stock_text = json_data.get('isinstock')
        if in_stock_text is True:
            item['in_stock'] = True
            item['available_to_checkout'] = True
        else:
            price_string = item_price[0].get('price_string') if item_price else None
            if price_string == 'Call For Price':
                item['in_stock'] = False
                item['available_to_checkout'] = False
            else:
                item['in_stock'] = True
                item['available_to_checkout'] = True

        return {'statusCode': 200, 'data': item}
    except Exception as e:
        return {'statusCode': 500, 'error_message': "An unexpected error occurred: " + str(e)}

if __name__ == '__main__':
    event = {'sku': 'G10NAT1.125X48X96',
             'pdp_url': 'https://www.eplastics.com/G10NAT1-125X48X96',
             'vendor': 'eplastics'}
    print(eplastics(pdp_url=event['pdp_url'], sku=event['sku']))
