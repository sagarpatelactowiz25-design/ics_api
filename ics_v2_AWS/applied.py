import json
import requests

from parsel import Selector


cookies = {
    'JSESSIONID': 'EA8D58688D2715B2F5D13A5A607DEBFD.accstorefront-6ddc48bd69-cnpnj',
    'punchout': 'false',
    'ROUTE': '.accstorefront-6ddc48bd69-cnpnj',
    '__cf_bm': 'upmS5IqrB.z9UhYk74OpRpKxaVkDEzyA4vE959TOUHM-1721979098-1.0.1.1-EV5NOdG142Tuzexr_zURANmjvO95VW4cEO9Ac1fQ4oL.4hpPwrrRPN1nqnFwU4LHVzNg9a5QYb.lKfWNuY6HvQ',
    'gbi_sessionId': 'clz2dvp6e0000356kdo39bxk5',
    'gbi_visitorId': 'clz2dvp6g0001356k393pq8l1',
    'cf_clearance': 'iDqNj_lGwcS9icHVPNTkkjil0nBnziuN0OqvvxeUU3I-1721979101-1.0.1.1-IkGdWe35RFGN8viCRwqwrJ_5k5bMtv76HTgJtibdat_YcDzY00eSvqK115EATNEBWkrY55TDmg7Kr7YNQpFezA',
    '_gcl_au': '1.1.1230815399.1721979075',
    'OptanonAlertBoxClosed': '2024-07-26T07:31:16.133Z',
    '_ga': 'GA1.2.1579823060.1721979076',
    '_gid': 'GA1.2.1562523563.1721979076',
    '__hstc': '195597939.3fec643c4ac1b6988bbc0fa0ec1e84fe.1721979078174.1721979078174.1721979078174.1',
    'hubspotutk': '3fec643c4ac1b6988bbc0fa0ec1e84fe',
    '__hssrc': '1',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Jul+26+2024+13%3A01%3A42+GMT%2B0530+(India+Standard+Time)&version=202405.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=36522dbf-1c0a-4056-ac47-a4671cf4488c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&intType=1&geolocation=IN%3BMP&AwaitingReconsent=false',
    '__hssc': '195597939.2.1721979078174',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'JSESSIONID=EA8D58688D2715B2F5D13A5A607DEBFD.accstorefront-6ddc48bd69-cnpnj; punchout=false; ROUTE=.accstorefront-6ddc48bd69-cnpnj; __cf_bm=upmS5IqrB.z9UhYk74OpRpKxaVkDEzyA4vE959TOUHM-1721979098-1.0.1.1-EV5NOdG142Tuzexr_zURANmjvO95VW4cEO9Ac1fQ4oL.4hpPwrrRPN1nqnFwU4LHVzNg9a5QYb.lKfWNuY6HvQ; gbi_sessionId=clz2dvp6e0000356kdo39bxk5; gbi_visitorId=clz2dvp6g0001356k393pq8l1; cf_clearance=iDqNj_lGwcS9icHVPNTkkjil0nBnziuN0OqvvxeUU3I-1721979101-1.0.1.1-IkGdWe35RFGN8viCRwqwrJ_5k5bMtv76HTgJtibdat_YcDzY00eSvqK115EATNEBWkrY55TDmg7Kr7YNQpFezA; _gcl_au=1.1.1230815399.1721979075; OptanonAlertBoxClosed=2024-07-26T07:31:16.133Z; _ga=GA1.2.1579823060.1721979076; _gid=GA1.2.1562523563.1721979076; __hstc=195597939.3fec643c4ac1b6988bbc0fa0ec1e84fe.1721979078174.1721979078174.1721979078174.1; hubspotutk=3fec643c4ac1b6988bbc0fa0ec1e84fe; __hssrc=1; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+26+2024+13%3A01%3A42+GMT%2B0530+(India+Standard+Time)&version=202405.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=36522dbf-1c0a-4056-ac47-a4671cf4488c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&intType=1&geolocation=IN%3BMP&AwaitingReconsent=false; __hssc=195597939.2.1721979078174',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}
