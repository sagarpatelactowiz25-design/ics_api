import re

import requests
from parsel import Selector

def sdpsi(pdp_url, sku='sku'):
    error = {}
    url_request = str()
    max_retires = 5
    for i in range(max_retires):
        url_request= requests.get(pdp_url, verify=False)
        if url_request.status_code == 200:
            break
    if url_request.status_code == 200:
        pass
    else:
        return {'statusCode': 408,
                'error_message':'Request timeout, failed to reach host'}
    if 'class="product info detailed"' not in url_request.text:
        error['statusCode'] = 404
        error['error_message'] = 'Product not found'
        return error

    response_text = url_request.text
    selector = Selector(text=response_text)
    item = dict()
    # Vendor Extracting :-
    item['vendor'] = 'sdpsi'
    # Sku Extracting :-
    try:
        scrapped_sku = "".join(selector.xpath("//div[@class='product-info-main']//h1//span//text()").getall())
        if scrapped_sku != sku:
            error['statusCode'] = 404
            error['error_message'] = f"Scraped SKU:{scrapped_sku} does not match input SKU:{sku}"
            return error

    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = "Internal server error" + str(e)
        return error

    item['sku'] = sku
    # Pdp_url Extracting :-
    item['pdp_url'] = pdp_url
    # Price Extracting :-
    item_price = []
    pricing_rows = selector.xpath('//table[@class="prices-tier items"]//tbody//tr[@class="item"]')
    if pricing_rows:
        for row in pricing_rows:
            qty_range = row.xpath('.//td[1]//text()').get()
            if qty_range:
                qty_range = qty_range.strip()
                if '-' in qty_range:
                    min_qty = int(qty_range.split('-')[0])
                elif '+' in qty_range:
                    min_qty = int(qty_range.split('+')[0])
            else:
                min_qty = 1

            price = row.xpath('.//td[2]//text()').get()
            if price:
                price = price.strip().replace('$', '').strip()
                if price:
                    price_float = float(price)
                else:
                    price_float = None
            else:
                price_float = None

            # Add price entry to the list if it's not a duplicate of min_qty = 1 and the price is valid
            if price_float is not None:
                item_price.append({
                    'currency': 'USD',
                    'min_qty': min_qty,
                    'price': price_float
                })
            else:
                item_price.append({
                    'min_qty': min_qty,
                    'price_string': "Call For Price"
                })
    else:
        price_1 = selector.xpath(
            '//div[contains(@class,"price-box price-final_price")]//span[@class="price"]//text()').extract()
        if price_1:
            price_1 = ''.join(price_1).strip().replace('$', '').strip()
            if price_1:
                price_float = float(price_1)
            else:
                price_float = None
        else:
            price_float = None

        if price_float is not None:
            item_price.append({
                'currency': 'USD',
                'min_qty': 1,
                'price': price_float
            })
        else:
            item_price.append({
                'min_qty': 1,
                'price_string': "Call For Price"
            })
    if not item_price:
        item_price = None
    item['price'] = item_price
    # Lead_time Extracting :-
    lead_time = []
    for val in selector.xpath('//table[@class="prices-tier items"]//tbody//tr[@class="item"]'):
        qty_range = val.xpath('.//td[1]//text()').get().strip()
        if '-' in qty_range:
            min_qty = int(qty_range.split('-')[0])
        elif '+' in qty_range:
            min_qty = int(qty_range.split('+')[0])
        shipping = val.xpath('.//td[3]//text()').get()
        if shipping and shipping.strip():
            lead_time.append(
                {
                    'min_qty': min_qty,
                    'time_to_ship': {'raw_value': shipping.strip()}
                }
            )
    if not lead_time:
        lead_time = None
    item['lead_time'] = lead_time

    # Available_to_checkout Extracting :-
    available_to_checkout =  selector.xpath("//div[@class='box-tocart']//button").get()
    if available_to_checkout == None:
        item['available_to_checkout'] = False
    else:
        item['available_to_checkout'] = True

    # In_stock Extracting :-
    in_stock_text = selector.xpath("//div[@class='product-info-main']//p//text()").getall()
    in_stock_text = ' '.join(in_stock_text).strip()
    if re.search(r"\b0 unit\(s\) in stock\.", in_stock_text):
        item['in_stock'] = False
    else:
        item['in_stock'] = True

    if 'statusCode' in item.keys():
        if item['statusCode'] == 500:
            return item
        elif item['statusCode'] == 404:
            return item
    else:
        return {'statusCode': 200,
                'data': item}


if __name__ == '__main__':
    event = {"pdp_url":"https://shop.sdp-si.com/a-1c44myk10020s.html",
            "sku":"A 1C44MYK10020S",
            "vendor":"sdpsi"}

    print(sdpsi(pdp_url=event['pdp_url'], sku=event['sku']))
