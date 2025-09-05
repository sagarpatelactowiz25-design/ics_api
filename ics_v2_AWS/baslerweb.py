import json
import math
import requests
from parsel import Selector

def baslerweb(url, sku, vendor='baslerweb'):
    try:
        url_request = str()
        error = dict()
        try:
            max_retires = 5
            for i in range(max_retires):
                url_request = requests.get(url=url)
                if url_request.status_code == 200:
                    break
                elif url_request.status_code == 404:
                    error['statusCode'] = 404
                    error['error_message'] = 'Product not found'
                    return error
                else:
                    # The function must have logic for retries Max. 5
                    # If request fails after 5 retries it should return following
                    return {'statusCode': 408,
                            'error_message': 'Request timeout, failed to reach host'}
        except Exception as e:
            print(e)

        if '<th scope="row">Order Number</th>' not in url_request.text:
            error['statusCode'] = 404
            error['error_message'] = 'Product not found'
            return error

        # pass response to Selector :-
        response = Selector(url_request.text)

        # define dictionary for making data dictionary :-
        item = dict()

        # vendor Extracting :-
        item['vendor'] = vendor

        # sku Extracting :-
        try:
            item['sku'] = response.xpath('//th[contains(text(),"Order Number")]/following-sibling::td/text()').get()
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

        # Price Extracting :-
        item_price = dict()
        price_list = list()
        if response.xpath('//table[@class="product-detail-add-to-cart__attribute-table"]//tr[last()]//div'):
            price = response.xpath(
                '//div[@class="product-detail-add-to-cart__attribute-value"]//text()').get('').replace(
                "\n", "").replace(',', '').strip()
            if "$" in price:
                original_price = dict(item_price)
                original_price['currency'] = 'USD'
                original_price['min_qty'] = 1
                price = price.replace('$', '')
                original_price['price'] = float(price)
                price_list.append(original_price)
            else:
                original_price = dict(item_price)
                original_price['min_qty'] = 1
                original_price['price_string'] = "Call For Price"
                price_list.append(original_price)
        else:
            original_price = dict(item_price)
            original_price['min_qty'] = 1
            original_price['price_string'] = "Call For Price"
            price_list.append(original_price)

        item['price'] = price_list

        # available_to_checkout Extracting :-
        if response.xpath('//button[@class="button button--icon-left button--attraction button--medium"]'):
            item['available_to_checkout'] = True
            item['in_stock'] = True
        else:
            item['available_to_checkout'] = False
            item['in_stock'] = False

        estimate_list = []
        if response.xpath('//span[@class="product-detail-add-to-cart__delivery-option-title-addition"]'):
            estimate_string = ''.join(response.xpath(
                '//span[@class="product-detail-add-to-cart__delivery-option-title-addition"]/text()').getall()).strip()
            if 'days' in estimate_string.lower() or 'weeks' in estimate_string.lower() or 'months' in estimate_string.lower():
                estimate_list.append({'min_qty': 1, 'time_to_arrive': {"raw_value": estimate_string.strip()}})
            else:
                item['lead_time'] = None
            item['lead_time'] = estimate_list
        else:
            item['lead_time'] = None

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


# if __name__ == '__main__':
#     # parse function call with products_url and sku :-
#     data = baslerweb(
#         url="https://www.baslerweb.com/en-us/shop/a2a640-240gmswir",
#         sku="108571")
#     # print json :-
#     print(data)