pricecookies = {
    'JSESSIONID': 'EA8D58688D2715B2F5D13A5A607DEBFD.accstorefront-6ddc48bd69-cnpnj',
    'punchout': 'false',
    'ROUTE': '.accstorefront-6ddc48bd69-cnpnj',
    '__cf_bm': 'upmS5IqrB.z9UhYk74OpRpKxaVkDEzyA4vE959TOUHM-1721979098-1.0.1.1-EV5NOdG142Tuzexr_zURANmjvO95VW4cEO9Ac1fQ4oL.4hpPwrrRPN1nqnFwU4LHVzNg9a5QYb.lKfWNuY6HvQ',
    'gbi_sessionId': 'clz2dvp6e0000356kdo39bxk5',
    'gbi_visitorId': 'clz2dvp6g0001356k393pq8l1',
    'cf_clearance': 'iDqNj_lGwcS9icHVPNTkkjil0nBnziuN0OqvvxeUU3I-1721979101-1.0.1.1-IkGdWe35RFGN8viCRwqwrJ_5k5bMtv76HTgJtibdat_YcDzY00eSvqK115EATNEBWkrY55TDmg7Kr7YNQpFezA',
    '_gcl_au': '1.1.1230815399.1721979075',
    'OptanonAlertBoxClosed': '2024-07-26T07:31:16.133Z',
    '_ga': 'GA1.2.1579823060.1721979076',
    '_gid': 'GA1.2.1562523563.1721979076',
    '_dc_gtm_UA-10812675-5': '1',
    '__hstc': '195597939.3fec643c4ac1b6988bbc0fa0ec1e84fe.1721979078174.1721979078174.1721979078174.1',
    'hubspotutk': '3fec643c4ac1b6988bbc0fa0ec1e84fe',
    '__hssrc': '1',
    '__hssc': '195597939.1.1721979078174',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Jul+26+2024+13%3A01%3A41+GMT%2B0530+(India+Standard+Time)&version=202405.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=36522dbf-1c0a-4056-ac47-a4671cf4488c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&intType=1&geolocation=IN%3BMP&AwaitingReconsent=false',
}

price_headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': 'JSESSIONID=EA8D58688D2715B2F5D13A5A607DEBFD.accstorefront-6ddc48bd69-cnpnj; punchout=false; ROUTE=.accstorefront-6ddc48bd69-cnpnj; __cf_bm=upmS5IqrB.z9UhYk74OpRpKxaVkDEzyA4vE959TOUHM-1721979098-1.0.1.1-EV5NOdG142Tuzexr_zURANmjvO95VW4cEO9Ac1fQ4oL.4hpPwrrRPN1nqnFwU4LHVzNg9a5QYb.lKfWNuY6HvQ; gbi_sessionId=clz2dvp6e0000356kdo39bxk5; gbi_visitorId=clz2dvp6g0001356k393pq8l1; cf_clearance=iDqNj_lGwcS9icHVPNTkkjil0nBnziuN0OqvvxeUU3I-1721979101-1.0.1.1-IkGdWe35RFGN8viCRwqwrJ_5k5bMtv76HTgJtibdat_YcDzY00eSvqK115EATNEBWkrY55TDmg7Kr7YNQpFezA; _gcl_au=1.1.1230815399.1721979075; OptanonAlertBoxClosed=2024-07-26T07:31:16.133Z; _ga=GA1.2.1579823060.1721979076; _gid=GA1.2.1562523563.1721979076; _dc_gtm_UA-10812675-5=1; __hstc=195597939.3fec643c4ac1b6988bbc0fa0ec1e84fe.1721979078174.1721979078174.1721979078174.1; hubspotutk=3fec643c4ac1b6988bbc0fa0ec1e84fe; __hssrc=1; __hssc=195597939.1.1721979078174; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+26+2024+13%3A01%3A41+GMT%2B0530+(India+Standard+Time)&version=202405.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=36522dbf-1c0a-4056-ac47-a4671cf4488c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&intType=1&geolocation=IN%3BMP&AwaitingReconsent=false',
    # 'if-modified-since': 'Fri, 26 Jul 2024 07:31:42 GMT',
    # 'priority': 'u=1, i',
    # 'referer': 'https://www.applied.com/c-brands/c-megadyne/1400ttm14m90/RPC-Titanium-Synchronous-Belt/p/119940642',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
final_list = []

proxy = {
            "http": "http://scraperapi:de51e4aafe704395654a32ba0a14494d@proxy-server.scraperapi.com:8001",
            "https": "http://scraperapi:de51e4aafe704395654a32ba0a14494d@proxy-server.scraperapi.com:8001"
        }

