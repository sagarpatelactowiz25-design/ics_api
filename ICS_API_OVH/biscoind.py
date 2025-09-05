import json  # install json
import re
import secrets  # pip install secrets
import jwt  # pip install PyJWT
import requests  # install requests
from parsel import Selector

max_retires = 5


def biscoind(pdp_url, sku, vendor):
    product_sku = sku
    cookies = {
        'utm_referrer': '',
        'VtexRCMacIdv7': '177ab654-fe33-43f8-9034-9ad052e60d9f',
        'biggy-anonymous': 'CTA2iiTmqTOTZUbGig61l',
        'vtex_binding_address': 'www.biscoind.com/en-US',
        'utm_referrer': 'https://www.google.com/',
        'checkout.vtex.com': '__ofid=bf72c6fd78ae447388071a06e3965395',
        '_ga': 'GA1.1.142262580.1710502596',
        '_ga_P1BVE8P2YP': 'GS1.1.1710736996.2.0.1710736996.60.0.0',
        'VtexWorkspace': 'master%3A-',
        'VtexRCSessionIdv7': 'd3ecf334-02ec-4c92-9099-040254c86994',
        '_uetsid': '1ece76f0f58011eea58f91621856cee8',
        '_uetvid': '3861ba40e2c011eebcfdddfe1c08e6f4',
        'vtex_session': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IkM0ODlERDdBRkFCRTdFMDlFOEIwM0Q3QUJFNzIxMzlBOEYwQjIzRTEiLCJ0eXAiOiJqd3QifQ.eyJhY2NvdW50LmlkIjoiNDY0YWRkMDMtNmZlZi00ZmE2LWJhNTYtN2IwYTRhNjcwZTRiIiwiaWQiOiJlYjQ1OGFlYi0zMWY1LTQ4YjQtYWVjMS05ZGJiNGUwZTNhNjQiLCJ2ZXJzaW9uIjoyLCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE3MTMyNTUzMTIsImlhdCI6MTcxMjU2NDExMiwiaXNzIjoidG9rZW4tZW1pdHRlciIsImp0aSI6IjRkZTkwYzM1LTA0MWYtNDUxMS04Yzg2LWIyNzA1ODFhZDk2YyJ9.G3FoU0bVnxI0vKM1e4QRRQwdchkcEZUpKucKML1yOYN7k_X122PZbRSA6VFFdlEs3GOWw59LkUxQsCxS5zE77Q',
        'vtex_segment': 'eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOm51bGwsInJlZ2lvbklkIjpudWxsLCJ1dG1fY2FtcGFpZ24iOm51bGwsInV0bV9zb3VyY2UiOm51bGwsInV0bWlfY2FtcGFpZ24iOm51bGwsImN1cnJlbmN5Q29kZSI6IlVTRCIsImN1cnJlbmN5U3ltYm9sIjoiJCIsImNvdW50cnlDb2RlIjoiVVNBIiwiY3VsdHVyZUluZm8iOiJlbi1VUyIsImFkbWluX2N1bHR1cmVJbmZvIjoiZW4tVVMiLCJjaGFubmVsUHJpdmFjeSI6InB1YmxpYyJ9',
        'biggy-session-biscoind': 'Ku8YAFlTPU1A8uNB2ATYA',
        '__kla_id': 'eyJjaWQiOiJORFJoTUdJMFpEZ3RaRGt3TWkwMFl6WmhMVGczTkRNdFpESXhZakl5TUdJeU9HTXgiLCIkcmVmZXJyZXIiOnsidHMiOjE3MTA1MDI1ODAsInZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJmaXJzdF9wYWdlIjoiaHR0cHM6Ly93d3cuYmlzY29pbmQuY29tLyJ9LCIkbGFzdF9yZWZlcnJlciI6eyJ0cyI6MTcxMjU2NDExNCwidmFsdWUiOiIiLCJmaXJzdF9wYWdlIjoiaHR0cHM6Ly93d3cuYmlzY29pbmQuY29tL252ZW50LXNjaHJvZmYtMjA4MTctNjA2L3AifX0=',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Apr+08+2024+13%3A45%3A15+GMT%2B0530+(India+Standard+Time)&version=202212.1.0&isIABGlobal=false&hosts=&consentId=e8f19186-6dcc-41e0-b845-40d3794bd385&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CSPD_BG%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false',
        'janus_sid': '8d6b10f3-0e5d-491c-a889-58372beefbdd',
        'biggy-event-queue': '',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'utm_referrer=; VtexRCMacIdv7=177ab654-fe33-43f8-9034-9ad052e60d9f; biggy-anonymous=CTA2iiTmqTOTZUbGig61l; vtex_binding_address=www.biscoind.com/en-US; utm_referrer=https://www.google.com/; checkout.vtex.com=__ofid=bf72c6fd78ae447388071a06e3965395; _ga=GA1.1.142262580.1710502596; _ga_P1BVE8P2YP=GS1.1.1710736996.2.0.1710736996.60.0.0; VtexWorkspace=master%3A-; VtexRCSessionIdv7=d3ecf334-02ec-4c92-9099-040254c86994; _uetsid=1ece76f0f58011eea58f91621856cee8; _uetvid=3861ba40e2c011eebcfdddfe1c08e6f4; vtex_session=eyJhbGciOiJFUzI1NiIsImtpZCI6IkM0ODlERDdBRkFCRTdFMDlFOEIwM0Q3QUJFNzIxMzlBOEYwQjIzRTEiLCJ0eXAiOiJqd3QifQ.eyJhY2NvdW50LmlkIjoiNDY0YWRkMDMtNmZlZi00ZmE2LWJhNTYtN2IwYTRhNjcwZTRiIiwiaWQiOiJlYjQ1OGFlYi0zMWY1LTQ4YjQtYWVjMS05ZGJiNGUwZTNhNjQiLCJ2ZXJzaW9uIjoyLCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE3MTMyNTUzMTIsImlhdCI6MTcxMjU2NDExMiwiaXNzIjoidG9rZW4tZW1pdHRlciIsImp0aSI6IjRkZTkwYzM1LTA0MWYtNDUxMS04Yzg2LWIyNzA1ODFhZDk2YyJ9.G3FoU0bVnxI0vKM1e4QRRQwdchkcEZUpKucKML1yOYN7k_X122PZbRSA6VFFdlEs3GOWw59LkUxQsCxS5zE77Q; vtex_segment=eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOm51bGwsInJlZ2lvbklkIjpudWxsLCJ1dG1fY2FtcGFpZ24iOm51bGwsInV0bV9zb3VyY2UiOm51bGwsInV0bWlfY2FtcGFpZ24iOm51bGwsImN1cnJlbmN5Q29kZSI6IlVTRCIsImN1cnJlbmN5U3ltYm9sIjoiJCIsImNvdW50cnlDb2RlIjoiVVNBIiwiY3VsdHVyZUluZm8iOiJlbi1VUyIsImFkbWluX2N1bHR1cmVJbmZvIjoiZW4tVVMiLCJjaGFubmVsUHJpdmFjeSI6InB1YmxpYyJ9; biggy-session-biscoind=Ku8YAFlTPU1A8uNB2ATYA; __kla_id=eyJjaWQiOiJORFJoTUdJMFpEZ3RaRGt3TWkwMFl6WmhMVGczTkRNdFpESXhZakl5TUdJeU9HTXgiLCIkcmVmZXJyZXIiOnsidHMiOjE3MTA1MDI1ODAsInZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJmaXJzdF9wYWdlIjoiaHR0cHM6Ly93d3cuYmlzY29pbmQuY29tLyJ9LCIkbGFzdF9yZWZlcnJlciI6eyJ0cyI6MTcxMjU2NDExNCwidmFsdWUiOiIiLCJmaXJzdF9wYWdlIjoiaHR0cHM6Ly93d3cuYmlzY29pbmQuY29tL252ZW50LXNjaHJvZmYtMjA4MTctNjA2L3AifX0=; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Apr+08+2024+13%3A45%3A15+GMT%2B0530+(India+Standard+Time)&version=202212.1.0&isIABGlobal=false&hosts=&consentId=e8f19186-6dcc-41e0-b845-40d3794bd385&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CSPD_BG%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false; janus_sid=8d6b10f3-0e5d-491c-a889-58372beefbdd; biggy-event-queue=',
        'if-none-match': '"81CFCE1A1FC280108C44CD63E45D63D4"',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'service-worker-navigation-preload': 'true',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    error_dict = {}

    for i in range(max_retires):
        response_data = requests.get(url=pdp_url, headers=headers, cookies=cookies)

        if response_data.status_code == 200:
            break

        elif response_data.status_code == 404:

            error_dict['statusCode'] = 410
            error_dict['error_message'] = str("410 Page not found")
            return error_dict
    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}

    if response_data.status_code == 200 and 'property="product:sku"' in response_data.text:

        response = Selector(text=response_data.text)

        js_pro = response.xpath('//template[@data-type="json"][@data-varname="__STATE__"]//text()').getall()
        if js_pro:
            js_pro_data = json.loads("".join(js_pro))
            key_first = list(js_pro_data.keys())[0]
            pro_data = js_pro_data.get(key_first)

            sku = (" ".join(response.xpath(
                '//span[@class="biscoind-bisco-components-0-x-productFieldHighlightsFieldValue"]//text()').getall())).strip()
            if sku:
                pass
            else:
                sku = pro_data.get("productReference")
            try:
                if sku.strip() != product_sku:
                    error_dict['statusCode'] = 410
                    error_dict['error_message'] = f"Scraped SKU:{sku} does not match input SKU:{product_sku}"
                    return error_dict
            except Exception as e:
                error_dict['statusCode'] = 500
                error_dict['error_message'] = str(e)
                return error_dict

            in_stock = True

            for i in list(js_pro_data.keys()):
                if "AvailableQuantity" in list(js_pro_data[i].keys()):
                    available_check = js_pro_data[i].get("AvailableQuantity")
                    if int(available_check) == 1000000 or int(available_check) == 0:
                        in_stock = False
                    else:
                        in_stock = True

                    break
            # pricing
            qi = 1
            for i in list(js_pro_data.keys()):
                if i.endswith('.items.0'):
                    qi = js_pro_data[i]['unitMultiplier']
            if qi == 0:
                qi = 1

            try:
                requests_zip_code_text_json = " ".join(
                    response.xpath('//template[@data-varname="__STATE__"]//text()').getall())
                requests_zip_code_text_dict = json.loads(requests_zip_code_text_json)
                if requests_zip_code_text_dict:
                    try:
                        for i in requests_zip_code_text_dict[
                            "ROOT_QUERY"]:  # we Find itemId,postalCode,sellerId,tradePolicyId,hash_value for lead time header
                            if "itemId" in str(i):
                                match = re.search(
                                    r'"itemId":"(\d+)","postalCode":"([^"]*)","sellerId":"([^"]*)","tradePolicyId":"(\d+)".*?"hash":"([^"]*)"',
                                    str(i))

                                if match:
                                    itemId = match.group(1)
                                    sellerId = match.group(3)
                                    tradePolicyId = match.group(4)
                                    hash = match.group(5)

                                else:
                                    itemId = ''
                                    sellerId = ''
                                    tradePolicyId = ''




                    except:
                        itemId = ''
                        sellerId = ''
                        tradePolicyId = ''
                    secret_key = secrets.token_urlsafe(32)

                    # This payload using convert secret_key and secret_key convert tocken this tocken is use in url name is estimated_lead_time_url
                    final_lead_time_list = []
                    if itemId and sellerId and tradePolicyId:
                        payload = {"itemId": f"{itemId}", "sellerId": f"{sellerId}",
                                   "tradePolicyId": f"{tradePolicyId}",
                                   "postalCode": "11106"}

                        token = jwt.encode(payload, secret_key, algorithm='HS256')
                        token_gen = token.split(".")[1]
                        try:
                            for key_find in requests_zip_code_text_dict.values():
                                if "unitMultiplier" in key_find:
                                    unitMultiplier = key_find['unitMultiplier']
                        except Exception as e:
                            print(e)

                        price = ''
                        price_list = []
                        for price_key in js_pro_data.keys():
                            if "ROOT_QUERY.priceBreaks" in price_key:
                                min_qty_data_min = int((js_pro_data[price_key]).get("minQuantity"))
                                min_qty_data = unitMultiplier * min_qty_data_min
                                price_data = round(float((js_pro_data[price_key]).get("price")) * int(min_qty_data_min),
                                                   2)
                                if price:
                                    if qi:
                                        min_qty_data = min_qty_data * qi
                                        price_data = float(f"{(price_data / qi):.4f}")

                                if min_qty_data and price_data and price_data != 0.0:
                                    price_list.append({"min_qty": min_qty_data, "price": price_data, "currency": "USD"})
                        if not price_list:
                            price_list = [{"min_qty": 1, "price_string": "Call for price"}]

                        headers_1 = {
                            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                            'accept': '*/*',
                            'content-type': 'application/json',
                            'Referer': 'https://www.biscoind.com/southco-ea-c3-101-9/p',
                            'sec-ch-ua-mobile': '?0',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'sec-ch-ua-platform': '"Windows"',
                        }

                        estimated_lead_time_url = f"""https://www.biscoind.com/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=en-US&__bindingId=ae5b2c52-c129-4fa1-ba8c-e8deeb511774&operationName=QuantityPriceBreaks&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22{hash}%22%2C%22sender%22%3A%22biscoind.bisco-components%400.x%22%2C%22provider%22%3A%22biscoind.bisco-graphql%400.x%22%7D%2C%22variables%22%3A%22{token_gen}%3D%22%7D"""
                        lead_time_data_response = requests.get(url=estimated_lead_time_url, headers=headers_1)
                        if lead_time_data_response.status_code == 200:
                            try:
                                datas = json.loads(lead_time_data_response.text)
                                check_days_updated = []

                                for data in datas['data']['priceBreaks']:
                                    min_quantity = unitMultiplier * int(data['minQuantity'])
                                    max_quantity = data['maxQuantity']

                                    lead_time = data['leadTime']
                                    if lead_time:
                                        if not lead_time in check_days_updated:
                                            value = {"min_qty": int(min_quantity),
                                                     "time_to_arrive": {"raw_value": f"{lead_time}"}}
                                            final_lead_time_list.append(value)
                                            check_days_updated.append(lead_time)
                                        elif max_quantity is None:
                                            value = {"min_qty": int(min_quantity),
                                                     "time_to_arrive": {"raw_value": f"{lead_time}"}}
                                            final_lead_time_list.append(value)
                                            check_days_updated.append(lead_time)

                                if final_lead_time_list:
                                    final_lead_time_list = final_lead_time_list
                            except Exception as e:
                                print(e)
                    else:
                        price = ''
                        price_list = []
                        for price_key in js_pro_data.keys():
                            if "ROOT_QUERY.priceBreaks" in price_key:
                                min_qty_data = int((js_pro_data[price_key]).get("minQuantity"))

                                price_data = round(float((js_pro_data[price_key]).get("price")), 2)
                                if price:
                                    if qi:
                                        min_qty_data = min_qty_data * qi
                                        price_data = f"{(price_data / qi):.4f}"

                                if min_qty_data and price_data and price_data != 0.0:
                                    price_list.append({"min_qty": min_qty_data, "price": price_data, "currency": "USD"})
                        if not price_list:
                            price_list = [{"min_qty": 1, "price_string": "Call for price"}]




            except Exception as e:
                print(e)
            if final_lead_time_list:
                available_to_checkout = True
            else:
                available_to_checkout = False
            # Data insert
            item = {}
            item['vendor'] = "biscoind"
            item['sku'] = product_sku
            item['pdp_url'] = pdp_url
            item['price'] = price_list
            item['available_to_checkout'] = available_to_checkout
            item['in_stock'] = in_stock
            if final_lead_time_list:
                item['lead_time'] = final_lead_time_list
            else:
                item['lead_time'] = None
            return {'statusCode': 200,
                    'data': item}
    else:
        error_dict['statusCode'] = 410
        error_dict['error_message'] = str("410 Page not found")
        return error_dict
# your vendor name

# if __name__ == '__main__':
# #
# #     # vendor_name = "Bisco Industries"
# #
#     event={"sku": "62047-11-524-5", "vendor": "biscoind", "pdp_url": "https://www.biscoind.com/southco-47-11-524-50/p"}
#     product_sku = event['sku']
#     pdp_url = event['pdp_url']
#     vendor_name=event['vendor']
#     print(json.dumps(biscoind(pdp_url,product_sku,vendor_name)))
# for i in list_data:
#     # product_sku = i.split("|")[0]
#     product_sku = "520024A"
#     # pdp_url = i.split("|")[1]
#     pdp_url = "https://www.biscoind.com/essentra-components-024a/p"
#     print(pdp_url,json.dumps(biscoind(pdp_url,product_sku,vendor_name)))
# break
