import json
import re
import requests
from parsel import Selector

max_retires = 5

def clear_cart():
    url = "https://www.fixsupply.com/checkout/cart/updatePost/"
    payload = 'form_key=PoK1eAxiMHJaYtiY&cart%5B249630%5D%5Bqty%5D=1&update_cart_action=empty_cart'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'fs_is_mobile=0; fs_visitor_id=161628434492374211715752547718843349324781; _gcl_au=1.1.529707905.1715752549; _ga=GA1.1.1985639095.1715752549; wp_ga4_customerGroup=NOT%20LOGGED%20IN; _ga_PL3Y9GWTZ8=deleted; _ga_PL3Y9GWTZ8=GS1.1.1718796592.8.1.1718797019.39.0.388467077; wp_ga4_customerGroup=NOT%20LOGGED%20IN; fs_utm_source=www.google.com; fs_utm_medium=referral; fs_visitor_saved=1; form_key=PoK1eAxiMHJaYtiY; mage-messages=; PHPSESSID=b71e16de906e9e501b5349f728a6c704; form_key=PoK1eAxiMHJaYtiY; mage-cache-sessid=true; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; PHPSESSID=fde65dfe035232628318290344c17b2e; private_content_version=a71b01ba4863c3ea36dd2841587cd053; _ga_PL3Y9GWTZ8=GS1.1.1721723205.32.1.1721725787.8.0.1989679239; section_data_ids={%22cart%22:1721726790%2C%22directory-data%22:1721725402%2C%22cart_latest_added_product%22:1721725402%2C%22wp_ga4%22:1721726738%2C%22company%22:1721726738%2C%22messages%22:null}; PHPSESSID=b71e16de906e9e501b5349f728a6c704; form_key=PoK1eAxiMHJaYtiY; fs_visitor_id=161628434492374211715752547718843349324781; private_content_version=c4888d1a142bbb5d41525b5570b09a11; wp_ga4_customerGroup=NOT%20LOGGED%20IN',
        'origin': 'https://www.fixsupply.com',
        'priority': 'u=0, i',
        'referer': 'https://www.fixsupply.com/checkout/cart/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

def add_cart(product_id,qty):
    payload = {'product': f'{product_id}',
               'selected_configurable_option': '',
               'related_product': '',
               'item': f'{product_id}',
               'form_key': 'PoK1eAxiMHJaYtiY',
               'qty': f'{qty}'}
    files = []
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'fs_is_mobile=0; fs_visitor_id=161628434492374211715752547718843349324781; _gcl_au=1.1.529707905.1715752549; _ga=GA1.1.1985639095.1715752549; wp_ga4_customerGroup=NOT%20LOGGED%20IN; _ga_PL3Y9GWTZ8=deleted; _ga_PL3Y9GWTZ8=GS1.1.1718796592.8.1.1718797019.39.0.388467077; wp_ga4_customerGroup=NOT%20LOGGED%20IN; fs_utm_source=www.google.com; fs_utm_medium=referral; fs_visitor_saved=1; form_key=PoK1eAxiMHJaYtiY; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-messages=; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; PHPSESSID=b71e16de906e9e501b5349f728a6c704; form_key=PoK1eAxiMHJaYtiY; mage-cache-sessid=true; private_content_version=14d457d12d566283502261de238f602e; section_data_ids={%22cart%22:1721719474%2C%22directory-data%22:1721719430%2C%22cart_latest_added_product%22:1721719430%2C%22wp_ga4%22:1721719430%2C%22company%22:1721719430}; _ga_PL3Y9GWTZ8=GS1.1.1721718102.31.1.1721719953.60.0.1221050801; PHPSESSID=b71e16de906e9e501b5349f728a6c704; form_key=PoK1eAxiMHJaYtiY; fs_visitor_id=161628434492374211715752547718843349324781; private_content_version=67512f85ae4619dfbfdb97a3a9c533cd; wp_ga4_customerGroup=NOT%20LOGGED%20IN',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMzNjMzNzUiLCJhcCI6IjExMjAwNDg5NTYiLCJpZCI6IjhhMjhiZjBiM2Q5YzVmNjMiLCJ0ciI6ImJmMGNlZGRlMWJhYmIwN2EzYmYyZjg0ODQwMDFjMzhjIiwidGkiOjE3MjE3MTk5ODMwMjMsInRrIjoiMTMyMjg0MCJ9fQ==',
        'origin': 'https://www.fixsupply.com',
        'priority': 'u=1, i',
        # 'referer': 'https://www.fixsupply.com/bulk-scrw-4104-machine-screw-slotted-flat-head-zinc-plated-steel-4-40-thread-7-8-long',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-bf0cedde1babb07a3bf2f8484001c38c-8a28bf0b3d9c5f63-01',
        'tracestate': '1322840@nr=0-1-3363375-1120048956-8a28bf0b3d9c5f63----1721719983023',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-newrelic-id': 'VwUBUlVUDRABVVFRDwAHX1MI',
        'x-requested-with': 'XMLHttpRequest'
    }
    for i in range(max_retires):
        url = f"https://www.fixsupply.com/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuZml4c3VwcGx5LmNvbS9idWxrLXNjcnctNDEwNC1tYWNoaW5lLXNjcmV3LXNsb3R0ZWQtZmxhdC1oZWFkLXppbmMtcGxhdGVkLXN0ZWVsLTQtNDAtdGhyZWFkLTctOC1sb25n/product/{product_id}/"
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code == 200:
            data = response.text
            return data

