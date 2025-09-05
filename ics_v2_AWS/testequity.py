import html
import json
import requests



cookies = {
    'JSESSIONID': 'CFD69C101EB5846963A4984E1C354270.accstorefront-66b8fc9d79-8962p',
    'punchout': 'false',
    'ROUTE': '.accstorefront-66b8fc9d79-8962p',
    '__cf_bm': 'tKkvBkQU.ZJ5Zr9mCmIQ_kHMLvIqgB1FGaMOM3mzpzc-1712913901-1.0.1.1-ngC9CXeB2k4gHCRFz4zaSNDftrMbcNWYnw4GMfdSsRskyhEEqyLy.kqQbo0UIHn2CK4SbMnDmmCCRUoTepna8Q',
    'CookieConsent': '{stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:3%2Cutc:1712913903109%2Cregion:%27IS%27}',
    'gbi_sessionId': 'cluwgpndj0000356pvs7nm7o8',
    'gbi_visitorId': 'cluwgpndj0001356p27f33hv8',
    'cf_clearance': 'b.nzWnfytEahkirkxovYA_Q6THsSbzt1yCKhw29wXt4-1712913904-1.0.1.1-VYKjn03RK2Mzii8nouiL3EY6i_Ez6INz1p7pRCVY9b_JSL4rvtO0kyuJDC6uxPGt6tr.Eog1gTbBzQgrhvUwOQ',
    '__utma': '254702680.1602020269.1712913905.1712913905.1712913905.1',
    '__utmc': '254702680',
    '__utmz': '254702680.1712913905.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmt': '1',
    '__utmb': '254702680.1.10.1712913905',
    '_gcl_au': '1.1.303773880.1712913906',
    '__hstc': '195597939.dc90aec371004d638d6464c62f8f7c51.1712913905868.1712913905868.1712913905868.1',
    'hubspotutk': 'dc90aec371004d638d6464c62f8f7c51',
    '__hssrc': '1',
    '__hssc': '195597939.1.1712913905868',
    '_fbp': 'fb.1.1712913907375.816516000',
    '_ga_ZT5EWHFHHL': 'GS1.1.1712913907.1.1.1712913907.60.0.0',
    '_ga': 'GA1.2.1419124220.1712913908',
    '_gid': 'GA1.2.602904563.1712913909',
    '_uetsid': '8e4dfc00f8ae11ee8d5d515840846243',
    '_uetvid': '8e4de0a0f8ae11eea2291b60917f5b6a',
    '_dc_gtm_UA-10812675-5': '1',
    '_clck': 'rdpr5z%7C2%7Cfkv%7C0%7C1563',
    '_clsk': 'ne65vs%7C1712913914569%7C1%7C1%7Cn.clarity.ms%2Fcollect',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'JSESSIONID=CFD69C101EB5846963A4984E1C354270.accstorefront-66b8fc9d79-8962p; punchout=false; ROUTE=.accstorefront-66b8fc9d79-8962p; __cf_bm=tKkvBkQU.ZJ5Zr9mCmIQ_kHMLvIqgB1FGaMOM3mzpzc-1712913901-1.0.1.1-ngC9CXeB2k4gHCRFz4zaSNDftrMbcNWYnw4GMfdSsRskyhEEqyLy.kqQbo0UIHn2CK4SbMnDmmCCRUoTepna8Q; CookieConsent={stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:3%2Cutc:1712913903109%2Cregion:%27IS%27}; gbi_sessionId=cluwgpndj0000356pvs7nm7o8; gbi_visitorId=cluwgpndj0001356p27f33hv8; cf_clearance=b.nzWnfytEahkirkxovYA_Q6THsSbzt1yCKhw29wXt4-1712913904-1.0.1.1-VYKjn03RK2Mzii8nouiL3EY6i_Ez6INz1p7pRCVY9b_JSL4rvtO0kyuJDC6uxPGt6tr.Eog1gTbBzQgrhvUwOQ; __utma=254702680.1602020269.1712913905.1712913905.1712913905.1; __utmc=254702680; __utmz=254702680.1712913905.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=254702680.1.10.1712913905; _gcl_au=1.1.303773880.1712913906; __hstc=195597939.dc90aec371004d638d6464c62f8f7c51.1712913905868.1712913905868.1712913905868.1; hubspotutk=dc90aec371004d638d6464c62f8f7c51; __hssrc=1; __hssc=195597939.1.1712913905868; _fbp=fb.1.1712913907375.816516000; _ga_ZT5EWHFHHL=GS1.1.1712913907.1.1.1712913907.60.0.0; _ga=GA1.2.1419124220.1712913908; _gid=GA1.2.602904563.1712913909; _uetsid=8e4dfc00f8ae11ee8d5d515840846243; _uetvid=8e4de0a0f8ae11eea2291b60917f5b6a; _dc_gtm_UA-10812675-5=1; _clck=rdpr5z%7C2%7Cfkv%7C0%7C1563; _clsk=ne65vs%7C1712913914569%7C1%7C1%7Cn.clarity.ms%2Fcollect',
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
pricecookies = {
    'JSESSIONID': 'CFD69C101EB5846963A4984E1C354270.accstorefront-66b8fc9d79-8962p',
    'punchout': 'false',
    'ROUTE': '.accstorefront-66b8fc9d79-8962p',
    '__cf_bm': 'tKkvBkQU.ZJ5Zr9mCmIQ_kHMLvIqgB1FGaMOM3mzpzc-1712913901-1.0.1.1-ngC9CXeB2k4gHCRFz4zaSNDftrMbcNWYnw4GMfdSsRskyhEEqyLy.kqQbo0UIHn2CK4SbMnDmmCCRUoTepna8Q',
    'CookieConsent': '{stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:3%2Cutc:1712913903109%2Cregion:%27IS%27}',
    'gbi_sessionId': 'cluwgpndj0000356pvs7nm7o8',
    'gbi_visitorId': 'cluwgpndj0001356p27f33hv8',
    'cf_clearance': 'b.nzWnfytEahkirkxovYA_Q6THsSbzt1yCKhw29wXt4-1712913904-1.0.1.1-VYKjn03RK2Mzii8nouiL3EY6i_Ez6INz1p7pRCVY9b_JSL4rvtO0kyuJDC6uxPGt6tr.Eog1gTbBzQgrhvUwOQ',
    '__utma': '254702680.1602020269.1712913905.1712913905.1712913905.1',
    '__utmc': '254702680',
    '__utmz': '254702680.1712913905.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmt': '1',
    '__utmb': '254702680.1.10.1712913905',
    '_gcl_au': '1.1.303773880.1712913906',
    '__hstc': '195597939.dc90aec371004d638d6464c62f8f7c51.1712913905868.1712913905868.1712913905868.1',
    'hubspotutk': 'dc90aec371004d638d6464c62f8f7c51',
    '__hssrc': '1',
    '__hssc': '195597939.1.1712913905868',
    '_fbp': 'fb.1.1712913907375.816516000',
    '_ga': 'GA1.2.1419124220.1712913908',
    '_gid': 'GA1.2.602904563.1712913909',
    '_uetsid': '8e4dfc00f8ae11ee8d5d515840846243',
    '_uetvid': '8e4de0a0f8ae11eea2291b60917f5b6a',
    '_dc_gtm_UA-10812675-5': '1',
    '_clck': 'rdpr5z%7C2%7Cfkv%7C0%7C1563',
    '_clsk': 'ne65vs%7C1712913914569%7C1%7C1%7Cn.clarity.ms%2Fcollect',
    '_ga_ZT5EWHFHHL': 'GS1.1.1712913907.1.1.1712913917.50.0.0',
}

price_headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': 'JSESSIONID=CFD69C101EB5846963A4984E1C354270.accstorefront-66b8fc9d79-8962p; punchout=false; ROUTE=.accstorefront-66b8fc9d79-8962p; __cf_bm=tKkvBkQU.ZJ5Zr9mCmIQ_kHMLvIqgB1FGaMOM3mzpzc-1712913901-1.0.1.1-ngC9CXeB2k4gHCRFz4zaSNDftrMbcNWYnw4GMfdSsRskyhEEqyLy.kqQbo0UIHn2CK4SbMnDmmCCRUoTepna8Q; CookieConsent={stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:3%2Cutc:1712913903109%2Cregion:%27IS%27}; gbi_sessionId=cluwgpndj0000356pvs7nm7o8; gbi_visitorId=cluwgpndj0001356p27f33hv8; cf_clearance=b.nzWnfytEahkirkxovYA_Q6THsSbzt1yCKhw29wXt4-1712913904-1.0.1.1-VYKjn03RK2Mzii8nouiL3EY6i_Ez6INz1p7pRCVY9b_JSL4rvtO0kyuJDC6uxPGt6tr.Eog1gTbBzQgrhvUwOQ; __utma=254702680.1602020269.1712913905.1712913905.1712913905.1; __utmc=254702680; __utmz=254702680.1712913905.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=254702680.1.10.1712913905; _gcl_au=1.1.303773880.1712913906; __hstc=195597939.dc90aec371004d638d6464c62f8f7c51.1712913905868.1712913905868.1712913905868.1; hubspotutk=dc90aec371004d638d6464c62f8f7c51; __hssrc=1; __hssc=195597939.1.1712913905868; _fbp=fb.1.1712913907375.816516000; _ga=GA1.2.1419124220.1712913908; _gid=GA1.2.602904563.1712913909; _uetsid=8e4dfc00f8ae11ee8d5d515840846243; _uetvid=8e4de0a0f8ae11eea2291b60917f5b6a; _dc_gtm_UA-10812675-5=1; _clck=rdpr5z%7C2%7Cfkv%7C0%7C1563; _clsk=ne65vs%7C1712913914569%7C1%7C1%7Cn.clarity.ms%2Fcollect; _ga_ZT5EWHFHHL=GS1.1.1712913907.1.1.1712913917.50.0.0',
    # 'if-modified-since': 'Fri, 12 Apr 2024 09:25:06 GMT',
    # 'referer': 'https://www.applied.com/c-brands/c-bunting-bearings-llc/pp800004/SAE-841-Sintered-Bronze-Oil-Impregnated-Plate-Stock/p/102870196',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
final_list = []
def testequity(url, sku, vendor='testequity'):
    error = {}
    try:
        headers = {
            'authority': 'www.testequity.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/json',
            'origin': 'https://www.testequity.com',
            'referer': f'{url}',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            # 'Cookie': 'CurrentCurrencyId=30b432b9-a104-e511-96f5-ac9e17867f77; CurrentLanguageId=a26095ef-c714-e311-ba31-d43d7e4e88b2; InsiteCacheId=260c7aaa-6116-4343-881c-89f12ee21a0c; SetContextLanguageCode=en-us; SetContextPersonaIds=d06988c0-9358-4dbb-aa3d-b7be5b6a7fd9'
        }
        product_id = url.split('/')[-1]
        keyword = f"https://www.testequity.com/api/v1/catalogpages?path=%2Fproduct%2F{product_id}"

        try:
            response_id = requests.get(keyword,headers=headers,cookies=cookies)
        except:
            response_id = requests.get(keyword, headers=headers,cookies=cookies)
        if response_id.status_code != 200:
            for k_ in range(0, 5):

                response_id = requests.get(url, headers=headers,cookies=cookies)

                if response_id.status_code == 200:
                    break
        if response_id.status_code == 404:
            error['statusCode'] = 410
            error['error_message'] = 'Product Not Found'
            return error
        if response_id.status_code == 200:
            data = {}
            data['vendor'] = vendor
            json_data_ = json.loads(response_id.text)
            product_id_ = json_data_.get('productId')
            new_url = f"https://www.testequity.com/api/v2/products/{product_id_}?expand=detail%2Cspecifications%2Ccontent%2Cimages%2Cdocuments%2Cattributes%2CvariantTraits%2Cbadges%2Cwarehouses%2Cproperties&includeAttributes=includeOnProduct&addToRecentlyViewed=true"
            try:
                response_data = requests.get(new_url,
                                        # headers=headers, impersonate="chrome99"
                                        )
            except:
                response_data = requests.get(new_url,
                                        # headers=headers, impersonate="chrome99"
                                        )
            if response_data.status_code != 200:
                for k_ in range(0, 5):
                    response_data = requests.get(new_url,
                                            # headers=headers, impersonate="chrome99"
                                            )
                    if response_data.status_code == 200:
                        break
            if response_data.status_code == 200:
                json_data = json.loads(response_data.text)
                # quoteRequired
                try:
                    data['sku'] = html.unescape(json_data.get('productNumber'))
                except:
                    data['sku'] = None
                try:
                    qoutprice =  json_data.get('quoteRequired')
                except:
                    qoutprice = False
                if data['sku']  == sku:
                    data['pdp_url'] = url
                    min_qt = json_data.get('detail').get('multipleSaleQty')
                    if min_qt:
                        min_d = str(min_qt).strip()
                        if min_d:
                            min_qty = min_d
                        else:
                            min_qty = 1
                    else:
                        min_qty = 1
                    estimated_list = []
                    estimated = json_data.get('properties').get('averageLeadTime')
                    if estimated:

                        if int(estimated) > 1:
                            est = str(estimated) + ' Days'
                        else:
                            est = str(estimated) + ' Day'
                        try:
                            min_qty = int(min_qty)
                        except:
                            min_qty = int(min_qty)
                        if est:
                            estimated_list.append({'min_qty': min_qty, 'time_to_stock': {'raw_value': est}})
                    instock_url = "https://www.testequity.com/api/v1/realtimeinventory"
                    payload = json.dumps({
                        "productIds": [
                            f"{product_id_}"
                        ]
                    })

                    response_instock = requests.post(url=instock_url, headers=headers, data=payload)
                    if response_instock.status_code == 200:
                        instock_json = json.loads(response_instock.text)
                        instock1 = instock_json.get('realTimeInventoryResults')[0].get('qtyOnHand')
                        if instock1:
                            if instock1 >= 1:
                                in_stock = True
                            else:
                                in_stock = False
                        else:
                            in_stock = False
                    try:
                        price_list = []
                        price_url = "https://www.testequity.com/api/v1/realtimepricing"

                        payload = json.dumps({
                            "productPriceParameters": [{
                                "productId": f"{product_id_}",
                                "unitOfMeasure": "PK",
                                "qtyOrdered": 1
                            }
                            ]
                        })
                        try:
                            response_price = requests.post(price_url,
                                                         headers=headers, data=payload
                                                         )
                        except:
                            response_price = requests.post(price_url,
                                                         headers=headers, data=payload
                                                         )
                        if response_price.status_code != 200:
                            for k_ in range(0, 5):
                                response_price = requests.post(price_url,
                                                             headers=headers, data=payload
                                                             )
                                if response_price.status_code == 200:
                                    break
                        if response_price.status_code ==200:
                            price_json = json.loads(response_price.text)
                            unitRegularBreakPrices = price_json.get('realTimePricingResults')[0].get('unitRegularBreakPrices')
                            unitRegularPriceDisplay = price_json.get('realTimePricingResults')[0].get('unitRegularPriceDisplay')
                            if unitRegularBreakPrices:
                                if '$' in unitRegularPriceDisplay:
                                    for pr in unitRegularBreakPrices:
                                        price_dict = {}
                                        price1 = pr.get('breakPriceDisplay')

                                        breakQty = pr.get('breakQty')
                                        min_qty = breakQty
                                        price2 = price1.replace('$', '').replace(',', '').strip()
                                        price_dict['min_qty'] = int(min_qty)
                                        if float(price2) > 0:
                                            price = str(price2)
                                            price_dict['price'] = float(price)
                                            price_dict['currency'] = 'USD'
                                        else:
                                            price_dict['price_string'] = 'Call for price'
                                        price_list.append(price_dict)
                                else:
                                    price_dict = {}
                                    price_dict['min_qty'] = 1
                                    price_dict['price_string'] = 'Call for price'
                                    price_list.append(price_dict)
                            else:
                                price_dict = {}
                                price_dict['min_qty'] = int(min_qty)
                                price1 = json_data.get('unitListPriceDisplay')
                                if price1:
                                    price2 = price1.replace('$', '').replace(',', '').strip()

                                    if float(price2) > 0:
                                        if not qoutprice:
                                            if price2:
                                                price = str(price2)
                                                price_dict['price'] = float(price)
                                                price_dict['currency'] = 'USD'
                                            else:
                                                price_dict['price_string'] = 'Call for price'
                                        else:
                                            price_dict['price_string'] = 'Call for price'
                                        price_list.append(price_dict)
                                    else:
                                        price_dict['price_string'] = 'Call for price'
                                        price_list.append(price_dict)

                                else:
                                    price_dict['price_string'] = 'Call for price'
                                    price_list.append(price_dict)

                            data['price'] = price_list
                    except:
                        pass
                    data['in_stock'] = in_stock
                    try:
                        available_to_checkout = json_data.get('cantBuy')
                        if available_to_checkout:
                            data['available_to_checkout'] = False
                        else:
                            data['available_to_checkout'] = True
                    except:
                        pass



                    if estimated_list:
                        data['lead_time'] = estimated_list
                    else:
                        data['lead_time'] = None
                    return {'statusCode': 200,
                            'data': data}


                else:
                    error['statusCode'] = 410
                    error['error_message'] = f"Scraped sku:{data['sku']} does not match input sku:{sku}"
                    return error

            else:
                error['statusCode'] = 408
                error['error_message'] = "Request timeout, failed to reach host"
                return error
        else:
            error['statusCode'] = 408
            error['error_message'] = "Request timeout, failed to reach host"
            return error

    except Exception as e:
        error['statusCode'] = 410
        error['error_message'] = 'Product Not Found'
        return error

# if __name__ == '__main__':
#     event={"sku": "512CH3034", "vendor": "testequity", "pdp_url": "https://www.testequity.com/product/512CH3034-135338"}
#     print(json.dumps(testequity(event['pdp_url'],event['sku'],event['vendor'])))