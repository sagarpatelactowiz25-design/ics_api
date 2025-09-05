import json

import requests
from parsel import Selector

def walkerindustrial(pdp_url, sku='sku'):
    try:
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
        if 'itemprop="productID"' not in url_request.text:
            error['statusCode'] = 410
            error['error_message'] = 'Product not found'
            return error
        response_text = url_request.text
        if 'class="discontinued"' in response_text:
            return {"statusCode": 410,
                    "error_message": "Product is discontinued"}
        else:
            selector = Selector(text=response_text)
            item = dict()

            # Vendor Extracting :-
            item['vendor'] = 'walkerindustrial'

            # Sku Extracting :-
            try:
                scrapped_sku = selector.xpath('//span[@itemprop="productID"]/text()').get('')
                if scrapped_sku != sku:
                        error['statusCode'] = 410
                        error['error_message'] = f"Scraped SKU:{scrapped_sku} does not match input SKU:{sku}"
                        return error
            except Exception as e:
                error['statusCode'] = 500
                error['error_message'] = "Internal server error" + str(e)
                return error

            # Pdp_url Extracting :-
            item['sku'] = sku
            item['pdp_url'] = pdp_url
            item_price = []
            min_qty = selector.xpath('//input[@name="Quantitybox"]/@value').extract_first()
            price = selector.xpath('//span[@itemprop="price"]/span//text()').get('').replace('$','').replace(',','')
            if min_qty is None:
                min_qty = 1
            if price is not None:
                price_float = float(price)
                item_price.append({'currency': 'USD', 'min_qty': int(min_qty), 'price': price_float})
            else:
                item_price.append({'min_qty': 1, 'price_string': "Call for price"})
            if not item_price:
                item_price = None
            item['price'] = item_price

            item['lead_time'] =None


            # In Stock Extraction
            add_to_cart = selector.xpath('//button[contains(text(),"Add To Cart")]//text()')
            stock = selector.xpath('//div[@class="sku-stock"]/span//text()').get('')
            if 'NOT' in stock:
                item['in_stock']=False
            else:
                item['in_stock']=True

            if not add_to_cart:
                item['available_to_checkout']=False
            else:
                item['available_to_checkout']=True

            if 'statusCode' in item.keys():
                if item['statusCode'] == 500:
                    return item
                elif item['statusCode'] == 410:
                    return item
            else:
                return {'statusCode': 200,
                        'data': item}
    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = "Internal server error" + str(e)
        return error

# if __name__ == '__main__':
#     event={"sku": "SMC ASP630F-N04-13S", "vendor": "walkerindustrial", "pdp_url": "https://www.walkerindustrial.com/itemdetail/SMC%20ASP630F-N04-13S"}
#     print(json.dumps(walkerindustrial(event['pdp_url'],event['sku'])))