def summery(code):
    url = "https://www.fixsupply.com/rest/default/V1/guest-carts/Ha5twePYT7EHjLmDxIf4VTJdJ8ewKqPy/estimate-shipping-methods"

    payload = json.dumps({
        "address": {
            "street": [
                "Main Street",
                "",
                ""
            ],
            "city": "New York",
            "region_id": "128",
            "region": "New York",
            "country_id": "US",
            "postcode": f"{code}",
            "email": "",
            "firstname": "Devin",
            "lastname": "John",
            "company": "",
            "telephone": "",
            "custom_attributes": [
                {
                    "attribute_code": "is_residential",
                    "value": "1"
                },
                {
                    "attribute_code": "is_liftgate_required",
                    "value": "0"
                },
                {
                    "attribute_code": "is_appointment_required",
                    "value": "0"
                },
                {
                    "attribute_code": "is_residential_saved",
                    "value": "1"
                }
            ]
        }
    })
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'fs_is_mobile=0; fs_visitor_id=161628434492374211715752547718843349324781; _gcl_au=1.1.529707905.1715752549; _ga=GA1.1.1985639095.1715752549; wp_ga4_customerGroup=NOT%20LOGGED%20IN; _ga_PL3Y9GWTZ8=deleted; _ga_PL3Y9GWTZ8=GS1.1.1718796592.8.1.1718797019.39.0.388467077; wp_ga4_customerGroup=NOT%20LOGGED%20IN; fs_utm_source=www.google.com; fs_utm_medium=referral; fs_visitor_saved=1; form_key=PoK1eAxiMHJaYtiY; PHPSESSID=b71e16de906e9e501b5349f728a6c704; form_key=PoK1eAxiMHJaYtiY; mage-cache-sessid=true; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; mage-messages=; private_content_version=378548e2385aaa7b3f8555eb9c7aa6cd; _ga_PL3Y9GWTZ8=GS1.1.1721723205.32.1.1721729662.52.0.1989679239; section_data_ids={%22cart%22:1721729662%2C%22directory-data%22:1721729333%2C%22cart_latest_added_product%22:1721729333%2C%22wp_ga4%22:1721729333%2C%22company%22:1721729333}; PHPSESSID=b71e16de906e9e501b5349f728a6c704; form_key=PoK1eAxiMHJaYtiY; fs_visitor_id=161628434492374211715752547718843349324781; private_content_version=c4888d1a142bbb5d41525b5570b09a11; wp_ga4_customerGroup=NOT%20LOGGED%20IN',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMzNjMzNzUiLCJhcCI6IjExMjAwNDg5NTYiLCJpZCI6IjUyZmZjMjUyMTNmMjczNDciLCJ0ciI6IjMzMTVkNTJiZDJlNWI2NDA1YzVhNTBmMzFmZmM4YjIwIiwidGkiOjE3MjE3Mjk2ODAxNjYsInRrIjoiMTMyMjg0MCJ9fQ==',
        'origin': 'https://www.fixsupply.com',
        'priority': 'u=1, i',
        'referer': 'https://www.fixsupply.com/checkout/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-3315d52bd2e5b6405c5a50f31ffc8b20-52ffc25213f27347-01',
        'tracestate': '1322840@nr=0-1-3363375-1120048956-52ffc25213f27347----1721729680166',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-newrelic-id': 'VwUBUlVUDRABVVFRDwAHX1MI',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

