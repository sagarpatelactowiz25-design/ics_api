import json
import time

import requests
# import api_key
from parsel import Selector

final_list = []


token='f42a5b59aec3467e97a8794c611c436b91589634343'

def globalindustrial(url, sku=None, zipcode='94104', min_qty=None):
    data = {}
    error = {}
    # "http://{}:geoCode=us@proxy.scrape.do:8080
    try:
        proxy =  {
    "http": f"http://{token}:geoCode=us@proxy.scrape.do:8080",
    "https": f"http://{token}:geoCode=us@proxy.scrape.do:8080",
    # "http": f"http://{token}:@proxy.scrape.do:8080?country=US",
    # "https": f"http://{token}:@proxy.scrape.do:8080?country=US"
}
        trace = str(int(time.time() * 1000))
        try:
            response1 = requests.get(url, proxies=proxy, verify=False, timeout=40)
        except Exception as e:
            print(e)
            response1 = requests.get(url, proxies=proxy, verify=False, timeout=40)
        if response1.status_code != 200:
            # for k_ in range(0, 5):
            #     response1 = requests.get(url, proxies=proxy, verify=False, timeout=40)
            #     if response1.status_code == 200:
            #         break
            for k_ in range(0, 5):
                response1 = requests.get(url)
                if response1.status_code == 200:
                    break
        if response1.status_code == 200:
            pass
        else:
            return {'statusCode': 408, 'error_message': 'Request timeout, failed to reach host'}
        # if "/c/[[...route]]" in response1.text:
        #     error['statusCode'] = 404
        #     error['error_message'] = 'Product not found'
        #     return error
        # else:
        response = Selector(text=response1.text)
    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = "Internal error: " + str(e)
        return error
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'BearereyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJERVYifQ.uOFB7h7_Aw6jbA1HSqVJ44tKMO7E1ljz1kV_JddeKL64YCOH57-l1ZX2Lly-Jnhdnxk3xMAeW5FawAgymEaMKA',
        'client_id': 'GEC',
        'content-type': 'application/json',
        # 'cookie': 'x-location=173.239.214.43=dummy; _cs_id=2bb03ade-a482-af01-a3be-b62728f0fb70.1717573738.7.1717683446.1717683441.1708624099.1751737738840.1; _cs_s=2.5.0.1717685246413; gec-test-rvid=b44413f9-9a97-4776-8465-07f32ffb953e; _ga_377MJKHZ21=GS1.1.1717683445.7.0.1717683447.0.0.0; _pk_id.b713c95c-55b4-4001-b825-d6b61c5f12e6.4282=d06c417c91d1cea2.1717573755.8.1717683450.1717683450.; _ga_EJJQPMP9YF=GS1.1.1717683446.3.0.1717683450.56.0.0; _br_uid_2=uid%3D5478427534019%3Av%3D15.0%3Ats%3D1717573757573%3Ahc%3D31; ltk-product-QOH=0; lastRskxRun=1717683451891; stg_externalReferrer=; stg_traffic_source_priority=1; rCookie=d65r7897tcqw0yk50m07ylx3celjs; gec-test-uuid=349fb787-f83e-4f47-8f4a-18284b878f3f; SESSION_ID=173-239-214-43-00efc4ba-2495-4362-a74a-308ef8ad945c; Authorization=Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJERVYifQ.uOFB7h7_Aw6jbA1HSqVJ44tKMO7E1ljz1kV_JddeKL64YCOH57-l1ZX2Lly-Jnhdnxk3xMAeW5FawAgymEaMKA; x-sid=site42; _cheq_rti=zQ8eby3wjbgpLitfLl7GkH6rQRc=cft7RWdusFMrsjN9jOeqpcUg+URfFjU0zX0gELduawH1IJdsvqD5Z5RMapaAM6uCGQw/Kp201enfiUO9cYO5PGNXp5Ox6YWNTHfPIHPurRKv9zhA6PpoTkixYf75menQTNE=; SESSION=173-239-214-43-00efc4ba-2495-4362-a74a-308ef8ad945c; gec-gl-zip=97527; stg_last_interaction=Thu%2C%2006%20Jun%202024%2014:18:29%20GMT; _fbp=fb.1.1717683512909.52811950743212003',
        'origin': 'https://www.globalindustrial.com',
        'priority': 'u=1, i',
        'referer': f'{url}',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'trace': trace,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    try:

        json1 = response.xpath('//script[@id="__NEXT_DATA__"]//text()').get('')
        json_data = json.loads(json1)
        try:
            try:
                product = json_data['props']['pageProps']['product']
            except:
                error['statusCode'] = 410
                error['error_message'] = "Product Not Found"
                return error
            try:
                SESSION_ID = json_data['props']['pageProps']['headers'].get('set-cookie')[0].split(';')[0].split('=')[1]
                itemKey = json_data['props']['pageProps']['product'].get('itemKey')
            except:
                pass
        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = "Internal error: " + str(e)
            return error
        try:
            if not min_qty:
                min_qty = 1
            cookies = {
                'SESSION_ID': SESSION_ID,
            }
            params = {
                'nocache': f'{trace}',
            }
            json_data = {
                'cartItemInputDTOList': [
                    {
                        'itemKey': itemKey,
                        'qty': int(min_qty),
                    },
                ],
            }
            # Please do not comment this code
            response_addToCart = requests.post(
                'https://www.globalindustrial.com/cartApis/cart/addToCart',
                params=params,
                cookies=cookies,
                headers=headers,
                json=json_data,
            )
            responseshipMethods = requests.get(
                f'https://www.globalindustrial.com/freightApis/freight/shipMethods/0/{zipcode}',
                params=params,
                cookies=cookies,
                headers=headers,

            )
            cart_summary = []
            try:
                shipMethodsjson = json.loads(responseshipMethods.text)
                cart_summary = []
                for ii in shipMethodsjson.get('shippingMethods'):
                    carrierKey = ii.get('carrierKey')
                    serviceKey = ii.get('serviceKey')
                    shippingMethod = ii.get('shippingMethod')
                    zipcode=(zipcode.split('-'))[0]
                    json_data = {
                        'zip': f'{zipcode}',
                        'carrierKey': f'{carrierKey}',
                        'serviceKey': f'{serviceKey}',
                        'flagResidential': False,
                        'page': 'viewcart',
                    }
                    response_shipcost = requests.post(
                        'https://www.globalindustrial.com/freightApis/freight/calculateFreight',
                        params=params,
                        cookies=cookies,
                        headers=headers,
                        json=json_data,
                    )

                    try:
                        dict1 = {}
                        shipping_costjson = json.loads(response_shipcost.text)
                        deliveryMessage = shipping_costjson.get('shippingList')[0].get('deliveryMessage')
                        freight = shipping_costjson.get('shippingGroupList')[0].get('freight')
                        dict1['zipcode'] = int(zipcode)
                        dict1['shipping_method'] = shippingMethod
                        dict1['shipping_cost'] = freight
                        dict1['delivery_date'] = deliveryMessage
                        cart_summary.append(dict1)

                    except:
                        # cart_dict = {}

                        cart_summary = [{"statusCode": 410, "errorMessage": "Invalid zipcode"}]
            except:
                pass
            # msg1 = f'In this Zipcode Shipping Cost Not Available'
            # cart_summary = [{"statusCode":404,"Message": msg1}]
            # print('shipping response', response_shipcost.text
            #       )
        except:
            pass
        data['vendor'] = 'globalindustrial'
        try:
            data['sku'] = product.get('legacyNumber')
            if sku.strip() != data['sku'].strip():
                error['statusCode'] = 410
                error['error_message'] = f"Scraped SKU:{data['sku']} does not match input SKU:{sku}"
                return error
        except Exception as e:
            print(e)
            data['sku'] = None
            if not data['sku']:
                error['statusCode'] = 500
                error['error_message'] = "Error while scraping SKU"
                return error

        data['pdp_url'] = url

        price_list = []
        estimated_list = []

        estimate = product.get('availabilityGTM')
        sale_qty1 = product.get('qty')
        try:
            num_price = len(product.get('priceBreaks'))
            estimate_count = 1
            sku_unit = product.get('unit')
            check_price = product.get('price')
            first_price = product.get('priceBreaks')[0].get('priceCatalogFormattedString').split(';')[1].strip()
            for pr in product.get('priceBreaks'):
                price_dict = {}
                if num_price > 1:
                    qty1 = pr.get('qtyStart')
                else:
                    qty1 = sale_qty1
                final_price = pr.get('priceCatalogFormattedString').split(';')[1].strip()
                if qty1:
                    if qty1:
                        final_qty = qty1
                    else:
                        final_qty = 1

                    if estimate_count == 1:
                        if estimate:
                            est = estimate.split('|')[1].strip()
                            if 'ship' in est.lower():
                                estimated_list.append({
                                    'min_qty': final_qty,
                                    'time_to_ship': {
                                        'raw_value': est
                                    }
                                })
                            elif 'around' in est.lower():
                                estimated_list.append({
                                    'min_qty': final_qty,
                                    'time_to_arrive': {
                                        'raw_value': est
                                    }
                                })

                estimate_count += 1

                price_dict['min_qty'] = final_qty
                if final_price:
                    if len(product.get('priceBreaks')) == 1:
                        final_price = float(str(final_price).replace(',', '').strip()) * sku_unit
                        price_dict['price'] = round(float(str(final_price).replace(',', '').strip()), 2)
                        price_dict['currency'] = 'USD'

                    elif str(first_price).replace(',', '').strip() != float(check_price):
                        final_price = float(str(final_price).replace(',', '').strip()) * sku_unit
                        price_dict['price'] = round(float(str(final_price).replace(',', '').strip()), 2)
                        price_dict['currency'] = 'USD'
                    else:
                        price_dict['price'] = round(float(str(final_price).replace(',', '').strip()), 2)
                        price_dict['currency'] = 'USD'
                else:
                    price_dict['price_string'] = 'Call for price'.title()

                price_list.append(price_dict)
        except:
            # if estimate:
                est = estimate.split('|')[1].strip()
                if 'ship' in est.lower():
                    estimated_list.append({
                        'min_qty': sale_qty1,
                        'time_to_ship': {
                            'raw_value': est
                        }
                    })
                elif 'around' in est.lower():
                    estimated_list.append({
                        'min_qty': sale_qty1,
                        'time_to_arrive': {
                            'raw_value': est
                        }
                    })
                price_dict = {}
                price_dict['min_qty'] = sale_qty1
                price_dict['price_string'] = 'Call for price'.title()

                price_list.append(price_dict)

        data['price'] = price_list
        instock1 = product.get('availabilityGTM')
        if instock1:
            if 'instock' in instock1.lower() or "expecte" in instock1.lower() or 'available' in instock1.lower() or 'usually ships in' in instock1.lower():
                if product.get('flagCallForPrice'):
                    instock = False
                else:
                    instock = True
            else:
                instock = False
            data['in_stock'] = instock
        else:
            instock = True
            data['in_stock'] =  True
        data['available_to_checkout'] = instock

        if estimated_list:
            data['lead_time'] = estimated_list
        else:
            data['lead_time'] = None
        if cart_summary:
            data['cart_summary'] = cart_summary
        else:
            data['cart_summary'] = None
        return {'statusCode': 200,
                'data': data}

    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = "Internal error: " + str(e)
        return error

# if __name__ == '__main__':
# 
#     event = {"sku": "WBB2185830", "vendor": "globalindustrial", "min_qty": 1, "pdp_url": "https://www.globalindustrial.com/p/bc30t2-30-inch-t-square-fence-and-rail-system", "zipcode": "85132-6130"}
# 
#     print(json.dumps(globalindustrial(url=event['pdp_url'], sku=event['sku'],zipcode=event['zipcode'],min_qty=event['min_qty'])))