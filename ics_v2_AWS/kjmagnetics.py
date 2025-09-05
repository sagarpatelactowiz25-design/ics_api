import requests
from parsel import Selector
import re

def kjmagnetics(pdp_url, sku='sku'):
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
    if 'class="product-pricing__quantity-discounts"' not in url_request.text:
        error['statusCode'] = 404
        error['error_message'] = 'Product not found'
        return error
    response_text = url_request.text
    if 'class="discontinued"' in response_text:
        return {"statusCode": 410,
                "error_message": "Product is discontinued"}
    else:
        selector = Selector(text=response_text)
        # print(response_text)
        item = dict()
        # Vendor Extracting :-
        item['vendor'] = 'kjmagnetics'
        # Sku Extracting :-
        try:
            scrapped_sku = selector.xpath('//div//h1[@itemprop="name"]/text()').get('').strip()
            if '-' in scrapped_sku:
                main_sku = scrapped_sku.rsplit('-', 1)
                scrapped_sku = main_sku[0].strip()
                # print(scrapped_sku)
                if scrapped_sku.strip().lower() != sku.strip().lower():
                    error['statusCode'] = 404
                    error['error_message'] = f"Scraped SKU:{scrapped_sku} does not match input SKU:{sku}"
                    return error

        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = "Internal server error" + str(e)
            return error
        # Pdp_url Extracting :-
        item['sku'] = sku
        item['pdp_url'] = pdp_url
        #************************************* PRICE *******************
        item_price = []
        pricing_table = selector.xpath('//*[@class="product-pricing__quantity-discounts"]//table//tr')
        if not pricing_table:
            min_qty = int(selector.xpath('//input[@title="Quantity"]/@value').get() or 1)
            price_string = selector.xpath('//*[@itemprop="price"]/@content').get()
            if price_string:
                price_float = float(price_string)
                item_price.append({'currency': 'USD', 'min_qty': min_qty, 'price': price_float})
            else:
                item_price.append({'min_qty': min_qty, 'price_string': "Call for price"})
        else:
            for tr in pricing_table[1:-1]:
                all_td = [i.strip() for i in tr.xpath(".//td//text()").getall() if i.strip()]
                min_qty_list = re.findall("\d+", all_td[1])
                min_qty = int(min_qty_list[0]) if min_qty_list else 1
                price_string = all_td[0][1:] if all_td else None
                if price_string:
                    price_float = float(price_string)
                    item_price.append({'currency': 'USD', 'min_qty': min_qty, 'price': price_float})
                else:
                    item_price.append({'min_qty': min_qty, 'price_string': "Call for price"})

        if not item_price:
            item_price = None
        item['price'] = item_price

        # Lead_time Extracting :-
        lead_time = []
        estimated_lead_time_text = selector.xpath('//section[@class="header-additional-info"]//p//text()').getall()
        cleaned_lead_time_text = ' '.join(estimated_lead_time_text).replace('\r\n', '').replace('\t', '').strip()
        lead_time = [
            {
                "min_qty": 1,
                "time_to_ship": {
                    "raw_value": cleaned_lead_time_text
                }
            }
        ]
        if not cleaned_lead_time_text:
            lead_time = None
        item['lead_time'] = lead_time

        # InStock Extracting :-
        in_stock_elements = selector.xpath("//div[@class='addtocart detailaddtocart']//button")
        if in_stock_elements:
            item['in_stock'] = True
            item['available_to_checkout'] = True
        else:
            item['in_stock'] = False
            item['available_to_checkout'] = False

        if 'statusCode' in item.keys():
            if item['statusCode'] == 500:
                return item
            elif item['statusCode'] == 404:
                return item
        else:
            return {'statusCode': 200,
                    'data': item}
if __name__ == '__main__':
    # parse function call with products_url and sku :-
    event = {'sku': 'MT-COMBO',
             'pdp_url': 'https://www.kjmagnetics.com/proddetail.asp?prod=BX082CS-P-N52',
             'vendor': 'kjmagnetics'}
    print(kjmagnetics(pdp_url=event['pdp_url'], sku=event['sku']))