def fixsupply(pdp_url,sku,zipcode):
    error_ = dict()
    url_request = str()
    max_retires = 5
    for i in range(max_retires):
        url_request = requests.get(url=pdp_url)
        if url_request.status_code == 200:
            break
    if url_request.status_code == 200:
        pass
    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}
    if 'data-ui-id="page-title-wrapper"' not in url_request.text:
        error_['statusCode'] = 404
        error_['error_message'] = 'Product not found'
        return error_

    response = Selector(url_request.text)

    # define dictionary for making data dictionary :-
    item = dict()

    # vendor Extracting :-
    item['vendor'] = 'fixsupply'
    # sku Extracting :-
    try:
        item['sku'] = response.xpath('//div[@class="product attribute sku"]/div/text()').get().strip()

        if not item['sku']:
            item['sku'] = response.xpath('//div[@class="product attribute product-brand-number-attribute"]/span/text()').get().strip()
        if item['sku'] != sku:
            error_['statusCode'] = 500
            error_['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
            return error_
    except Exception as e:
        error_['statusCode'] = 500
        error_['error_message'] = str(e)
        return error_

    # pdp_url Extracting :-
    item['pdp_url'] = pdp_url

    # Price Extracting :-
    item_price = dict()
    item_price['currency'] = 'USD'
    min_qty = response.xpath('//span[@class="price-uom-label"]/text()').get()
    if min_qty:
        try:
            item_price['min_qty'] = int(re.findall("\d+", min_qty)[0])
        except:
            item_price['min_qty'] = 1
    else:
        item_price['min_qty'] = 1

    price_main = response.xpath('//div[@class="product-info-price"]//span[@class="price"]/text()').get()
    if price_main == None:
        if response.xpath('//div[@class="ui-messageselector"]//p//text()'):
            item_price['price_string'] = None
        else:
            item_price['price_string'] = 'Call for price'
    else:
        price_float = price_main.replace('$', '').replace(',', '')
        price_float_1 = price_main.replace('$', '').replace(',', '')
        if price_float_1 != 'Request Pricing':
            item_price['price'] = float(price_float)
            item['cart_summary'] = [{"shipping_cost": item_price['price']}]


    price_list = list()
    price_list.append(item_price)
    item['price'] = price_list

    # available_to_checkout and in_stock Extracting :-
    available_to_checkout = response.xpath('//button[@id="product-addtocart-button"]').get()
    if available_to_checkout == None:
        item['available_to_checkout'] = False
        item['in_stock'] = False
    else:
        item['available_to_checkout'] = True
        item['in_stock'] = True
    ship_time = response.xpath("//div[@class='expected-to-ship']/span[contains(@class,'stock-item')]/text()").getall()
    if ship_time:
        # Check if the item is temporarily unavailable
        if ship_time != "This item is temporarily unavailable.":
            if len(ship_time) == 1:
                lead_time = [{'min_qty': 1, 'time_to_ship': {'raw_value': ship_time[0]}}]
                estimated_lead_time = json.loads(json.dumps(lead_time))
                item['lead_time'] = estimated_lead_time
            else:
                aa = ship_time[0].split('.')
                min_qty = re.sub('[A-Za-z,+\s]+', '', aa[0])
                time_ = re.sub('\s+', ' ', ". ".join(aa[1:3]).strip())
                # If not unavailable, create a lead time dictionary
                lead_time = [{'min_qty': int(min_qty), 'time_to_ship': {'raw_value': time_}}]
                estimated_lead_time = json.loads(json.dumps(lead_time))
                # Add estimated lead time to the product loader
                item['lead_time'] =  estimated_lead_time
        else:
            item['lead_time'] = None
    else:
        item['lead_time']= None
    form = response.xpath('//div[@class="product-add-form"]/form[@id="product_addtocart_form"]/@action').get()
    pro_id = response.xpath('//div[@class="product-add-form"]/form/input[@name="product"]/@value').get()
    qty = response.xpath('//div[@class="qty-increment-info"]//span//text()').get()
    if qty:
        qty = re.findall(r'\d+',qty)[0]
    else:
        qty = 1
    if form:
        clear_ = clear_cart()
        if pro_id:
            crat_info = add_cart(pro_id,qty)
            summery_ = summery(zipcode)
            crat_data = json.loads(summery_)
            cart_list = list()
            for data in crat_data:
                cart_dict = {
                    "zipcode": zipcode,
                    "shipping_method": data['method_title'],
                    "shipping_cost": data['amount'],
                    "delivery_date": data["extension_attributes"]['method_message']
                }
                cart_list.append(cart_dict)
            item['cart_summary'] = json.loads(json.dumps(cart_list))

    if 'statusCode' in item.keys():
        if item['statusCode'] == 500:
            return item
        elif item['statusCode'] == 404:
            return item
    else:
        return {'statusCode': 200,
                'data': item}

# if __name__ == '__main__':
#     event = {"pdp_url": "https://www.fixsupply.com/sika-607405-sikabiresin-ch72-1-two-component-epoxy-lamination-system-fast-cure-pale-amber-1-quart-part-b",
#              "sku": "AO9763",
#              "zipcode": '10001',
#              "vendor":"fixsupply"}
#     print(fixsupply(pdp_url=event['pdp_url'], sku=event['sku'],zipcode=event['zipcode']))