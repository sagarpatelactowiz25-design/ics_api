import requests
import json
import html
from parsel import Selector
import re


def skygeek(pdp_url, sku):
    error = {}
    max_retries = 5

    VENDOR_ID = 'ACT-B7-008'
    VENDOR_NAME = 'skygeek'

    # Attempt to fetch the webpage
    try:
        resp_status_code = 408
        error_msg = 'Request timeout, failed to reach host'
        for _ in range(max_retries):
            response = requests.get(pdp_url, verify=False)
            if response.status_code == 200:
                resp_status_code = 200
                error_msg = None
                break
            if response.status_code == 404:
                resp_status_code = 410
                error_msg = "Product is discontinued"
                break
                # return {"statusCode": 410, "error_message": "Product is discontinued"}
        if resp_status_code != 200:
            return {'statusCode': resp_status_code, 'error_message': error_msg}
    
        # Check if the product is available
        if 'class="productView-sku"' not in response.text:
            error['statusCode'] = 410
            error['error_message'] = 'Product not found'
            return error
    
        # Check if the product is discontinued
        if 'class="discontinued"' in response.text:
            return {"statusCode": 410, "error_message": "Product is discontinued"}
    
        # Parse HTML response
        selector = Selector(text=response.text)
        item = {}
    
        # Extract vendor
        item['vendor'] = 'skygeek'
    
        # Extract SKU
        try:
            scrapped_sku = selector.xpath('//div[@class="productView-sku"]//span[position()>1]/text()').get()
            if scrapped_sku.lower() != sku.lower():
                error['statusCode'] = 410
                error['error_message'] = f"Scraped SKU:{scrapped_sku} does not match input SKU:{sku}"
                return error
        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = "Internal server error" + str(e)
            return error
    
        # Extract PDP URL and SKU
        item['sku'] = sku
        item['pdp_url'] = pdp_url
    
        # Extracting basic data from the response
        basic_data = {
            # 'id': "url_id",
            'vendor_id': VENDOR_ID,
            'vendor_name': VENDOR_NAME,
            'pdp_url': 'pdp_url',
            'sku': 'sku'
        }
    
        stock_and_price = selector.xpath('//script[@type="text/javascript" and contains(text(), "BCData")]/text()').get()[
                          14:-2]
        stock_and_price_data = json.loads(stock_and_price)
    
        price_data_list = list()
        for multiple_price_data in selector.xpath('//div[@class="table-body"]//li'):
            price = re.findall(r'([0-9.,]+)', "".join(multiple_price_data.xpath('.//span//text()').getall()))[-1].strip().replace(',', '')
            try:
                price = float(price)
            except:
                price = float(re.findall(r'([0-9.,]+)', "".join(multiple_price_data.xpath('.//span//text()').getall()))[-2].strip().replace(',', ''))
            price_data = {
                'min_qty': int(re.findall(r'(\d+)', "".join(multiple_price_data.xpath('.//span//text()').getall()[0]))[0].strip()),
                'price': price,
                'currency': 'USD'
            }
            if price_data["price"] == '.':
                price_data['price'] = re.findall(r'([0-9.,]+)', "".join(multiple_price_data.xpath('.//span//text()').getall()))[-2].strip().replace(',', '')
            price_data_list.append(price_data)
        main_price_data = {
            'min_qty': 1,
            'currency': 'USD'
        }
        main_price_data_ = {
            'min_qty': 1
        }
        if selector.xpath('//div[@itemprop="offers"]//span[@class="price price--withoutTax "]/text()'):
            main_price_data["price"] = float(selector.xpath('//div[@itemprop="offers"]//span[@class="price price--withoutTax "]/text()').get().replace("$", "").strip().replace(',', '').strip())
            price_data_list.append(main_price_data)
        else:
            main_price_data_["price_string"] = "Call For Price"
            price_data_list.append(main_price_data_)
    
        item['price'] = price_data_list
    
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://skygeek.com',
            'referer': 'https://skygeek.com/',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }
        # headers =  {
        #     'sec-ch-ua-platform': '"Windows"',
        #     'Referer': 'https://skygeek.com/',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        #     'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        #     'sec-ch-ua-mobile': '?0',
        # }
        params = {
            'sellingSku': f'{sku}',
        }
    
    
        try:
            for _ in range(max_retries):
                response = requests.get(
                    'https://api.skygeek.com/PublicApis/api/v0/SkyGeekDotComApi/SellingSkuData',
                    params=params,
                    headers=headers,
                    timeout=2
                )
    
                if response.status_code == 200:
                    break
                else:
                    return {'statusCode': 408, 'error_message': 'Request timeout, failed to reach host'}
                # Extract lead time
            lead_time_data = json.loads(response.text)
            new_html = lead_time_data['availabilityHtml']
            lead_time_html = Selector(lead_time_data["availabilityHtml"])
            estimated_lead_time = [{
                'min_qty': 1,
                'time_to_stock': {
                    'raw_value': html.unescape(re.sub(r'\s+', ' ', " ".join(lead_time_html.xpath('(//div)[2]//text()').getall()).strip()).split(':')[-1].strip())
                }
            }]
            if estimated_lead_time[0]["time_to_stock"]["raw_value"] =='':
                estimated_lead_time = [{
                    'min_qty': 1,
                    'time_to_stock': {
                        'raw_value': re.findall(r'>(.*?)<', new_html)[0]
                    }
                }]
            if estimated_lead_time[0]["time_to_stock"]["raw_value"]:
                item['lead_time']= estimated_lead_time
            else:
                item['lead_time'] = None
        except:
            item['lead_time'] = None
    
        # Extract availability
    
        stock_and_price = selector.xpath('//script[@type="text/javascript" and contains(text(), "BCData")]/text()').get()[14:-2]
        stock_and_price_data = json.loads(stock_and_price)
        in_stock = True if stock_and_price_data["product_attributes"]["purchasable"] else False
        item["in_stock"] = in_stock
        if in_stock == False:
            item["available_to_checkout"] = False
        else:
            item["available_to_checkout"] = True
        return {'statusCode': 200, 'data': item}
    except Exception as ee:
        return {'statusCode': 408, 'error_message': 'Request timeout, failed to reach host'}


# if __name__ == '__main__':
#     pdp_url = "https://skygeek.com/socomore-aeroglaze-9924a-qt.html"

#     sku = "SGP205240"
    # event = {"sku": "SGP26604", "vendor": "skygeek", "pdp_url": "https://skygeek.com/25w.html"}
    # print(skygeek(event["pdp_url"], event['sku']))