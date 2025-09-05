from datetime import datetime
import json
import requests
from parsel import Selector

import api_token

scraper_api_token=api_token.scraperAPI_key
def parse(response, keyword, response_estimate, sku):
    try:
        new_response = Selector(response.text)
        # if 'data-cy="product-detail-main"' not in response.text:
        #     return {'statusCode': 410,
        #             'error_message': 'Product not found'}

        data = {}

        try:
            j_data=new_response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
            if j_data:
                new_data=json.loads(j_data)
        except:
            pass
        #prodcut discountinue status
        try:
            discontinuew=new_data['props']['pageProps']['product']['inventoryStatus']
            if discontinuew=="DISCONTINUED":
                return {'statusCode': 410,
                 "error_message": "Product is discontinued"}

        except:
            pass
        data['vendor'] = 'motionindustries'
        try:
            data['sku'] = new_data['props']['pageProps']['product']['id']
        except:
            data['sku'] = None

        data['pdp_url'] = keyword

        try:
            price_ = new_data['props']['pageProps']['product']['price']
            minimum_qty =  new_data['props']['pageProps']['product']['minimumPurchaseQuantity']
            price_list = []
            if price_:
                price = price_
                price_text = {
                    "min_qty": minimum_qty,
                    "price": float(price),
                    "currency": "USD"
                }
                price_list.append(price_text)
                data['price'] = price_list
            else:
                price_text = {
                    "min_qty": 1,
                    "price_string": "Call for Price"
                }
                price_list.append(price_text)
                data['price'] = price_list
        except:
            data['price'] = None
        try:
            check_instock_status = new_response.xpath('//button[@data-testid="add-to-cart"]/span/text()').get().lower()
            if check_instock_status:
                data['available_to_checkout'] = True
                data['in_stock'] = True
            else:
                data['available_to_checkout'] = False
                data['in_stock'] = False
            if 'quote' in check_instock_status:
                data['available_to_checkout'] = False
                data['in_stock'] = False

        except:
            data['available_to_checkout'] = False
            data['in_stock'] = False
        try:
            estimate_json = json.loads(response_estimate.text)
            date_parse_ = estimate_json['leadTime']
        except:
            date_parse_ = ''

        est = list()
        if date_parse_:
            date_obj = datetime.strptime(date_parse_, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %B %d")
            est.append({
                "min_qty": minimum_qty,
                "time_to_arrive": {
                    "raw_value": f'Estimated to arrive on {formatted_date}'
                }
            })
        if est == []:
            est = None
        else:
            pass
        data['lead_time'] = est
        return data
    except Exception as e:
        return {
                'statusCode': 500,
                'error_message': 'Internal server error' + str(e)
        }


def motionindustries(pdp_url, sku,vendor='motionindustries'):
    try:
        url = pdp_url
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')
        # proxy = {
        #     "http": 'http://keep_headers=false:{scraper_api_token}@proxy-server.scraperapi.com:8001',
        #     "https": 'http://keep_headers=false:{scraper_api_token}@proxy-server.scraperapi.com:8001'
        # }

        try:
            response = requests.get(f'http://api.scraperapi.com/?api_key={scraper_api_token}&url={url}',verify=False, timeout=40)
        except:
            response = requests.get(f'http://api.scraperapi.com/?api_key={scraper_api_token}&url={url}', verify=False, timeout=40)
        if response.status_code != 200:
            for k_ in range(0, 5):
                response = requests.get(f'http://api.scraperapi.com/?api_key={scraper_api_token}&url={url}', verify=False, timeout=40)
                if response.status_code == 200:
                    break

        # todo of estimate response
        try:
            scraped_sku = url.split('/sku/')[1]
        except:
            scraped_sku = ''
        if scraped_sku:
            if sku.strip() != scraped_sku.strip():
                return {'statusCode': 410,
                        'error_message': f'Scraped SKU:{scraped_sku} does not match input SKU:{sku}'}
        else:
            return {'statusCode': 500,
                    'error_message': 'SKU error, SKU is None'}
        if 'Shipping time may vary. Motion rep will advise' in response.text:
            response_estimate={"leadTime": None}
            final_item_dict = parse(response, url, response_estimate, sku)
            return {'statusCode': 200,
                    'data': final_item_dict}
        try:
            lead_url=f'http://api.scraperapi.com/?api_key={scraper_api_token}&url=https://www.motion.com/api/shipping/delivery-estimate?postalCode=10001&items[0][id]={scraped_sku}&items[0][manufacturerControlNumber]=00825&items[0][groupSerial]=B05450&items[0][quantity]=1'
            # response_estimate = requests.get(f'https://www.motion.com/misvc/mi/services/json/Availability.AvailabilityTransitTime?miLoc=EB99&customerNo=96000001&mfrCtlNo=00820&groupSerial=A00002&itemNo={sku}&prodGroupNo=1511&orderCtlNo=&orderSourceCd=&orderLineNo=&cmpntLineNo=&qty=1&zip=35210&requestedDate={formatted_date}',headers=headers,proxies=proxy,verify=False,timeout=40)
            response_estimate = requests.request("GET",lead_url,timeout=40)
        except:
            response_estimate = requests.request("GET",lead_url,verify=False,timeout=40)
        if response_estimate.status_code != 200:
            for k_ in range(0, 5):
                response_estimate = requests.request("GET",lead_url,timeout=40)
                if response_estimate.status_code == 200:
                    break
        # todo  end of estimate response
        if response.status_code == 200 and response_estimate.status_code == 200:
            final_item_dict = parse(response, url, response_estimate, sku)

            return {'statusCode': 200,
                    'data': final_item_dict}
        else:
            return {
                'statusCode': 408,
                'error_message': 'Request timeout, failed to reach the host'
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'error_message': 'Internal server error' + str(e)
        }

if __name__ == '__main__':
    url = 'https://www.motion.com/products/sku/00047903'
    sku = '0004790'
    # url = 'https://www.motion.com/products/sku/00001006'
    # sku = '00001006'
    #
    print(json.dumps(motionindustries(url, sku, vendor='motionindustries')))