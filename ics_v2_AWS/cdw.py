import re
import json
import requests
from parsel import Selector

max_retires = 5


def lead_time(sku, url):  # lead_time function for requests :-
    # estimated_lead_time_url :-
    estimated_lead_time_url = 'https://www.cdw.com/api/product/1/data/getshippingmessage'
    # headers :
    headers = {
        'authority': 'www.cdw.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.cdw.com',
        'referer': url,
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    # Payload :-
    data = {
        'ProductsInfo[0][ProductCode]': f'{sku}',
        'ProductsInfo[0][DropShip]': '',
        'ProductsInfo[0][ProductClass]': '',
        'ProductsInfo[0][Source]': '',
        'ProductsInfo[0][Quantity]': '',
        'ToZipCode': '',
    }
    for i in range(max_retires):
        # requests to get json :-
        response = requests.request("POST", estimated_lead_time_url,
                                    headers=headers,
                                    data=data)
        if response.status_code == 200:
            # json load for estimated lead time extracting :-
            data1 = json.loads(response.text)
            # return dictionary :-
            return data1


def cdw(pdp_url, sku='sku'):
    error = {}
    # request to pdp_url :-
    url_request = str()
    for i in range(max_retires):
        url_request = requests.get(url=pdp_url)
        if url_request.status_code == 200:
            break
    if url_request.status_code == 200:
        pass
    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'
                }
    if 'class="productRight vertical-by-stack"' not in url_request.text:
        error['statusCode'] = 410
        error['error_message'] = 'Product not found'
        return error

    response = Selector(url_request.text)

    shipping = re.findall('"Shipping.*?,', url_request.text)

    key_value = dict()
    for i in re.findall('"Shipping.*?,', url_request.text):
        key_value[i.replace('"', '').split(':')[0]] = i.replace('"', '').split(':')[1][:-1]

    # define dictionary for making data dictionary :-
    item = dict()

    # vendor Extracting :-
    item['vendor'] = 'cdw'

    # sku Extracting :-
    try:
        item['sku'] = response.xpath(
            '//div[@class="primary-product-part-numbers"]//span[@itemprop="sku"]//text()').get().strip()

        if not item['sku']:
            item['sku'] = response.xpath(
                '//div[@class="primary-product-part-numbers"]//span[@itemprop="mpn"]//text()').get().strip()

        if item['sku'] != sku:
            error['statusCode'] = 410
            error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
            return error

    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = "Internal error: " + str(e)
        return error

    # pdp_url Extracting :-
    item['pdp_url'] = pdp_url

    # Price Extracting :-
    item_price = dict()

    item_price['min_qty'] = 1

    price_main = response.xpath('//span[@class="price"]//span//text()').get()
    if price_main == 'Request Pricing' or price_main == None:
        if response.xpath('//div[@class="ui-messageselector"]//p//text()'):
            item_price['price_string'] = 'Call for price'.capitalize()
        else:
            item_price['price_string'] = 'Call for price'.capitalize()
    else:
        price_float = price_main.replace('$', '').replace(',', '')
        price_float_1 = price_main.replace('$', '').replace(',', '')
        if price_float_1 != 'Request Pricing':
            item_price['price'] = float(price_float)
            item_price['currency'] = 'USD'
    price_list = list()
    price_list.append(item_price)
    item['price'] = price_list

    # available_to_checkout Extracting :-
    available_to_checkout = response.xpath('//div[@class="addtocart-container"]//button[@type="submit"]//text()').get()
    if available_to_checkout == None:
        item['available_to_checkout'] = False
    else:
        item['available_to_checkout'] = True

    # in_stock Extracting :-
    if "message availability in-stock" in url_request.text:
        item['in_stock'] = True
    else:
        item['in_stock'] = False

    # Lead_time request function and return json :-
    if 'This item was discontinued on' not in url_request.text:
        if sku != 'sku':
            data = lead_time(sku=sku, url=pdp_url)
        else:
            data = lead_time(sku=item['sku'], url=pdp_url)

        # Extracting lead_time :-
        estimated_lead_time = list()

        # if data and False if data["ProductShippingMessage"] == [] else data["ProductShippingMessage"][0]["DropshipEdcShouldCallUps"]==True :
        if data and False if data["ProductShippingMessage"] == [] else True:
            estimated_lead_time_text_list = list()
            estimated_lead_time_result = list()
            con = False
            for iii in data['ProductShippingMessage']:
                for key in iii:
                    if key == 'Arrival':
                        for i in data['ProductShippingMessage'][0][key]:
                            if data['ProductShippingMessage'][0][key][i] != None:
                                estimated_lead_time_text_list.append(data['ProductShippingMessage'][0][key][i].strip())
                                con = True
                    if key == 'Destination' or key == 'Urgency':
                        if con:
                            for i in data['ProductShippingMessage'][0][key]:
                                if data['ProductShippingMessage'][0][key][i] != None:
                                    try:
                                        if i == 'UtcDifference':
                                            if data['ProductShippingMessage'][0][key]['UtcDifference'] != None:
                                                cutoffhours = int(
                                                    data['ProductShippingMessage'][0]['Urgency']['CutoffHour'])
                                                setting_time = cutoffhours - int(key_value['ShippingCutoffHour'])
                                                total_hours = int(
                                                    key_value['ShippingHoursLeft'].split(' ')[1]) + setting_time
                                                within_time_list = key_value['ShippingHoursLeft'].split(' ')
                                                within_time_list[1] = str(total_hours)
                                                estimated_lead_time_text_list.append(" ".join(within_time_list))
                                                break
                                    except Exception as e:
                                        error['statusCode'] = 500
                                        error['error_message'] = "Internal error: " + str(e)
                                        return error

                                    estimated_lead_time_text_list.append(
                                        data['ProductShippingMessage'][0][key][i].strip())
            if estimated_lead_time_text_list:
                estimated_lead_time_str = " ".join(estimated_lead_time_text_list)
                if 'today' in estimated_lead_time:
                    estimated_lead_time_result_1 = {"min_qty": 1,
                                                    "time_to_arrive": {"raw_value": f"{estimated_lead_time_str}"}}
                else:
                    estimated_lead_time_result_1 = {"min_qty": 1,
                                                    "time_to_stock": {"raw_value": f"{estimated_lead_time_str}"}}
                estimated_lead_time_result.append(estimated_lead_time_result_1)
                # estimated_lead_time_result_final_1 = str(estimated_lead_time_result)
                estimated_lead_time_result_final = json.dumps(estimated_lead_time_result, ensure_ascii=False)
                estimated_lead_time = estimated_lead_time_result_final

            if not estimated_lead_time_result:
                for iii in data['ProductShippingMessage']:
                    estimated_lead_time = iii['Shipsinshippingmessage']
                    if estimated_lead_time == '':
                        if "requestQuote" in url_request.text:
                            estimated_lead_time = ''
                        else:
                            estimated_lead_time = response.xpath(
                                '//input[@name="CartItems[0].ProductInventory.ShippingStatusMessage"]//@value').get().strip()
                            if estimated_lead_time:
                                if 'today' in estimated_lead_time:
                                    estimated_lead_time_result_1 = {"min_qty": 1,
                                                                    "time_to_arrive": {
                                                                        "raw_value": f"{estimated_lead_time}"}}
                                else:
                                    estimated_lead_time_result_1 = {"min_qty": 1,
                                                                    "time_to_stock": {
                                                                        "raw_value": f"{estimated_lead_time}"}}
                                estimated_lead_time_result.append(estimated_lead_time_result_1)
                                # estimated_lead_time_result_final_1 = str(estimated_lead_time_result)
                                estimated_lead_time_result_final = json.dumps(estimated_lead_time_result,
                                                                              ensure_ascii=False)
                                estimated_lead_time = estimated_lead_time_result_final
                            else:
                                estimated_lead_time = None
                    else:
                        if estimated_lead_time:
                            if 'today' in estimated_lead_time:
                                estimated_lead_time_result_1 = {"min_qty": 1,
                                                                "time_to_arrive": {
                                                                    "raw_value": f"{estimated_lead_time}"}}
                            else:
                                estimated_lead_time_result_1 = {"min_qty": 1,
                                                                "time_to_stock": {
                                                                    "raw_value": f"{estimated_lead_time}"}}
                            estimated_lead_time_result.append(estimated_lead_time_result_1)
                            # estimated_lead_time_result_final_1 = str(estimated_lead_time_result)
                            estimated_lead_time_result_final = json.dumps(estimated_lead_time_result,
                                                                          ensure_ascii=False)
                            estimated_lead_time = estimated_lead_time_result_final
                        else:
                            estimated_lead_time = None

        # appends lead_time to item dictionary :-
        item['lead_time'] = json.loads(estimated_lead_time) if isinstance(estimated_lead_time,
                                                                          str) else estimated_lead_time

    else:
        item['lead_time'] = None

    if item['lead_time'] == []:
        item['lead_time'] = None

    if 'statusCode' in item.keys():
        if item['statusCode'] == 500:
            return item
        elif item['statusCode'] == 410:
            return item
        elif item['statusCode'] == 408:
            return item
    else:
        return {'statusCode': 200,
                'data': item}


# if __name__ == "__main__":
#     # event = {
#     #     "pdp_url": "https://www.cdw.com/product/apc-by-schneider-electric-power-cord-kit-6-ea-locking-c13-to-c14-1.8m/3068504?pfm=srh",
#     #     "sku": "3068504",
#     #     "vendor": "cdw",
#     # }
#     event = {
#         "pdp_url": "https://www.cdw.com/product/panduit-industrialnet-din-rail-shelf-4u/5101482",
#         "sku": "510148",
#         "vendor": "cdw",
#     }
#     print(json.dumps(cdw(event["pdp_url"], event["sku"])))