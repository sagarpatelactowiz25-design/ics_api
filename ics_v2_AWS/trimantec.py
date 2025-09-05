import requests
from parsel import Selector
import re

def trimantec(pdp_url, sku='sku'):
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
        if 'class="vendor"' not in response_text:
            return {'statusCode': 404, 'error_message': 'Product not found'}

        if 'class="discontinued"' in response_text:
            return {"statusCode": 410, "error_message": "Product is discontinued"}

        selector = Selector(text=response_text)
        item = {}

        # Vendor Extracting
        item['vendor'] = 'trimantec'

        # Sku Extracting
        try:
            sku1 = selector.xpath('//select[@data-section="product-template"]//option/@data-sku').getall()
            if sku1:
                sku = sku1[-1].strip()
                if sku.startswith('-'):
                    sku = sku[1:]
            else:
                sku_elem = selector.xpath('//h1[@itemprop="name"]/text()').get()
                if sku_elem:
                    parts = sku_elem.strip().split('-')
                    if len(parts) > 1:
                        scrapped_sku = parts[-1].strip()
                        if re.search('[a-zA-Z]', scrapped_sku) and re.search('[0-9]', scrapped_sku):
                            sku = re.sub(r'\(MOQ.*?\)', '', scrapped_sku)
                            sku = sku.strip()
                            if sku != sku:
                                return {'statusCode': 404, 'error_message': f"Scraped SKU:{scrapped_sku} does not match input SKU:{sku}"}
        except Exception as e:
            return {'statusCode': 500, 'error_message': "Error occurred while extracting SKU: " + str(e)}

        # Pdp_url Extracting
        item['sku'] = sku
        item['pdp_url'] = pdp_url

        # Price Extraction
        item_price = []

        price1 = selector.xpath('//div[@class="selection-wrapper price product-single__price-product-template"]//span[contains(text(),"$")]//text()').get('')
        pro_name = selector.xpath('//div[@class="purchase-box "]//div[@class="product-title"]//h1//text()').get()
        if '(MOQ' in pro_name:
            # Extracting product name to get SKU unit
            pre_pn1 = pro_name.split('(')[1].strip()
            sku_unit = ' '.join(re.findall('\d+', pre_pn1)).strip()
            price2 = price1.replace('$', '').replace(',', '').strip()
            final_price = float(sku_unit) * float(price2)
            final_price = round(final_price, 3)
            item_price.append({'currency': 'USD', 'min_qty': 1, 'price': final_price})
        else:
            final_price1 = price1.replace('$', '').replace(',', '').strip()
            final_price1 = round(float(final_price1), 3)
            item_price.append({'currency': 'USD', 'min_qty': 1, 'price': float(final_price1)})

        quantity = selector.xpath(
            '//div[@class="quantity-select quantity-select-product-template"]//input[@class="quantity"]/@value').get('')
        if quantity:
            final_quantity = quantity.strip()
        else:
            final_quantity = '1'
            item['min_qty'] = final_quantity
            item['price_string'] = 'Call for price'

        if not item_price:
            item_price = None
        item['price'] = item_price


        # Lead Time Extraction
        item['lead_time'] = None  # Lead time not available in this case

        # In Stock Extraction
        instock1 = selector.xpath('//div[@class="button-wrapper default-cart-button"]//span[contains(text(),"Add")]')
        if instock1:
            item['in_stock'] = True
            item['available_to_checkout'] = True
        else:
            item['in_stock'] = False
            item['available_to_checkout'] = False

        return {'statusCode': 200, 'data': item}
    except Exception as e:
        return {'statusCode': 500, 'error_message': "An unexpected error occurred: " + str(e)}

# if __name__ == '__main__':
#     event = {'sku': 'PP6',
#              'pdp_url': 'https://trimantec.com/products/airtac-pp-push-lock-pneumatic-fitting-plug-pp6',
#              'vendor': 'trimantec'}
#     print(trimantec(pdp_url=event['pdp_url'], sku=event['sku']))
