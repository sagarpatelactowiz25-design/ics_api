import json# install json
# import requests# intall requests
from parsel import Selector # intsall parsel
import re
from curl_cffi import requests# intsall curl_cffi
max_retires = 5

def coleparmer(pdp_url,product_sku,vendor="coleparmer"):
    try:
        url_request=''
        error={}

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        item={}
        for i in range(max_retires):
            url_request = requests.get(url=pdp_url,headers=headers,impersonate = "chrome110")
            if url_request.status_code == 200:
                break
            else:
                return {"statusCode": 404,
                        "error_messeage": "Product not found"}
        

        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}

        response = Selector(text=url_request.text)

        dis = response.xpath('//div[@class="container"]//ul[@class="breadcrumbs"]//text()').getall()
        dis = ''.join(dis)
        if 'Discontinued' in dis:

            return {"statusCode":410,
                    "error_messeage":"Product is discontinued"}

        if 'class="eb-sku"' not in url_request.text:
            error['statusCode'] = 404
            error['error_message'] = 'Product not found'
            return error

        item['vendor'] = vendor
        item['pdp_url'] = pdp_url


        try:
            sku = response.xpath('//div[@class="sku-item-block"]//span[@itemprop="sku"]//text()').get().strip()
            sku_value1 = re.findall(r'\d+', sku)
            sku_value = ''.join(sku_value1).strip()
            item['sku'] =sku
            if item['sku'] != product_sku:
                error['statusCode'] = 404
                error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{product_sku}"
                return error
            else:
                pass
        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = str(e)
            return error

        # EXTRACTING THE price USING XPATH
        price_list = []
        price = response.xpath('//div[@class="main-price"]/span[@itemprop="price"]/@content').get()
        if price != None:
            if price == '0.00':
                price_list.append({
                    'min_qty': 1,
                    'price_string': 'Call For Price'
                })
            else:
                price.replace(",", "")
                price_list.append({
                    "currency": "USD",
                    'min_qty': 1,
                    'price': float(price)
                })
        else:
            price_list.append({
                'min_qty': 1,
                'price_string': 'Call For Price'
            })

        if price_list:
            item['price'] = price_list
        else:
            item['price'] = None
        available_to_checkout = response.xpath('//div//a[contains(text(),"Add To Cart")]//text()').get()
        if available_to_checkout != None:
            available_to_checkout = True if "Cart" in available_to_checkout else False

        json_data = {'skusWithComma': sku_value, }
        try:
            respons = requests.post('https://www.coleparmer.com/Shared/GetProductInventory',
                                    impersonate = "chrome110",
                                    json=json_data)
            respons = respons.json()
            time_to_ship = respons["ProductServiceResposeModel"][0]["AvailabilityDto"]["Message"]
            estimated_lead_time = []
            if "Ships" in time_to_ship or "Days" in time_to_ship:
                estimated_lead_time.append({"min_qty": 1, "time_to_ship": {"raw_value": time_to_ship.strip()}})
                in_stock = False
            elif "Stock" in time_to_ship:
                in_stock = True
                estimated_lead_time=None
            else:
                in_stock = False
                estimated_lead_time = None
        except:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}


        item['lead_time'] = estimated_lead_time
        item['available_to_checkout'] = available_to_checkout
        item['in_stock'] = in_stock


        if item['lead_time'] == []:
            item['lead_time'] = None
        return {'statusCode': 200,
                'data': item}
    except Exception as e:
        print(e)
        return {'statusCode': 408,
        'error_message': 'Request timeout, failed to reach host'}

# if __name__ == '__main__':
#     product_sku = 'EW-12917-01'
#     pdp_url = 'https://www.coleparmer.com/i/kinesis-kx-syringe-filter-pvdf-4-mm-dia-0-45-m-1000-pk/1291701'
#
#     print(json.dumps(coleparmer(pdp_url, product_sku)))