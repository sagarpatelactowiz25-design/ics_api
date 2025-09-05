import requests
from parsel import Selector
import re
import datetime
import hashlib


def parse(response, url, sku):
    error = {}
    try:
        data1 = response.text
        if 'class="productDetail--info"' not in response.text:
            try:
                # response = requests.get(url)
                # if 'class="productDetail--info"' not in response.text:
                #     response = requests.get(url)
                #     if 'class="productDetail--info"' not in response.text:
                #         error['statusCode'] = 404
                #         error['error_message'] = 'Product not found'
                #         error['response'] = reponse.text
                #         return error
                #     else:
                #         data1 = response.text
                # else:
                #     data1 = response.text
                error['statusCode'] = 410
                error['error_message'] = 'Product not found'
                # error['response'] = response.text
                error['response_status'] = response.status_code
                return error
            except Exception as e:
                print(e)
        ss = Selector(data1)

        data = {}
        data['vendor'] = "mrosupply"

        sku1 = ss.xpath(
            '//*[contains(@class,"flex-table")]//*[contains(text(),"SKU") or contains(text(),"sku")]//parent::div//following-sibling::div//text()').getall()
        if sku1:
            sku2 = ' '.join(sku1).strip()
            data['sku'] = sku2
            if sku.strip() != data['sku'].strip():
                error['statusCode'] = 410
                # error['response'] = response.text
                error['response_status'] = response.status_code
                error['error_message'] = f"Scraped SKU:{data['sku']} does not match input SKU:{sku}"
                return error

        else:
            data['sku'] = None
            if not data['sku']:
                error['statusCode'] = 500
                # error['response'] = response.text
                error['response_status'] = response.status_code
                error['error_message'] = "Error while scraping SKU"
                return error

        data['pdp_url'] = url

        min_qt = ss.xpath('//*[contains(@class,"a-icon a-icon-info ")]/following-sibling::strong/text()').get('')
        if min_qt:
            min_d = ' '.join(re.findall(r'\d+', min_qt)).strip()
            if min_d:
                min_qty = min_d
            else:
                min_qty = 1
        else:
            min_qty = 1
        estimated = ss.xpath('//*[contains(@class,"muted reset")]//text()').getall()
        if estimated:
            estimated_list = []
            est = ' '.join(estimated).strip().split(': ')[1].strip()
            try:
                min_qty = int(min_qty)
            except:
                min_qty = min_qty
            if est:
                estimated_list.append({
                    'min_qty': min_qty,
                    'time_to_ship': {
                        'raw_value': est
                    }
                })

            price_list = []

            pricing_loaders = {}

            pricing_loaders['currency'] = "USD"

            if min_qty:
                pricing_loaders['min_qty'] = min_qty
            else:
                pricing_loaders['min_qty'] = '1'

            price1 = ss.xpath('//div[contains(@class,"card--pricing")]//*[@class="price"]//text()').getall()
            if price1:
                price2 = ' '.join(price1).strip()
                if not "call" in price2.lower() and '$' in price2.lower():
                    extracted_values = ' '.join(re.findall(r'\$(\d+(?:,\d+)*\.\d+)', price2)).strip()
                    pricing_loaders['price'] = float(str(extracted_values).replace(',', '').strip())
                else:
                    pricing_loaders['price_string'] = 'Call for price'.capitalize()
                    # pricing_loaders['price'] = 0
            else:
                pricing_loaders['price_string'] = 'Call for price'.capitalize()
                # pricing_loaders['price'] = 0
            price_list.append(pricing_loaders)

            data['price'] = price_list

            instock1 = ss.xpath(
                '//div[contains(@class,"card--pricing")]//button[contains(@class,"product")]//text()').getall()
            if instock1:
                ins = ' '.join(instock1).strip().lower()
                if 'add to cart' in ins:
                    instock = True
                else:
                    instock = False
            else:
                instock = False

            data['available_to_checkout'] = instock
            data['in_stock'] = instock

            if estimated_list:
                data['lead_time'] = estimated_list
            else:
                data['lead_time'] = None
        return data

    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = "Internal error: " + str(e)
        # error['response'] = response.text
        error['response_status'] = response.status_code
        return error


def mrosupply(url, sku=None):
    try:
        response = requests.get(url)
    except:
        response = requests.get(url)

    failed_response = []
    if response.status_code != 200:
        for k_ in range(0, 5):
            utctime = datetime.datetime.now(datetime.timezone.utc).timestamp()
            request_id = hashlib.sha256((sku + str(utctime)).encode()).hexdigest()
            response = requests.get(url)
            if response.status_code == 200:
                break

    if response.status_code == 200:
        final_item_dict = parse(response, url, sku)
        if 'statusCode' in final_item_dict.keys():
            if final_item_dict['statusCode'] == 500:
                return final_item_dict
            elif final_item_dict['statusCode'] == 410:
                return final_item_dict
            elif final_item_dict['statusCode'] == 408:
                return final_item_dict
        else:
            return {'statusCode': 200,
                    'data': final_item_dict}
    elif response.status_code==404:
        return {'statusCode': 410,
         'error_message': 'Product not found'
         }
    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host',
                'response': failed_response
                }

# if __name__ == '__main__':
#     event={"pdp_url": "https://www.mrosupply.com/bearings/10001_uest207-23tc_ami-bearings/", "sku": "10001", "vendor": "mrosupply"}
# 
#     print(mrosupply(event['pdp_url'],event['sku']))