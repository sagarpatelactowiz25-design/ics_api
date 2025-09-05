import json
import time
from curl_cffi import requests
# import requests
from parsel import Selector
import re
from datetime import datetime,timedelta
max_entries = 5
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_uetsid=7ee3ab000b1811f0a46c9fa6c2a351fd; _uetvid=7ee39d100b1811f09fe4d73e1c1177f9; _gcl_au=1.1.585123560.1743086028; _ga=GA1.1.1860600884.1743086028; _ga_N9X9YNMPT5=GS1.1.1743086028.1.1.1743086028.60.0.0; _hjSessionUser_3690666=eyJpZCI6ImJmYWYwZjk5LWE0ZmUtNTlkYy1iYWNmLWQ2NzZlZjM3MTJiNCIsImNyZWF0ZWQiOjE3NDMwODYwMjg1MjMsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_3690666=eyJpZCI6IjczMDY4ZjgwLWE2MDgtNDFlZS1hOTBlLTczOTQ2OWM2MWVhNSIsImMiOjE3NDMwODYwMjg1MjQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; form_key=uQDtRVe591Phrg5G; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; zCountry=IN; zHello=1; mage-messages=; _ALGOLIA=anonymous-89376ee6-65cf-4f0c-8106-5b0f093ddfc7; _rdt_uuid=1743086029358.1e1a6549-75c8-428e-973c-ccb7582d42ab; _ga_752JYSYLMK=GS1.1.1743086029.1.0.1743086029.0.0.0; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; rj2session=66941ad1-d6a1-4849-abbd-8d4d26ffe9b5; __hstc=116416729.29d1778303ca4c4f6b335430117459a2.1743086030286.1743086030286.1743086030286.1; hubspotutk=29d1778303ca4c4f6b335430117459a2; __hssrc=1; __hssc=116416729.1.1743086030287; PHPSESSID=h943huheh2k2gsk9he2k4i6m8a; form_key=uQDtRVe591Phrg5G; wp_ga4_customerGroup=NOT%20LOGGED%20IN; _zitok=89bce74f6890f73d771a1743086030; private_content_version=590dc18c855323f344a223755d2764d8',
}
proxy = {
    "http": "http://2d76727898034978a3091185c24a5df27a030fdc3f8:@proxy.scrape.do:8080",
    "https": "http://2d76727898034978a3091185c24a5df27a030fdc3f8:@proxy.scrape.do:8080"
}
def galco(pdp_url,sku,vendor="galco"):
    try:
        for i in range(max_entries):
            url_request = requests.get(url = pdp_url,headers=headers,
                                       proxies =proxy,
                                       verify = False,
                                       impersonate="edge99"
                                       )
            if url_request.status_code == 200:
                break
        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}
            pass
        # Checking if status code and the product name  is also in the response text
        if url_request.status_code == 200:
            response = Selector(text = url_request.text)
            if response.xpath('//h1[@class="page-title"]/span[@itemprop="name"]'):
                # Extracting sku
                scraped_sku = response.xpath('//span[@data-ui-id="page-title-wrapper"]/text()').get()
                if scraped_sku != sku:
                    return {"statusCode": 404,
                            "error_message": f"Scraped SKU:{scraped_sku} does not match input SKU:{sku}"}
                else:
                    # In stock checking and Availble to checkout
                    in_stock_text = response.xpath('//th[@class="col label" and contains(text(),"In Stock")]/parent::tr/td/text()').get()
                    if "Yes" in in_stock_text:
                        in_stock = True
                    else:
                        in_stock = False

                    # Available
                    available_to_checkout_text = response.xpath('//button[@type="submit"]//span[contains(text(),"Add to Cart")]')
                    available_to_checkout = True if available_to_checkout_text else False
                    # lead_time
                    uom = response.xpath('//div/@data-uom').get()
                    lead_Time_value = response.xpath('//div[@class="tooltip-content"]/text()').get()
                    estimated_lead_time = {
                        'min_qty': 1,
                        'time_to_ship': lead_Time_value.strip()
                    }
                    # lead_time and price_request
                    for i in range(max_entries):
                        data = {
                            'parts[0][part_number]': sku,
                            'parts[0][uom]': uom,
                            'parts[1][part_number]': sku,
                            'parts[1][uom]': uom,
                        }
                        price_url = 'https://www.galco.com/dynamicdata/api/getdata/'
                        # price_url = "http://api.scrape.do/?token={}&url={}".format("2d76727898034978a3091185c24a5df27a030fdc3f8", "https://www.galco.com/dynamicdata/api/getdata/")
                        price_headers =  {
                            'accept': '*/*',
                            'accept-language': 'en-US,en;q=0.9',
                            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            # 'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0NzQ1OTQiLCJhcCI6IjEzODYxODM4NDkiLCJpZCI6IjViZDFkYzhkODFiNjU2MjciLCJ0ciI6ImY2M2M5MGFhNzcyYjIyNGMwZDM4NWUyYjdlZmNhNWM3IiwidGkiOjE3NDMxNDUxNDA0NTZ9fQ==',
                            'origin': 'https://www.galco.com',
                            'priority': 'u=1, i',
                            'referer': 'https://www.galco.com/dms3101a18-22p-f-fujikura-formerly-ddk.html',
                            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            # 'traceparent': '00-f63c90aa772b224c0d385e2b7efca5c7-5bd1dc8d81b65627-01',
                            # 'tracestate': '4474594@nr=0-1-4474594-1386183849-5bd1dc8d81b65627----1743145140456',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                            'x-requested-with': 'XMLHttpRequest',
                            # 'cookie': '_gcl_au=1.1.585123560.1743086028; _ga=GA1.1.1860600884.1743086028; form_key=uQDtRVe591Phrg5G; zHello=1; _ALGOLIA=anonymous-89376ee6-65cf-4f0c-8106-5b0f093ddfc7; rj2session=66941ad1-d6a1-4849-abbd-8d4d26ffe9b5; hubspotutk=29d1778303ca4c4f6b335430117459a2; __hssrc=1; wp_ga4_customerGroup=NOT%20LOGGED%20IN; _zitok=89bce74f6890f73d771a1743086030; _hjSessionUser_3690666=eyJpZCI6ImJmYWYwZjk5LWE0ZmUtNTlkYy1iYWNmLWQ2NzZlZjM3MTJiNCIsImNyZWF0ZWQiOjE3NDMwODYwMjg1MjMsImV4aXN0aW5nIjp0cnVlfQ==; zCountry=IN; _hjSession_3690666=eyJpZCI6ImVmZTNkY2NlLWMwM2UtNDU3MS04MTg1LWMzMmJjYmY0NmUyZSIsImMiOjE3NDMxNDUxMzU1MDUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _ga_N9X9YNMPT5=GS1.1.1743145135.2.1.1743145135.60.0.0; _uetsid=7ee3ab000b1811f0a46c9fa6c2a351fd; _uetvid=7ee39d100b1811f09fe4d73e1c1177f9; _ga_752JYSYLMK=GS1.1.1743145135.2.0.1743145135.0.0.0; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; _rdt_uuid=1743086029358.1e1a6549-75c8-428e-973c-ccb7582d42ab; mage-messages=; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; __hstc=116416729.29d1778303ca4c4f6b335430117459a2.1743086030286.1743086030286.1743145137036.2; __hssc=116416729.1.1743145137036; form_key=uQDtRVe591Phrg5G; PHPSESSID=ma9o0vocoh0abscfkjktoaghnv; private_content_version=ee745275efbec72f434050e9773e3079',
}
                        price_cookies = {
                            '_gcl_au': '1.1.585123560.1743086028',
                            '_ga': 'GA1.1.1860600884.1743086028',
                            'form_key': 'uQDtRVe591Phrg5G',
                            'zHello': '1',
                            '_ALGOLIA': 'anonymous-89376ee6-65cf-4f0c-8106-5b0f093ddfc7',
                            'rj2session': '66941ad1-d6a1-4849-abbd-8d4d26ffe9b5',
                            'hubspotutk': '29d1778303ca4c4f6b335430117459a2',
                            '__hssrc': '1',
                            'wp_ga4_customerGroup': 'NOT%20LOGGED%20IN',
                            '_zitok': '89bce74f6890f73d771a1743086030',
                            '_hjSessionUser_3690666': 'eyJpZCI6ImJmYWYwZjk5LWE0ZmUtNTlkYy1iYWNmLWQ2NzZlZjM3MTJiNCIsImNyZWF0ZWQiOjE3NDMwODYwMjg1MjMsImV4aXN0aW5nIjp0cnVlfQ==',
                            '__hstc': '116416729.29d1778303ca4c4f6b335430117459a2.1743086030286.1743163110592.1743165528374.4',
                            'private_content_version': '2f38285f485d23ef77c8f1a9e82b8098',
                            'zCountry': 'IN',
                            '_hjSession_3690666': 'eyJpZCI6ImYzNDZhYzkzLTRlMmYtNDg1My04YzI3LWQ1ZjFiMGE1YzBlMSIsImMiOjE3NDMxNjk4OTcwOTUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
                            '_ga_N9X9YNMPT5': 'GS1.1.1743169896.5.1.1743169897.59.0.0',
                            '_ga_752JYSYLMK': 'GS1.1.1743169896.5.1.1743169897.0.0.0',
                            '_uetsid': '7ee3ab000b1811f0a46c9fa6c2a351fd',
                            '_uetvid': '7ee39d100b1811f09fe4d73e1c1177f9',
                            '_rdt_uuid': '1743086029358.1e1a6549-75c8-428e-973c-ccb7582d42ab',
                            'mage-cache-storage': '{}',
                            'mage-cache-storage-section-invalidation': '{}',
                            'mage-cache-sessid': 'true',
                        }
                        price_request = requests.post(price_url,
                                                 headers=price_headers,
                                                impersonate = "edge99",
                                                #       proxies=proxy,
                                                      verify = False,
                                                      cookies = price_cookies,
                                                 data=data)
                        if price_request.status_code == 200:
                            break
                    else:
                        return {'statusCode': 408,
                                'error_message': 'Request timeout, failed to reach host'}

                    if price_request.status_code == 200:
                        # lead_time = response.xpath('//div[@class="product-info-delivery-note"]//text()').get()
                        price_json = json.loads(price_request.text)
                        # if in_stock == False:
                        #     try:
                        #         lead_time = int(price_json[f'{scraped_sku}']['lead_time'])
                        #     except:
                        #         lead_time = None
                        #     l = int(lead_time)
                        #     if l <= 10 and lead_time:
                        #         estimated_lead_time = []
                        #         current_date =datetime.now()
                        #         desired_date = current_date + timedelta(days=10)
                        #         formatted_date = desired_date.strftime("%A, %B %dth")
                        #         lead_time = {
                        #             'raw_value': 'Available For Back Order with an estimated ship date of' + ' ' + formatted_date}
                        #         estimated_lead_time.append(
                        #             {
                        #                 'min_qty': 1,
                        #                 'time_to_stock': lead_time
                        #             }
                        #         )
                        #     elif 10 < l <= 365 and lead_time:
                        #         estimated_lead_time = []
                        #         current_date = datetime.now()
                        #         days_to_add = l
                        #         desired_date = current_date + timedelta(days=days_to_add)
                        #         formatted_date = desired_date.strftime("%A, %B %dth")
                        #
                        #         lead_time = {
                        #             'raw_value': 'Available For Back Order with an estimated ship date of' + ' ' + formatted_date}
                        #         estimated_lead_time.append(
                        #             {
                        #                 'min_qty': 1,
                        #                 'time_to_stock': lead_time
                        #             }
                        #         )
                        #     else:
                        #         estimated_lead_time = None
                        # else:
                        #     if not lead_time :
                        #         estimated_lead_time = None
                        #     else:
                        #
                        #         estimated_lead_time = []
                        #         lead_time = lead_time.replace("\n", '').strip()
                        #         lead_time = {'raw_value': lead_time}
                        #         estimated_lead_time.append(
                        #             {
                        #                 'min_qty': 1,
                        #                 'time_to_ship': lead_time
                        #             }
                        #         )

                        # Price extraction
                        price_list = []
                        try:
                            price = price_json[scraped_sku]["price"]
                            if price != 0:
                                price_list.append({"min_qty": 1, "price": float(price), "currency": "USD"})
                            else:
                                price_list.append({"min_qty": 1, "price_string": "Call For Price"})
                        except:
                            price_list.append({"min_qty":1,"price_string":"Call For Price"})

                        try:
                            multiple_price = price_json[scraped_sku]["tiers"]
                            for price_ in multiple_price:
                                try:
                                    qty = price_["qty"]
                                    price = float(price_["price"])
                                    price_list.append({"min_qty": qty, "price": price, "currency": "USD"})
                                except:
                                    pass
                        except:
                            pass

                        data = {'vendor': vendor, 'pdp_url': pdp_url, 'sku': sku, 'price': price_list,
                                'lead_time': estimated_lead_time, 'available_to_checkout': available_to_checkout,
                                'in_stock': in_stock}
                        return {'statusCode': 200,
                                'data': data}
                    else:
                        return {'statusCode': 404,
                                'error_message': 'Product not found'}

            else:

                return {'statusCode': 404,
                        'error_message': 'Product not found'}

        else:
            return {'statusCode': 404,
                    'error_message': 'Product not found'}
    except Exception as e:
        return {"statusCode": 500,
                    "error_message": "Internal server error" + str(e)}



