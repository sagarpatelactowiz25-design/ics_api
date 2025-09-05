import json
import time
import requests
from parsel import Selector
import re
max_entries = 5


def tacomascrew(pdp_url,product_sku, vendor="tacomascrew"):
    url = pdp_url
    try:
        cookies = {
            'CurrentLanguageId': 'a26095ef-c714-e311-ba31-d43d7e4e88b2',
            'SetContextLanguageCode': 'en-us',
            'CurrentCurrencyId': '30b432b9-a104-e511-96f5-ac9e17867f77',
            'SetContextPersonaIds': 'd06988c0-9358-4dbb-aa3d-b7be5b6a7fd9',
            'InsiteCacheId': '26489313-4b2d-464f-9f31-a09bd9a63f46',
            'FirstPage': 'false',
            '_gid': 'GA1.2.1140285464.1712834461',
            'CurrentFulfillmentMethod': 'Ship',
            'CurrentPickUpWarehouseId': '664fd364-efc6-40ad-9a1f-ab9800d1fa32',
            '_dc_gtm_UA-38296018-1': '1',
            '_ga': 'GA1.2.2086021197.1712834461',
            '_ga_XZLHCD4MQE': 'GS1.1.1712834460.1.1.1712835540.0.0.0',
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        # Maximum retries for urls and checking the status code is 200 or not.
        for i in range(max_entries):
            url_request = requests.get(url=pdp_url,headers=headers)
            if url_request.status_code == 200:
                response = Selector(text=url_request.text)
                break
        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}

        # Checking if status code and the product name  is also in the response text
        if url_request.status_code == 200 and response.xpath('//h1[@class="product-name"]'):
            response = Selector(text=url_request.text)
            # Executing Product_Id using json
            params = {
                'path': url.replace("https://www.tacomascrew.com", "")
            }
            time.sleep(1)
            for i in range(max_entries):
                product_id_response = requests.get('https://www.tacomascrew.com/api/v1/catalogpages', params=params,headers=headers)
                if product_id_response.status_code == 200:
                    product_id_json_load = json.loads(product_id_response.text)
                    product_id = product_id_json_load["productId"]
                    category_id = product_id_json_load["category"]["id"]
                    break

            # Extracting sku from json
            sku_request = requests.get(
                f'https://www.tacomascrew.com/api/v1/products/{product_id}?addToRecentlyViewed=true&applyPersonalization=true&categoryId={category_id}&expand=documents,specifications,styledproducts,htmlcontent,attributes,crosssells,pricing,relatedproducts,brand&getLastPurchase=true&includeAlternateInventory=true&includeAttributes=IncludeOnProduct,NotFromCategory&replaceProducts=false'
                ,headers=headers
                )
            sku_response = json.loads(sku_request.text)
            sku = sku_response["product"]["sku"]

            if sku != product_sku:
                return {"statusCode": 410,
                        "error_message": f"Scraped SKU:{sku} does not match input SKU:{product_sku}"}
            else:

                # json response for instock and unit
                instock_json_data = {
                    'productIds': [
                        product_id,
                    ],
                }
                instock_response = requests.post('https://www.tacomascrew.com/api/v1/realtimeinventory',
                                                 cookies=cookies,
                                                 headers=headers,
                                                 json=instock_json_data)
                time.sleep(2)
                instock_json_load = json.loads(instock_response.text)
                # Executing unit from josn
                try:
                    unit = instock_json_load['realTimeInventoryResults'][0]["inventoryAvailabilityDtos"][0][
                        "unitOfMeasure"]
                except:
                    unit = 'EA'

                # Executing minimum quantity
                minimum_quantity = (
                    response.xpath('//div[@ng-show="vm.isQuantityVisible()"]/input/@value').get())
                if minimum_quantity:
                    minimum_quantity = int(minimum_quantity)
                else:
                    minimum_quantity = 1
                # Executing price using json

                price_json_data = {
                    'productPriceParameters': [
                        {
                            'productId': product_id,
                            'unitOfMeasure': unit,
                            'qtyOrdered': 1,
                        },
                    ],
                }
                time.sleep(2)
                price_response_data = requests.post('https://www.tacomascrew.com/api/v1/realtimepricing',
                                                    headers=headers, json=price_json_data)
                if price_response_data.status_code == 200:
                    try:
                        price_json_load = json.loads(price_response_data.text)
                        price = price_json_load["realTimePricingResults"][0]["unitRegularPriceDisplay"]
                        price = re.findall(r'[\d.]+', price.replace(',', ''))[0]
                        price = [{'min_qty': minimum_quantity, 'price': float(price), 'currency': 'USD'}]
                    except:
                        return {"statusCode": 408,
                                "error_message": "The error message indicates a timeout issue where the price couldn't be found due to JSON not being loaded."}
                else:
                    price = [{'min_qty': minimum_quantity, 'price_string': "Call For Price".capitalize()}]

                # Executing estimate_lead_time and available_to_checkout and in_stock using xpath and json
                script_text = " ".join(response.xpath('//script[@type="text/ng-template"]//text()').getall())
                response_text = Selector(text=script_text)
                inventory_not_available = response_text.xpath('//div[@ng-if="failedToGetRealTimeInventory"]/span[contains(text(),"Inventory Not Available")]')
                if price == [{'min_qty': minimum_quantity, 'price_string': "Call For Price".capitalize()}] and inventory_not_available:
                    in_stock = False
                    available_to_checkout = False
                else:
                    add_to_cart = response_text.xpath(
                        '//div[@class="actions-block"]//div[@class="action"]/button[text()="Add to Cart"]')
                    available_to_checkout = True if add_to_cart else False

                    if instock_response.status_code == 200:

                        message = instock_json_load["realTimeInventoryResults"][0]["inventoryAvailabilityDtos"][0][
                            "availability"][
                            "message"]
                        if message == "In Stock" or message == "Low Stock":
                            in_stock = True
                        else:
                            in_stock = False
                    else:
                        in_stock = False

                shipping_time = response_text.xpath('//span[contains(text(),"Ships in 24 Hours")]/text()').get()
                estimate_lead_time = [{'min_qty': minimum_quantity, 'time_to_ship': {
                    'raw_value': 'Ships in 24 Hours'}}] if shipping_time else None



                # Data insert
                data = {'vendor': vendor, 'pdp_url': pdp_url, 'sku': product_sku, 'price': price,
                        'lead_time': estimate_lead_time, 'available_to_checkout': available_to_checkout,
                        'in_stock': in_stock}
                return {'statusCode': 200,
                        'data': data}

        else:
            return {'statusCode': 410,
                    'error_message': 'Product not found'}
    except Exception as e:

        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}

# if __name__ == '__main__':
#     event={"sku": "615-6011", "vendor": "tacomascrew", "pdp_url": "https://www.tacomascrew.com/Catalog/chemicals-paints/sealants-caulk/615-601"}
#     print(json.dumps(tacomascrew(event['pdp_url'],event['sku'],event['vendor'])))