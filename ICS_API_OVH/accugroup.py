import json  # install json
from parsel import Selector  # intsall parsel
from curl_cffi import requests  # intsall curl_cff
import html

max_retires = 5


def accugroup(pdp_url, sku, vendor='accugroup'):
    try:
        if 'https://accu-components.com/' not in pdp_url:
            return {"statusCode": 410,
                    "error_message": "Product not found"}
        item = {}
        error = {}

        for i in range(max_retires):
            url_request = requests.get(pdp_url, impersonate="chrome110")
            if url_request.status_code == 404:
                error['statusCode'] = 410
                error['error_message'] = 'Product not found'
                return error
            if url_request.status_code == 200:
                break

        if url_request.status_code == 200:
            pass

        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}

        response = Selector(text=url_request.text)
        # ----------------------------------- product_sku and Pdp_url below --------------------------------
        _sku = response.xpath(
            '//div[@class="flex flex-grow flex-col"]/span/text() | //div[@class="hidden lg:block"]/span/text()').getall()
        try:
            p_sku = ''.join(_sku).replace('\n', '').replace('\r', '').replace('\t', '').strip().split(': ')[1]
        except:
            split_url = pdp_url.split('/')
            sku = split_url[-1]
            p_sku = '-'.join(sku.split('-')[1:]).strip()

        if p_sku != sku:
            return {"statusCode": 410,
                    "error_message": f"Scraped SKU:{p_sku} does not match input SKU:{sku}"}

        # ----------------------------------- product_sku and Pdp_url above --------------------------------

        # ----------------------------------- price  and in_stock below --------------------------------
        headers_price = {
            'authority': 'odelp45i07.execute-api.eu-west-1.amazonaws.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://accu-components.com',
            # 'referer': 'https://accu-components.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        params = {
            'currency': '2',
            'products': response.xpath('//div[@x-show="!loading"]/@data-bv-product-id').get(),
        }
        fdata = ''
        for jj, kk in params.items():
            fdata += f'{jj}={kk}&'
        if fdata.endswith('&'):
            fdata = fdata[:-1]
        # url1 = f'https://odelp45i07.execute-api.eu-west-1.amazonaws.com/Prod/stock-and-price?{fdata}'
        url1 = f'https://e0tup0y4lb.execute-api.eu-west-1.amazonaws.com/Prod/stock-and-price?{fdata}'
        # yield scrapy.Request(url=url1, headers=headers_price)
        response_price = requests.get(url=url1, headers=headers_price)
        price_data = response_price.text
        price_data_json = json.loads(price_data)
        # price_list = []
        final_price = []  # Initialize price_list as an empty list to store dictionaries
        # EXTRACTING THE IN STOCK AND AVAILABLE TO CHECKOUT USING JSON
        for pri_json in price_data_json:
            price_loop = pri_json['price_breaks']
            date_discontinued = pri_json['date_discontinued']
            if date_discontinued == None:
                if price_loop:
                    min_qty = pri_json['minimal_quantity']
                    price_1 = pri_json['price']
                    if price_1 != 0:
                        price_info = {"min_qty": min_qty, "price": price_1,
                                      "currency": "USD"}  # Create a dictionary for price details
                        final_price.append(price_info)  # Append the price details dictionary to the price_list
                        available_to_checkout = True
                        in_stock = True
                    else:
                        final_price.append(
                            {"min_qty": 1, "price_string": 'Call for price'})
                        available_to_checkout = False
                        in_stock = False
                    for ii in price_loop:
                        qty = ii['from_quantity']
                        final_price_val = ii['price']  # Use a different variable name for the final price value
                        if qty and final_price_val != 0:
                            min_qty = qty
                            price = final_price_val
                            available_to_checkout = True
                            in_stock = True
                            final_price.append(
                                {"min_qty": min_qty, "price": price, "currency": "USD"}, )
                        else:
                            available_to_checkout = False
                            in_stock = False
                            final_price.append(
                                {"min_qty": 1, "price_string": 'Call for price'})
                else:
                    available_to_checkout = False
                    in_stock = False
                    final_price.append(
                        {"min_qty": 1, "price_string": 'Call for price'})
            else:
                return {'statusCode': 410,
                        "error_message": "Product is discontinued"}
            # ----------------------------------- price and in_stock below --------------------------------

            # ----------------------------------- Added Lead Time belove -----------------------------------
            #     if in_stock ==True:
            #         headers = {
            #             'accept': 'application/json, text/plain, */*',
            #             'accept-language': 'en-US,en;q=0.9',
            #             'origin': 'https://accu-components.com',
            #             'referer': 'https://accu-components.com/',
            #             'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            #             'sec-ch-ua-mobile': '?0',
            #             'sec-ch-ua-platform': '"Windows"',
            #             'sec-fetch-dest': 'empty',
            #             'sec-fetch-mode': 'cors',
            #             'sec-fetch-site': 'cross-site',
            #             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            #         }
            #         lead_id = ''.join(pdp_url.split('/')[-1].split('-')[:1])
            #         params = {
            #             'currency': '2',
            #             'products': lead_id,
            #         }
            #
            #         response11 = requests.get(
            #             'https://e0tup0y4lb.execute-api.eu-west-1.amazonaws.com/Prod/stock-and-price',
            #             params=params,
            #             headers=headers,
            #         )
            #         estimated_lead_time = list()
            #         for i in json.loads(response11.text):
            #             quantity = i['quantity']
            #             total_minutes = i['express_cutoff']
            #             hours = int(total_minutes // 60)
            #             minutes = int(total_minutes % 60)
            #             main_estimated = f"Ships today - Order in {hours} hours & {minutes} minutes"
            #             if main_estimated and quantity != 0:
            #                 lead_time1 = {'raw_value': main_estimated}
            #                 min_qty_1 = int(quantity)
            #                 estimated_lead_time.append(
            #                     {
            #                         'min_qty': min_qty_1,
            #                         'time_to_arrive': html.unescape(lead_time1)
            #                     }
            #                 )
            #
            #             ex_lead_time = i['ex_lead_time']
            #             ex_stock = i['ex_stock']
            #             str_ex_stock = f'Ships in {ex_lead_time} day'
            #             if str_ex_stock and ex_stock != 0:
            #                 lead_time2 = {'raw_value': str_ex_stock}
            #                 min_qty_1 = int(ex_stock)
            #                 estimated_lead_time.append(
            #                     {
            #                         'min_qty': min_qty_1,
            #                         'time_to_arrive': html.unescape(lead_time2)
            #                     }
            #                 )
            #
            #             secondary_lead_time = i['secondary_lead_time']
            #             secondary_stock = i['secondary_stock']
            #             str_secondary_stock = f'Ships in {secondary_lead_time} days'
            #             if str_secondary_stock and secondary_stock != 0:
            #                 lead_time3 = {'raw_value': str_secondary_stock}
            #                 min_qty_1 = int(secondary_stock)
            #                 estimated_lead_time.append(
            #                     {
            #                         'min_qty': min_qty_1,
            #                         'time_to_arrive': html.unescape(lead_time3)
            #                     }
            #                 )
            #
            #             if estimated_lead_time == []:
            #                 estimated_lead_time = None
            #         estimated_lead_time = estimated_lead_time
            #     else:
            #         estimated_lead_time = None
            # ---------------------- Added Lead Time above -------------------------
            main_lead_time_list = []
            for pri_json in price_data_json:
                ##################################

                if pri_json['available_for_order'] != 0:

                    # if pri_json['total_rating_count'] is None:
                    first_set = set()
                    if pri_json['secondary_stock'] != 0:
                        first_set.add(pri_json['secondary_stock'])
                    if pri_json['ex_stock'] != 0:
                        first_set.add(pri_json['ex_stock'])

                    if len(first_set) < 2:
                        # 13-01-2025 BY deepak
                        if pri_json["quantity"] == 0 and pri_json["ex_stock"] == 0 and pri_json['secondary_stock'] == 0:
                            minQty_1 = {"min_qty": 1, "time_to_ship": {
                                "raw_value": f"Ships in {pri_json['secondary_lead_time']} days"}}
                            main_lead_time_list.append(minQty_1)
                        # 17/01/2025
                        if pri_json["quantity"] != 0 and pri_json["ex_stock"] == 0 and pri_json['secondary_stock'] == 0:
                            total_minutes = pri_json['express_cutoff']
                            hours = int(total_minutes // 60)
                            minutes = int(total_minutes % 60)
                            main_estimated = f"Ships today - Order in {hours} hours & {minutes} minutes"
                            minQty_1 = {"min_qty": 1, "time_to_ship": {"raw_value": f"{main_estimated}"}}
                            main_lead_time_list.append(minQty_1)

                            minQty_2 = {"min_qty": pri_json["quantity"] + 1,
                                        "time_to_ship": {"raw_value": f"Get A Quote"}}
                            main_lead_time_list.append(minQty_2)

                        if pri_json["quantity"] == 0 and pri_json["ex_stock"] == 0 and pri_json['secondary_stock'] != 0:

                            minQty_1 = {"min_qty": 1, "time_to_ship": {
                                "raw_value": f"Ships in {pri_json['secondary_lead_time']} days"}}
                            main_lead_time_list.append(minQty_1)
                            minQty_2 = {"min_qty": pri_json["secondary_stock"] + 1,
                                        "time_to_ship": {"raw_value": f"Get A Quote"}}
                            main_lead_time_list.append(minQty_2)
                        elif pri_json["quantity"] == 0 and pri_json["secondary_stock"] != 0 and pri_json[
                            'ex_stock'] != 0:
                            if pri_json["quantity"] == 0 and pri_json["secondary_stock"] != 0:
                                minQty_1 = {"min_qty": 1,
                                            "time_to_ship": {"raw_value": f"Ships in {pri_json['ex_lead_time']} days"}}
                                main_lead_time_list.append(minQty_1)
                                minQty_2 = {"min_qty": pri_json["ex_stock"] + 1, "time_to_ship": {
                                    "raw_value": f"Ships in {pri_json['secondary_lead_time']} days"}}
                                main_lead_time_list.append(minQty_2)
                        else:
                            if pri_json["quantity"] == 0 and pri_json["secondary_stock"] == 0 and pri_json[
                                "ex_stock"] != 0:
                                minQty_1 = {"min_qty": 1,
                                            "time_to_ship": {"raw_value": f"Ships in {pri_json['ex_lead_time']} days"}}
                                main_lead_time_list.append(minQty_1)
                                minQty_2 = {"min_qty": pri_json["ex_stock"] + 1, "time_to_ship": {
                                    "raw_value": f"Ships in {pri_json['secondary_lead_time']} days"}}
                                main_lead_time_list.append(minQty_2)

                    # for 3 estimated lead time
                    if pri_json['secondary_stock'] == 0 and pri_json["quantity"] != 0 and pri_json['ex_stock'] != 0:
                        total_minutes = pri_json['express_cutoff']
                        hours = int(total_minutes // 60)
                        minutes = int(total_minutes % 60)
                        main_estimated = f"Ships today - Order in {hours} hours & {minutes} minutes"
                        minQty_1 = {"min_qty": 1, "time_to_ship": {"raw_value": f"{main_estimated}"}}
                        main_lead_time_list.append(minQty_1)

                        minQty_2 = {"min_qty": pri_json['quantity'] + 1,
                                    "time_to_ship": {"raw_value": f"Ships in {pri_json['ex_lead_time']} days"}}
                        main_lead_time_list.append(minQty_2)

                        minQty_3 = {"min_qty": pri_json['ex_stock'] + 1,
                                    "time_to_ship": {"raw_value": f"Ships in {pri_json['secondary_lead_time']} days"}}
                        main_lead_time_list.append(minQty_3)
                    elif pri_json['ex_stock'] == 0 and pri_json['secondary_stock'] != 0 and pri_json['quantity'] != 0:
                        total_minutes = pri_json['express_cutoff']
                        hours = int(total_minutes // 60)
                        minutes = int(total_minutes % 60)
                        main_estimated = f"Ships today - Order in {hours} hours & {minutes} minutes"
                        minQty_1 = {"min_qty": 1, "time_to_ship": {"raw_value": f"{main_estimated}"}}
                        main_lead_time_list.append(minQty_1)

                        minQty_2 = {"min_qty": pri_json['quantity'] + 1,
                                    "time_to_ship": {"raw_value": f"Ships in {pri_json['secondary_lead_time']} days"}}
                        main_lead_time_list.append(minQty_2)

                        minQty_3 = {"min_qty": pri_json['secondary_stock'] + 1,
                                    "time_to_ship": {"raw_value": f"Get A Quote"}}
                        main_lead_time_list.append(minQty_3)
                    else:
                        if pri_json["quantity"] == 0 and pri_json["secondary_stock"] != 0 and pri_json['ex_stock'] != 0:
                            minQty_1 = {"min_qty": 1,
                                        "time_to_ship": {"raw_value": f"Ships in {pri_json['ex_lead_time']} days"}}
                            main_lead_time_list.append(minQty_1)

                            minQty_2 = {"min_qty": pri_json['ex_stock'] + 1, "time_to_ship": {
                                "raw_value": f"Ships in {pri_json['secondary_lead_time']} days"}}
                            main_lead_time_list.append(minQty_2)

                            minQty_3 = {"min_qty": pri_json['secondary_stock'] + 1,
                                        "time_to_ship": {"raw_value": f"Get A Quote"}}
                            main_lead_time_list.append(minQty_3)

                    if pri_json['ex_stock'] and pri_json['secondary_stock'] and pri_json['quantity']:
                        total_minutes = pri_json['express_cutoff']
                        hours = int(total_minutes // 60)
                        minutes = int(total_minutes % 60)
                        main_estimated = f"Ships today - Order in {hours} hours & {minutes} minutes"
                        minQty_1 = {"min_qty": 1, "time_to_ship": {"raw_value": f"{main_estimated}"}}
                        main_lead_time_list.append(minQty_1)

                        minQty_2 = {"min_qty": pri_json['quantity'] + 1,
                                    "time_to_ship": {"raw_value": f"Ships in {pri_json['ex_lead_time']} days"}}
                        main_lead_time_list.append(minQty_2)

                        minQty_2 = {"min_qty": pri_json['ex_stock'] + 1,
                                    "time_to_ship": {"raw_value": f"Ships in {pri_json['secondary_lead_time']} days"}}
                        main_lead_time_list.append(minQty_2)

                        minQty_3 = {"min_qty": pri_json['secondary_stock'] + 1,
                                    "time_to_ship": {"raw_value": f"Get A Quote"}}
                        main_lead_time_list.append(minQty_3)

            item['vendor'] = vendor
            item['sku'] = p_sku
            item['pdp_url'] = pdp_url
            sorted_list = sorted(final_price, key=lambda x: x['min_qty'])
            if sorted_list != []:
                item['price'] = sorted_list
            else:
                item['price_string'] = final_price
            # item['price'] = sorted_list if sorted_list != [] else item['price_string'] = price_string
            item['available_to_checkout'] = available_to_checkout
            item['in_stock'] = in_stock
            # item['lead_time'] = estimated_lead_time
            item['lead_time'] = main_lead_time_list

            for price_data in item['price']:
                if 'price' in price_data:
                    price_data['price'] = float(price_data['price'])
            return {'statusCode': 200,
                    'data': item}
    except Exception as e:
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}


# Input Params
# vendor = "accugroup"
# sku = '05020070001'
# pdp_url = 'https://accu-components.com/us/wera-joker-6001-switch-ratcheting-combination-spanners/644704-05020070001'
# print(json.dumps(accugroup(pdp_url, sku, vendor)))
# if __name__ == '__main__':
#     event = {"sku": "SFP-0-80-3/16-A2-B", "vendor": "accugroup", "pdp_url": "https://components.com/us/imperial-slotted-pan-head-screws/168962-SFP-0-80-3-16-A2-BL"}
#     print(json.dumps(accugroup(pdp_url=event['pdp_url'], sku=event['sku'])))

# {"pdp_url": "https://accu-components.com/us/wera-joker-6002-combination-spanners/644738-05003760001", "sku": "5003760001", "vendor": "accugroup"}

