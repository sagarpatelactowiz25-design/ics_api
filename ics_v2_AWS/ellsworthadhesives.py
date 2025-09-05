import json
import time
import requests
from parsel import Selector
import re
max_entries = 5

def ellsworthadhesives(pdp_url,product_sku,vendor="ellsworthadhesives"):
    try:
        url = pdp_url
        # Maximum retries for urls and checking the status code is 200 or not.
        for i in range(max_entries):
            url_request = requests.get(url=pdp_url)
            if url_request.status_code == 200:
                break
        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}

        # Checking if status code and the product name  is also in the response text
        if url_request.status_code == 200:
            response = Selector(text = url_request.text)
            if response.xpath('//h1/span[@itemprop="name"]/text()').get():  # Product name
                # Extracting sku
                scraped_sku = response.xpath('//div[@class="col-lg-12 prd-num"]/span[@itemprop="sku"]/text()').get()
                if scraped_sku != product_sku:
                    return {"statusCode": 404,
                            "error_message": f"Scraped SKU:{scraped_sku} does not match input SKU:{product_sku}"}
                else:
                    discontinued_text = response.xpath('//div[@id="PanelNoPricing"]/p//text()').getall()
                    if discontinued_text and "discontinued" in "".join(discontinued_text):
                        return  {"statusCode": 410,
                        "error_message": "Product is discontinued"}
                    else:
                        # In stock checking and Availble to checkout
                        in_stock_checking = response.xpath('//div[@class="col-xs-6 col-md-4"]/a[contains(text(),"Add to Cart")]')
                        if in_stock_checking:
                            in_stock = True
                            available_to_checkout = True
                        else:
                            in_stock = False
                            available_to_checkout = False

                        # estimate_lead_time
                        estimate_list = []
                        estimate_string = ''.join(response.xpath(
                            '//div[@class="row clearfix"]/div[@class="col-xs-12 col-md-12 shipping-notes"]//li[not(@class="bold")]/text()').getall()).strip()
                        if 'day' in estimate_string.lower() or 'week' in estimate_string.lower() or 'month' in estimate_string.lower():
                            estimate_list.append({'min_qty': 1, 'time_to_ship': {"raw_value": estimate_string.strip()}})
                        estimate_lead_time =  estimate_list if estimate_list else None

                        # price
                        price_list =[]
                        pricing_sel = response.xpath('//tr[@itemprop="offers"]')
                        if pricing_sel:
                            for price_info in pricing_sel:
                                try:
                                    if '-' in price_info.xpath('.//span[@itemprop="eligibleQuantity"]/text()').get():
                                        qty = int(
                                            price_info.xpath('.//span[@itemprop="eligibleQuantity"]/text()').get().split(
                                                '-')[0])
                                    else:
                                        qty = int(price_info.xpath('.//span[@itemprop="eligibleQuantity"]/text()').get())
                                except:
                                    qty = int(
                                        price_info.xpath('.//span[@itemprop="eligibleQuantity"]/text()').get().replace('+',
                                                                                                                       ''))
                                try:
                                    price = float(price_info.xpath('.//span[@itemprop="price"]/text()').get())
                                except:
                                    price = ''
                                if price:
                                    price_list.append({
                                        "min_qty":int(qty),
                                        "price":price,
                                        "currency": "USD",
                                    })
                                else:
                                    price_list.append({
                                            "min_qty": 1,

                                            "price_string": "Call For Price"

                                    })

                        else:
                            price_list.append({
                                "min_qty": 1,
                                "price_string": "Call For Price"

                            })

                        data = {'vendor': vendor, 'pdp_url': url, 'sku': product_sku, 'price': price_list,
                                'lead_time': estimate_lead_time, 'available_to_checkout': available_to_checkout,
                                'in_stock': in_stock}
                        return {'statusCode': 200,
                            'data': data}

            else:
                return {'statusCode': 404,
                        'error_message': 'Product not found'}

        else:
            return {'statusCode': 404,
                    'error_message': 'Product not found'}

    except Exception as e:
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}



# if __name__ == '__main__':
#     # event = {
#     #     "pdp_url": "https://www.ellsworth.com/products/dispensing-equipment-supplies/accessories/techcon-910-25-nozzle-retaining-nut/",
#     #     "sku": "910-25", "vendor": "ellsworthadhesives"}
#     event  = {
#         "pdp_url": "https://www.ellsworth.com/products/by-manufacturer/bostik/sealants/silyl-terminated-polymer/bostik-70-03a-silyl-modified-polymer-sealant-black-290-ml-cartridge/",
#         "sku": "A61019", "vendor": "ellsworthadhesives"}

#     # event = {
#     #     "pdp_url" :"https://www.ellsworth.com/products/by-manufacturer/bostik/sealants/silyl-terminated-polymer/bostik-70-03a-silyl-modified-polymer-sealant-black-290-ml-cartridge/",
#     #     "product_sku":"A61019"
#     #
#     #     # "pdp_url" :"https://www.ellsworth.com/products/dispensing-equipment-supplies/dispensing-systems-fluid/hand-held-1-part-applicators/fisnar-fmg-120t-metal-manual-dispense-kit-12-oz/",
#     #     # "product_sku":"FMG-120T"
#     # }
#     print(ellsworthadhesives(event["pdp_url"],event["sku"]))
