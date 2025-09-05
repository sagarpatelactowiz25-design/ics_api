import json
import re

import requests
from parsel import Selector

final_list = []
def igus(url, sku, vendor='igus'):

    error = {}
    try:
        response1 = requests.get(url)
    except:
        response1 = requests.get(url)

    if response1.status_code!=200:
        for k_ in range(0,5):
            response1 = requests.get(url)

            if response1.status_code==200:
                break
    if response1.status_code==200:
        response = Selector(text=response1.text)
        try:
            result = {}
            try:
                sku1 =url.split('=')[1]
                if "?artnr" in sku1:
                    sku1 = url.split("?artnr=")[1]
            except:
                sku1 = ''
            if sku1 ==sku:
                try:
                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Connection': 'keep-alive',
                        # 'Cookie': '_gcl_au=1.1.676755666.1683272864; specificga=GA1.2.10435550.1683272865; rollupga=GA1.2.10435550.1683272865; _evga_a655={%22uuid%22:%22fff26fcbcd97580a%22}; _sfid_efb2={%22anonymousId%22:%22fff26fcbcd97580a%22%2C%22consents%22:[]}; _fbp=fb.1.1683272866222.569416171; CookiesInfo=1; hubspotutk=f90ec5a31fc95f11504ae47270ff359f; stg_returning_visitor=Fri%2C%2005%20May%202023%2007:54:27%20GMT; _gid=GA1.2.1049304933.1683525385; specificga_gid=GA1.2.883515036.1683525385; rollupga_gid=GA1.2.240324026.1683525385; ASP.NET_SessionId=ydx0eqhogwwlmjt0eg4rltwv; DomainUserMapping=isLocalPriceDomain=1&uc=in&ud=www.igus.in&ucn=India; server=1; __hssrc=1; liveagent_invite_rejected_5732X000000Gr8i=true; ln_or=eyJOVUxMIjoiZCIsIjQ0MDI4MzQsTlVMTCI6ImQifQ%3D%3D; stg_traffic_source_priority=1; Global_SessionId=v24v1av5vj5ayvig35i2ucrt; _pk_ses.6cffafdd-f01c-4312-8dae-3ec1d1be0771.532d=*; __hstc=191717877.f90ec5a31fc95f11504ae47270ff359f.1683272868774.1683609427631.1683621885931.9; _ga=GA1.1.10435550.1683272865; _pk_id.6cffafdd-f01c-4312-8dae-3ec1d1be0771.532d=a9015a009f654717.1683272866.8.1683621946.1683621861.; _uetsid=10e50600ed6511ed9a3c6fbf78f1504c; _uetvid=1f924d80eb1911ed8ed6f111321f5814; __hssc=191717877.3.1683621885931; stg_last_interaction=Tue%2C%2009%20May%202023%2008:47:34%20GMT; _gali=btnQuantityDiscount; _ga_7YN4G92YEY=GS1.1.1683621840.9.1.1683622054.46.0.0',
                        # 'Referer': 'https://www.igus.com/product/732?artNr=WS-10-30S',
                        'Sec-Fetch-Dest': 'iframe',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    params = {
                        'page': 'PricePopup',
                        'artno': f'{sku}',
                    }
                    price_list = []

                    available_to_checkout = False
                    instock = False
                    resp = requests.get('https://www.igus.com/myigus/default.aspx', params=params, headers=headers)
                    response_price = Selector(text=resp.text)
                    price3 = response_price.xpath('//table[@id="staffel"]//tr')
                    if price3:
                        for p in price3:
                            price_dict = {}
                            price = p.xpath('.//td[2]//text()').get()
                            min_qty = p.xpath('.//td[1]//text()').get().replace('from', '').replace("m", "").replace("Upon request", "1").replace("Pc.", "").replace("ft", "")
                            try:
                                if price:
                                    price_dict['min_qty'] = int(min_qty)
                                    if price_dict['min_qty'] <1:
                                        price_dict['min_qty'] = 1
                                    if "Upon request" in price:
                                        pricing_string = 'Call For Price'
                                        price_dict['price_string'] = pricing_string.strip()
                                        price_list.append(price_dict)

                                    else:
                                        pricing1 = price.split("USD/Pc")[0].replace("USD/m", "").replace("USD/Pc.", "").replace("USD/ft", "").replace("+", "").replace(",", "").strip()
                                        price_dict['price'] = float(pricing1)
                                        price_dict['currency'] = 'USD'
                                        price_list.append(price_dict)
                                        available_to_checkout =  True
                                        instock =  True

                                else:
                                    price_dict['min_qty'] = int(min_qty)
                                    if price_dict['min_qty'] < 1:
                                        price_dict['min_qty'] = 1
                                    price_dict['price_string'] = 'Call For Price'
                                    price_list.append(price_dict)
                            except:pass

                    try:
                        p_id = url.split('product/')[1].split('?')[0]
                    except:
                        p_id = response.xpath('//link/@href').get('').split('/')[-1]

                    headers = {
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/json; charset=UTF-8',
                        # 'Cookie': '_gcl_au=1.1.676755666.1683272864; specificga=GA1.2.10435550.1683272865; rollupga=GA1.2.10435550.1683272865; _evga_a655={%22uuid%22:%22fff26fcbcd97580a%22}; _sfid_efb2={%22anonymousId%22:%22fff26fcbcd97580a%22%2C%22consents%22:[]}; _fbp=fb.1.1683272866222.569416171; CookiesInfo=1; hubspotutk=f90ec5a31fc95f11504ae47270ff359f; stg_returning_visitor=Fri%2C%2005%20May%202023%2007:54:27%20GMT; _gid=GA1.2.1049304933.1683525385; specificga_gid=GA1.2.883515036.1683525385; rollupga_gid=GA1.2.240324026.1683525385; ln_or=eyJOVUxMIjoiZCIsIjQ0MDI4MzQsTlVMTCI6ImQifQ%3D%3D; stg_traffic_source_priority=1; _pk_ses.6cffafdd-f01c-4312-8dae-3ec1d1be0771.532d=*; DomainUserMapping=isLocalPriceDomain=1&uc=in&ud=www.igus.in&ucn=India; ASP.NET_SessionId=kmjd2venmybmzwe4lbc0wrlt; Global_SessionId=zsbmjf10xjiicz1ds1blvxfb; server=1; __hstc=191717877.f90ec5a31fc95f11504ae47270ff359f.1683272868774.1683881859805.1683881871390.36; __hssrc=1; liveagent_invite_rejected_5732X000000Gr8i=true; __hssc=191717877.7.1683881871390; _gat_UA-45372250-1=1; _dc_gtm_UA-51039103-4=1; _dc_gtm_UA-51039103-2=1; _ga_7YN4G92YEY=GS1.1.1683881858.34.1.1683884498.59.0.0; _ga=GA1.1.10435550.1683272865; _pk_id.6cffafdd-f01c-4312-8dae-3ec1d1be0771.532d=a9015a009f654717.1683272866.34.1683884499.1683881859.; stg_last_interaction=Fri%2C%2012%20May%202023%2009:41:40%20GMT; _uetsid=10e50600ed6511ed9a3c6fbf78f1504c; _uetvid=1f924d80eb1911ed8ed6f111321f5814',
                        'Origin': 'https://www.igus.com',
                        # 'Referer': 'https://www.igus.com/product/732?artNr=WS-10-30',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest',
                        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    json_data = {
                        'PageId': f'{p_id}',
                        'OrderTypeId': '1210',
                        'ArtNr': f'{sku}',
                        'MinLength': '160',
                        'MaxLength': '4000',
                        'Discontinued': False,
                    }

                    response_avv = requests.post('https://www.igus.com/Product/GetOrderBox',headers=headers, json=json_data)
                    # dd = json.loads(response_avv.text)
                    dd = json.loads(response_avv.text)
                    a = dd['Html']
                    s = Selector(text=a)

                    estimated_lead_time = s.xpath('//a[@class="link link--icon igus007BuyBox__availability availability--fast"]//div[@class="link__text"]//text() | //a[@class="link link--icon igus007BuyBox__availability availability--secondary"]//div[@class="link__text"]//text()').get()
                    if estimated_lead_time is None:
                        estimated_lead_time = ''
                    if "Ready to ship within" in estimated_lead_time:
                        estimated_lead_time = [{
                            'min_qty': 1,
                            'time_to_ship': {
                                'raw_value': estimated_lead_time
                            }
                        }]

                    elif "Ready to ship in" in estimated_lead_time:
                        estimated_lead_time = [{
                            'min_qty': 1,
                            'time_to_ship': {
                            'raw_value': estimated_lead_time
                            }
                        }]

                    if estimated_lead_time:
                        estimated_lead_time = estimated_lead_time
                    else:
                        estimated_lead_time = None
                    result['vendor'] = vendor
                    result['sku'] = sku
                    result['pdp_url'] = url
                    result['price'] = price_list
                    result['available_to_checkout'] = available_to_checkout
                    result['in_stock'] = instock
                    result['lead_time'] = estimated_lead_time
                    return {'statusCode': 200,
                            'data': result}
                except Exception as e:
                    error['statusCode'] = 500
                    error['error_message'] = "Internal server error" + str(e)
                    return error
            else:
                error['statusCode'] = 410
                error['error_message'] = "Product not found"
                return error
        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = "Internal server error" + str(e)
            return error
    elif response1.status_code==404:
        error['statusCode'] = 410
        error['error_message'] = "Page not found"
        return error
    else:
        error['statusCode'] = 408
        error['error_message'] = "Request timeout, failed to reach host"
        return error

if __name__ == '__main__':
    event = {"sku": "CFBUS-PUR-001", "vendor": "igus", "pdp_url": "https://www.igus.com/product/CFBUS_PUR"}
    print(igus(event["pdp_url"],event["sku"],event["vendor"]))