def applied(url, sku, vendor='applied'):
    try:
        error = {}
        try:

            response_data = requests.get(url,
                                headers=headers,
                                         cookies=cookies,
                                         verify=False,
                                         proxies=proxy)
        except:

            response_data = requests.get(url, headers=headers,cookies=cookies,
                                         verify=False,
                                         proxies=proxy)
        if response_data.status_code != 200:
            for k_ in range(0, 5):

                response_data = requests.get(url, headers=headers,cookies=cookies,
                                             verify=False,
                                             proxies=proxy)

                if response_data.status_code == 200:
                    break
        if response_data.status_code == 200:
            response = Selector(text=response_data.text)
            data = {}
            data['vendor'] = vendor
            if not response.xpath('//div[@class="product-list"]'):
                sku1 = response.xpath('//*[contains(@class,"part-number")]//text()').get('')
                if sku1:
                    try:
                        data['sku'] = sku1.split('#')[1].strip()
                    except:
                        data['sku'] = None

                if data['sku'] == sku:
                    data['pdp_url'] = url
                    estimated_list = []
                    pcode = url.split('/')[-1]
                    params_instock = {
                        'quantity': '1',
                        'productCodes': f'{pcode}',
                        'page': 'SAC',
                        'productCode': f'{pcode}',
                    }

                    try:

                        response_status = requests.post('https://www.applied.com/inventory/status',headers=price_headers,cookies=pricecookies,
                                                        proxies=proxy)
                    except:

                        response_status = requests.post('https://www.applied.com/inventory/status',params=params_instock,headers=price_headers,cookies=pricecookies,
                                                        verify=False,
                                                        proxies=proxy)
                    if response_status.status_code != 200:
                        for k_ in range(0, 5):

                            response_status = requests.post('https://www.applied.com/inventory/status',params=params_instock,headers=price_headers,cookies=pricecookies,
                                                            verify=False,
                                                            proxies=proxy)
                            if response_status.status_code == 200:
                                break
                    if response_status.status_code==200:
                        available_Data = json.loads(response_status.text)
                        try:
                            if available_Data:
                                status = ''
                                for st in available_Data.get("responseObject"):
                                    status = st.get('status').lower()
                                    estimate = st.get('toolTipMessage').lower()
                                    if estimate:
                                        estimate_lead = estimate
                                        estimated_list.append({
                                            'min_qty': 1,
                                            'time_to_ship': {
                                                'raw_value': estimate_lead
                                            }
                                        })
                                if "ready to ship" in status or "available to order" in status or 'in stock' in status:
                                    instock = True
                                else:
                                    instock = False

                        except:
                            pass
                    #                 here code for price
                    price_list = []
                    price_dict = {}
                    quintity = response.xpath('//div[contains(@class,"qty")]//input[contains(@class,"qty input")]//@value').get('')
                    if quintity:
                        price_dict['min_qty'] = int(quintity.strip())
                    else:
                        price_dict['min_qty'] = 1
                    params_price = {
                        'productCodes': f'{pcode}',
                    }

                    try:

                        response_price = requests.get('http://www.applied.com/getprices', verify=False,params=params_price,headers=price_headers,cookies=pricecookies,
                                                      proxies=proxy)
                    except:

                        response_price = requests.get('http://www.applied.com/getprices', verify=False,params=params_price,headers=price_headers,cookies=pricecookies,
                                                      proxies=proxy)
                    if response_price.status_code != 200:
                        for k_ in range(0, 5):

                            response_price = requests.get('http://www.applied.com/getprices', verify=False,params=params_price,headers=price_headers,cookies=pricecookies,
                                                          proxies=proxy)
                            if response_price.status_code == 200:
                                break
                    if response_price.status_code ==  200:
                        price_data = json.loads(response_price.text)

                        if price_data:
                            price1 = price_data['responseObject'][f'{data["sku"]}'].get('priceData').get('value')
                            if price1:
                                price_dict['price'] = float(str(price1).replace(',', '').strip())
                                price_dict['currency'] = 'USD'
                            else:
                                price_dict['price_string'] = 'Call For Price'

                        price_list.append(price_dict)
                    if response_status.status_code==200 and response_price.status_code ==200 and response_data.status_code == 200:
                        data['price'] = price_list
                        data['available_to_checkout'] = instock
                        data['in_stock'] = instock
                        if estimated_list:
                            data['lead_time'] = estimated_list
                        else:
                            data['lead_time'] = None

                        return {'statusCode': 200,
                                'data': data}
                    else:
                        error['statusCode'] = 408
                        error['error_message'] = "Request timeout, failed to reach host"
                        return error


                else:
                    error['statusCode'] = 404
                    error['error_message'] = f"Scraped sku:{data['sku']} does not match input sku:{sku}"
                    return error
            else:
                error['statusCode'] = 404
                error['error_message'] = 'Product Not Found'
                return error
        else:
            error['statusCode'] = 408
            error['error_message'] = "Request timeout, failed to reach host"
            return error

    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = "Internal server error" + str(e)
        return error
