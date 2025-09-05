import json
import requests
from parsel import Selector

def asmcindustrial(url, sku, vendor='asmcindustrial'):
    try:
        url_request = str()
        error = dict()
        try:
            max_retires = 5
            for i in range(max_retires):
                url_request = requests.get(url=url)
                if url_request.status_code == 200:
                    break
            else:
                # The function must have logic for retries Max. 5
                # If request fails after 5 retries it should return following
                return {'statusCode': 408,
                        'error_message': 'Request timeout, failed to reach host'}
        except Exception as e:
            print(e)

        if 'data-product-sku' not in url_request.text:
            error['statusCode'] = 404
            error['error_message'] = 'Product not found'
            return error

        # pass response to Selector :-
        response_req = Selector(url_request.text)

        # define dictionary for making data dictionary :-
        item = dict()

        # vendor Extracting :-
        item['vendor'] = vendor

        # sku Extracting :-
        try:
            item['sku'] = response_req.xpath('//dd[@class="productView-info-value"][@data-product-sku]/text()').get()
            if item['sku'] != sku:
                error['statusCode'] = 404
                error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
                return error
            else:
                pass
        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = str(e)
            return error

        # url Extracting :-
        item['pdp_url'] = url

        # available_to_checkout Extracting :-
        avail = bool(response_req.xpath('//div[@class="form-action"]/input[@value="Add to Cart"]').get())

        item['available_to_checkout'] = avail
        item['in_stock'] = avail

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://www.asmc.net',
            'Referer': 'https://www.asmc.net/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'productcode': f'{sku}',
        }

        response_lead = requests.get('https://api.optimum7.com/yosemitesam/asmc/filtering/bulkprice.php', params=params,
                                headers=headers)

        # response_text_lead = Selector(text=response_lead.text)
        try:
            json_data = json.loads(response_lead.text)
            estimated_lead_time_list = list()
            if item['in_stock'] == True:
                min_qty = int(json_data['result']['minimum'])
                qty_hand = json_data['result']['qtyhand']
                if qty_hand == 0:
                    estimated_lead_time_list.append({"min_qty": min_qty,
                                        "time_to_ship": {"raw_value": "Ships within 2-3 business days"}})
                elif qty_hand != 0:
                    estimated_lead_time_list.append({"min_qty": min_qty,
                                                     "time_to_ship": {"raw_value": "Ships within 1 business day"}})

                if estimated_lead_time_list:
                    item['lead_time'] = estimated_lead_time_list
            else:
                item['lead_time'] = None

            # Price Extracting :-
            item_price = dict()
            price_list = list()
            price_json = json_data['result']['discounts']
            if price_json:
                for pr in price_json:
                    original_price = dict(item_price)
                    original_price['currency'] = 'USD'
                    original_price['min_qty'] = int(pr['min'])
                    price = str(pr['type_value']).replace(',', '')
                    original_price['price'] = float(price)
                    price_list.append(original_price)
                item['price'] = price_list
        except:
            item['lead_time'] = None
            item_price = dict()
            price_list = list()
            original_price = dict(item_price)
            original_price['currency'] = 'USD'
            original_price['min_qty'] = int(response_req.xpath('//div[@class="form-increment"]/input/@value').get())
            original_price['price'] = float(
                response_req.xpath('//meta[@itemprop="price"]/@content').get().split('$')[0].replace(',',
                                                                                                     '').strip())
            price_list.append(original_price)

            item['price'] = price_list

        # return json output :-
        # The function should return a dictionary having statusCode: 200;
        # If all above given headers are scraped properly
        return {"statusCode": 200,
                "data": item}

    except Exception as e:
        # The function should return a dictionary having statusCode: 500;
        # If any internal error occurs. i.e If any Exception is caught inside try-except.
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}
