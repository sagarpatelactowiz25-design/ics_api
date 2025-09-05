import json
from parsel import Selector
max_retires = 5
import requests
import api_key

token=api_key.scraperDo_key

def hisco(pdp_url, sku, vendor='hisco'):
    try:
        if 'https://www.hisco.com/' not in pdp_url:
            return {"statusCode": 410,
                    "error_message": "Product not found"}
        item = {}
        error = {}

        for i in range(max_retires):
            pdp_urls = f"http://api.scrape.do?token={token}&url={pdp_url}"
            url_request = requests.get(url=pdp_urls)
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

        selector = Selector(text=url_request.text)
        available_to_checkout = selector.xpath('//button[@data-test-selector="addProductToCart"]/span/text()').getall()
        final_dict = {}

        path = pdp_url.split("/Product/")[-1]
        proxy = {
            "http": f"http://{token}:@proxy.scrape.do:8080?country=US",
            "https": f"http://{token}:@proxy.scrape.do:8080?country=US"
        }
        url1 = f"https://www.hisco.com/api/v1/catalogPages?path=%2FProduct%2F{path}"
        urls1 = f"http://api.scrape.do?token={token}&url={url1}"
        params = {
            'path': f'/Product/{path}',
        }
        # result = requests.get(url=urls1,params=params)
        result = requests.get(url=url1,params=params,proxies=proxy,
                              verify=False)
        # result = requests.get(url=urls,params=params,headers=headers,cookies=cookies,impersonate='edge99')

        data = json.loads(result.text)
        uri = data['productId']
        params = {
            'expand': 'detail,specifications,content,images,documents,attributes,variantTraits,badges',
            'includeAttributes': 'includeOnProduct,notFromCategory',
            'addToRecentlyViewed': 'true',
            'categoryId': uri,
        }

        url3 = f'https://www.hisco.com/api/v2/products/{uri}?expand=detail%2Cspecifications%2Ccontent%2Cimages%2Cdocuments%2Cattributes%2CvariantTraits%2Cbadges&includeAttributes=includeOnProduct&addToRecentlyViewed=true'
        urls3 = f"http://api.scrape.do?token={token}&url={url3}"
        result2 = requests.get(url=url3,params=params,verify=False,proxies=proxy)

        data2 = json.loads(result2.text)
        brand_new_min_qty = data2['minimumOrderQty']
        p_sku = data2['detail']['sku']
        if sku != p_sku:
            sku = sku.upper()

        if sku != p_sku:
            error['statusCode'] = 410
            error['error_message'] = f"Scraped SKU:{p_sku} does not match input SKU:{sku}"
            return error

        else:
            instock = data2['inventoryDetail']['inStock']
            min_qty = data2['minimumOrderQty']
            lead_time = data2['inventoryDetail']['leadTime']
            unit_of_measure = data2['properties']['unitOfMeasureSelling']

            json_data = {
                'productPriceParameters': [
                    {
                        'productId': uri,
                        'unitOfMeasure': unit_of_measure,
                        'qtyOrdered': min_qty,
                    },
                ],
            }
            url4 = 'https://www.hisco.com/api/v1/realtimepricing'
            urls4 = f"http://api.scrape.do?token={token}&url={url4}"
            result3 = requests.post(url=urls4, json=json_data,)

            data3 = json.loads(result3.text)
            price_list = []
            json_price = data3['realTimePricingResults']
            min_quantaty = []
            for i in json_price:
                try:
                    price_json = i['unitRegularBreakPrices']
                    for p in price_json:
                        min_qty = p['breakQty']
                        if min_qty not in min_quantaty:
                            min_quantaty.append(min_qty)
                        else:
                            continue
                        price = p['breakPrice']
                        if price:
                            price = round(price, 2)
                            if price == 0.0 or price == 0.00 or price == 0:
                                price_list.append({'min_qty': int(min_qty),
                                                   'price_string': 'Call for price'})
                            else:
                                price_list.append({'currency': 'USD',
                                                   'min_qty': int(min_qty),
                                                   'price': price})
                except:
                    min_qty = 1
                    try:
                        price= i['actualPrice']
                        if price==0.0 or price==0.00 or price==0:
                            price_list.append({'min_qty': int(min_qty),
                                               'price_string': 'Call for price'})
                        else:
                            price = round(price, 2)
                            price_list.append({'currency': 'USD',
                                           'min_qty': int(min_qty),
                                           'price': price})
                    except:
                        price_list.append({'min_qty': int(min_qty),
                                           'price_string': 'Call for price'})

            json_data = {
                'productId': uri,
                'qtyOrdered': brand_new_min_qty,
                'unitOfMeasure': unit_of_measure,
            }
            url5 = 'https://www.hisco.com/api/v1/carts/current/cartlines'
            urls5 = f"http://api.scrape.do?token={token}&url={url5}"
            response1 = requests.post(url = urls5, json=json_data)
            just_response = response1.text
            just_json = json.loads(just_response)
            new_price_list = []
            try:
                minimum_qty = just_json['qtyOrdered']
                main_price = just_json['pricing']['actualPrice']
                main_price = round(main_price, 2)
                if main_price == 0.0 or main_price == 0.00 or main_price == 0:
                    new_price_list.append({'min_qty': int(minimum_qty),
                                           'price_string': 'Call for price'})
                else:
                    new_price_list.append({'currency': 'USD',
                                           'min_qty': int(minimum_qty),
                                           'price': main_price})
            except:
                new_price_list.append({'min_qty': int(brand_new_min_qty),
                                       'price_string': 'Call for price'})

            if just_json:
                try:
                    if just_json['message']:
                        message = just_json['message']
                        if message=='The requested product cannot be added to the cart.':
                            available_to_checkout = False
                        else:
                            available_to_checkout = True
                    else:
                        available_to_checkout = True
                except:
                    available_to_checkout = True
            all_min_qty = []
            for one in price_list:
                all_min_qty.append(one['min_qty'])
            try:
                for x in price_list:
                    if x['min_qty']<new_price_list[0]['min_qty']:
                        continue
                    elif x['min_qty']==new_price_list[0]['min_qty']:
                        pass
                    else:
                        new_price_list.append(x)
            except:
                pass

            data_dict = {'vendor': vendor,
                         'pdp_url': pdp_url,
                         'sku': p_sku,
                         'price': new_price_list,
                         'lead_time': [{'min_qty':brand_new_min_qty,
                                       'time_to_ship':{
                                           'raw_value':str(lead_time) + ' days'
                                       }}],
                         'available_to_checkout': available_to_checkout,
                         'in_stock': instock}

            return {'statusCode': 200,
                    'data': data_dict}

    except Exception as e:
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}


# if __name__ == '__main__':
#     #Input Params
#     event={"pdp_url": "https://www.hisco.com/Product/00021200030987-31196", "sku": "00021200030987-31196", "vendor": "hisco"}
#     vendor = "hisco"
#     sku = event['sku']
#     pdp_url = event['pdp_url']
#     print(json.dumps(hisco(pdp_url,sku,vendor)))