if __name__ == '__main__':
    # event = {"pdp_url": "https://www.galco.com/xne-8ai-u-i-4pt-ni-cutler-hammer-div-of-eaton-corp.html",
    #     "sku": "XNE-8AI-U/I-4PT/NI", "vendor": "galco"}
    event = {"pdp_url": "https://www.galco.com/xne-8ai-u-i-4pt-ni-cutler-hammer-div-of-eaton-corp.html",
        "sku": "XNE-8AI-U/I-4PT/NI", "vendor": "galco"}
    # event  = {
    #     "pdp_url": "https://www.galco.com/dms3101a18-22p-f-fujikura-formerly-ddk.html",
    #     "sku": "DMS3101A18-22P-F", "vendor": "galco"}
#
#     # event = {
#     #     "pdp_url" :"https://www.ellsworth.com/products/by-manufacturer/bostik/sealants/silyl-terminated-polymer/bostik-70-03a-silyl-modified-polymer-sealant-black-290-ml-cartridge/",
#     #     "sku":"A61019"
#     #
#     #     # "pdp_url" :"https://www.ellsworth.com/products/dispensing-equipment-supplies/dispensing-systems-fluid/hand-held-1-part-applicators/fisnar-fmg-120t-metal-manual-dispense-kit-12-oz/",
#     #     # "sku":"FMG-120T"
#     # }
    print(galco(event["pdp_url"],event["sku"]))

