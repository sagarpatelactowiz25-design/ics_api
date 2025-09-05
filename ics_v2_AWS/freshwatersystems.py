import json
import re
from datetime import datetime
import requests
from parsel import Selector


max_retires = 5

def data_json(slug):
    url = "https://www.freshwatersystems.com/api/2023-07/graphql.json"
    json_data = {
        'query': f'\n          query {{\n            product(handle: "{slug}") {{\n              id\n              title\n              handle\n              totalInventory\n              availableForSale\n              tags\n              vendor\n              featuredImage {{ \n                url\n                altText\n              }}\n              media(first: 20) {{\n                edges {{\n                  node {{\n                    ... on MediaImage {{\n                      image {{\n                        url\n                        altText\n                      }}\n                    }}\n                    mediaContentType\n                    previewImage {{\n                      url\n                      altText\n                    }}\n                    ... on ExternalVideo {{\n                      embedUrl\n                    }}\n                  }}\n                }}\n              }}\n              variants(first: 100) {{\n                edges {{\n                  node {{\n                    id\n                    title\n                    quantityAvailable\n                    availableForSale\n                    currentlyNotInStock\n                    msrp: metafield(namespace: "custom", key: "variant_msrp") {{\n                      value\n                    }}\n                    buyBoxNote: metafield(namespace: "custom", key: "variant_buy_box_note") {{\n                      value\n                    }}\n                    fullRollLength: metafield(namespace: "custom", key: "full_roll_length") {{\n                      value\n                    }}\n                    gpItemClassCode: metafield(namespace: "custom", key: "item_class_code") {{\n                      value\n                    }}\n                    shippingGroups: metafield(namespace: "global", key: "SHIPPING_GROUPS") {{\n                      value\n                    }}\n                    estimatedShipDate: metafield(namespace: "inventory", key: "estimated_ship_date") {{\n                      value\n                    }}\n                    sku\n                    price {{ amount }}\n                    compareAtPrice {{ amount }}\n                    availabilityOverride: metafield(namespace: "inventory", key: "availablility_override") {{\n                      value\n                    }}\n                    specifications: metafield(namespace: "custom", key :"product_specifications") {{\n                      value\n                    }}\n                    shippingGroups: metafield(namespace: "global", key: "SHIPPING_GROUPS") {{\n                      value\n                    }}\n                    showMAP: metafield(namespace: "products", key: "show_map_price") {{\n                      value\n                    }},\n                    MAP: metafield(namespace: "products", key: "map_price") {{\n                      value\n                    }}\n                  }}\n                }}\n              }}\n              descriptionHtml\n              compatibilityTable: metafield(namespace: "products", key: "compatible") {{\n                value\n              }}\n              prop65: metafield(namespace: "global", key: "CA_prop_65") {{\n                value\n              }}\n              quoteFormEnabled: metafield(namespace: "custom", key: "allow_quote_request") {{\n                value\n              }}\n              quoteFormMinimum: metafield(namespace: "custom", key: "minimum_quote_request_quantity") {{\n                value\n              }}\n              callToOrder: metafield(namespace: "global", key: "call_to_order") {{\n                value\n              }}\n              similarItems: metafield(namespace: "parts_arrays", key: "similar_items") {{\n                value\n              }}\n              showBuyButton: metafield(namespace: "global", key: "show_buy_button") {{\n                value\n              }}\n              reviewAverage: metafield(namespace: "reviews", key: "rating") {{\n                value\n              }}\n              reviewCount: metafield(namespace: "reviews", key: "rating_count") {{\n                value\n              }}\n              sellingPlanGroups(first: 5) {{\n                edges {{\n                  node {{\n                    appName\n                    name\n                    options {{\n                      values\n                    }}\n                    sellingPlans(first: 5) {{\n                      edges {{\n                        node {{\n                          id\n                          name\n                        }}\n                      }}\n                    }}\n                  }}\n                }}\n              }}\n            }}\n          }}',
    }
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        # 'cookie': 'secure_customer_sig=; cart_currency=USD; _tracking_consent=%7B%22lim%22%3A%5B%22CMP%22%5D%2C%22region%22%3A%22INGJ%22%2C%22v%22%3A%222.1%22%2C%22reg%22%3A%22%22%2C%22con%22%3A%7B%22CMP%22%3A%7B%22p%22%3A%22%22%2C%22s%22%3A%22%22%2C%22m%22%3A%22%22%2C%22a%22%3A%22%22%7D%7D%7D; _shopify_y=2fef8de3-ce7c-4006-b04d-08fe5272ed88; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX1%2Br8GDQU%2Fm9EaTqiJ3eDkutabVvjfg6Ko4%3D; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX19ekbANaSA0nY6vjSFH%2BEeM%2ByzqpglCazo%3D; _gcl_au=1.1.1226934420.1708945892; _fbp=fb.1.1708945891731.1996794150; _pin_unauth=dWlkPU9UVmxPVGt6WVdFdE1UWmhOQzAwTXpRMExXSmlaall0WTJFelltTXhOMk0zWW1FNA; _shg_user_id=c84174b3-6aa7-4c36-b7f2-ec405d299209; zHello=1; cart=4f2b0cd333587002c6bb3e355f42a097; localization=IN; _hjSessionUser_1664567=eyJpZCI6IjFmOTdlODRlLWVlMjAtNWQxZC1iNDA4LWVjNmRmYzc3MzY2YiIsImNyZWF0ZWQiOjE3MDkyNjc3MDk1NjYsImV4aXN0aW5nIjp0cnVlfQ==; _uetvid=cbc8a780d49711ee8d5dc7ffcdbcd439; _secure_session_id=ef85d461a76abdf0414de906a4b37bd0; checkout_session_token__co__900cc7822ad9d4a32f5f0ac86cb59333=%7B%22token%22%3A%22OG9QSWcrd3d2aFFUYkM3Q0J4Yis0VngyY2paN3JzOE9Nc3BEbk9DcmF1eVd5UkNOL2VLR1ZOZkdsb1J5Wjg0bnVPdWt6UmJhZHp3bXV1NEl2UklVWEdBTnZsMDdWVG04Z1VPdTJOdzlidVppcG12clVzMWVMOUxEcVhwUmtlT2pqdGluY0gvY3hySnVQT3lRSDdVSmdLSVdiN0JTSXF1c2hyZ3hPU0dEUVlnZmJuSzJKSXhtVHBGd3RxV044Ris0dU1vMysxanpwbDhHYXpXdSs4MzdKV05IM01WMGZKRUgwVUxsbHZTRHlDdHV3OU0yekoweFoyUTFMZitOS09NM3BCdTAtLTQvSVpPaTZPR3hpS25Zd3EtLWYzSVVuOXBuL2x1K0kvN1JHVHE0VFE9PQ%22%2C%22locale%22%3A%22en-IN%22%2C%22permanent_domain%22%3A%22fwsco.myshopify.com%22%2C%22checkout_session_identifier%22%3A%22900cc7822ad9d4a32f5f0ac86cb59333%22%7D; checkout_session_lookup=%7B%22version%22%3A1%2C%22keys%22%3A%5B%7B%22source_id%22%3A%22900cc7822ad9d4a32f5f0ac86cb59333%22%2C%22checkout_session_identifier%22%3A%22900cc7822ad9d4a32f5f0ac86cb59333%22%2C%22source_type_abbrev%22%3A%22co%22%2C%22updated_at%22%3A%222024-03-19T10%3A56%3A43.217Z%22%7D%5D%7D; _ga_48Y3NSLS75=GS1.1.1710845770.1.1.1710845792.38.0.0; _orig_referrer=; _landing_page=%2Fproducts%2Fstow-n-flow-greenfeeder-5-gal-in-ground-feeder-system%3Fvariant%3D42300410233016; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D; receive-cookie-deprecation=1; _gid=GA1.2.959157920.1712303985; yotpo_pixel=ef034948-fd3e-4344-8696-99c7b4d1202c; _sp_ses.c890=*; br-uid=uid-lumdl0xo-2qwdq3d5w; __brLastSetCartToken=4f2b0cd333587002c6bb3e355f42a097; locale_bar_accepted=1; cart_sig=5283edc86185d2c62d3d79b1305156e6; cart_ts=1712305307; __brTagsSet=add to cart, add to cart, add to cart, add to cart, add to cart, add to cart; cto_bundle=6y9Fa19ZdWdrczElMkZGMWxsak5SMTBoclBvRXJpSkFncDNXQ2p1Vlg5djh5JTJGeWNVbWc0OXJ1QVEzcTZaVWJvRG5qc3IwYXBYRXpvR1lBNUQzZjRpaUlpYVR3c21reEZ3bTVKU1RJYTRBalp6bUluRm9nZFc1NDRDOGFQJTJGMm9kdWNWS2lid3RzMVElMkY5Y3I1dHFyUSUyRjFpTzF1bkZua1U3d1hlMm93NHFuJTJGbUVodzc0blh5UVFPR2hWdzZyV05OWmJxOTBzOTZIV3h2UVQwWlVwc0VScjc4QWpoVm9MTWNpb0ZKWDhaRXoxZ2xMa0F2RU9oQlEyWDN0NnMxQ0RoNCUyQkNpTkxoREc2QUMyMFJReCUyQlF4V3MyU2p1Rk9KSWclM0QlM0Q; _uetsid=77b0ae70f32211eeb2ef8f06c95439a1; zCountry=IN; _shopify_essential=:AY5WWvt4AAH_VLVx3GK6Dv2654-CgrP2oOMXotKOWpiRabzul4uxwl9E-gVi3TgYSGh4dhSmpZRufStFIiCXxjc2DzfZ9JVrGrsJTXmJjjDDjzXNapuarVMrsgWAhZzcWn7oL6CJtnwENtgKYjwtbvVtF8IrjriiFOc-yA==:; _sp_id.c890=35782d8354690b6f.1708945894.33.1712308123.1712153308; keep_alive=ab1157ae-5c68-416d-9ad5-1181f5083548; _ga_N6ZMPQ442S=GS1.1.1712308131.42.0.1712308131.60.0.0; _shopify_s=cc997164-87cd-4831-ab6e-55fd5c1dc8a9; _shopify_sa_t=2024-04-05T09%3A08%3A51.950Z; _shopify_sa_p=; _ga=GA1.2.1984668175.1708945892; _gat=1; rl_user_id=RudderEncrypt%3AU2FsdGVkX181u7MZXL6603l1nmO%2FrtaU4ymBbQ6Lbv8%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX18sBoo3bSNqntmU3rboyNXnnMWhAjpAPYE%3D; rl_group_id=RudderEncrypt%3AU2FsdGVkX18%2FOFjIoKokBfCcsELyecrl0RZcs%2FaTJSc%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2BTijevrNbV3BKJ22N0YYd%2B1%2FVa25%2B%2FTaE%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX1%2Bpxi2xvKx1fSrmwNwOls2CXq%2BJWoLIP%2BW28t2GYFlWY8Qcv%2F6EsifN5gQUmCnLF1PZilhJPlgw5w%3D%3D; __kla_id=eyJjaWQiOiJZbVUyTURKbFpXSXROR0ZoT0MwMFlUSTFMV0ppTURJdE5UbGxNek0yTWpSaVptWXgiLCIkcmVmZXJyZXIiOnsidHMiOjE3MDg5NDU4OTIsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vd3d3LmZyZXNod2F0ZXJzeXN0ZW1zLmNvbS9wcm9kdWN0cy9wcm8tZmlsdGVyLW1hdGUtc2FuaXdlbGwtc2FuaXRpemVyP3ZhcmlhbnQ9MTcyMDgwMjM2NzkwMTkifSwiJGxhc3RfcmVmZXJyZXIiOnsidHMiOjE3MTIzMDgxMzMsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vd3d3LmZyZXNod2F0ZXJzeXN0ZW1zLmNvbS9wcm9kdWN0cy9uZW8tcHVyZS1oZGZiLXBwLW1sLTIyNS1zcy1oaWdoLWRlbnNpdHktMi1wb2x5cHJvcHlsZW5lLWJhZy1maWx0ZXItc3RhaW5sZXNzLXN0ZWVsLXJpbmctMjUtbWljcm9uP3ZhcmlhbnQ9NDE5OTQ1NjgwMDc4NjQifX0=',
        'origin': 'https://www.freshwatersystems.com',
        'referer': 'https://www.freshwatersystems.com/products/neo-pure-hdfb-pp-ml-225-ss-high-density-2-polypropylene-bag-filter-stainless-steel-ring-25-micron?variant=41994568007864',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-shopify-storefront-access-token': 'b69b04f0a1647c283cb243b41593db26',
    }
    for i in range(max_retires):
        # requests to get json :-
        response = requests.request("POST", url,
                                    headers=headers,
                                    json=json_data)
        if response.status_code == 200:
            # json load for estimated lead time extracting :-
            data = response.text
            # return dictionary :-
            return data


def freshwatersystems(pdp_url,sku):
    error_ = dict()
    url_request = str()
    max_retires = 5
    for i in range(max_retires):
        url_request = requests.get(url=pdp_url)
        if url_request.status_code == 200:
            break
    if url_request.status_code == 200:
        pass
    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}

    if 'class="link underline text-xl"' not in url_request.text:
        error_['statusCode'] = 410
        error_['error_message'] = 'Product not found'
        return error_
    else:
        slug_id = pdp_url.split('?')[0].split('/')[-1]
        data = data_json(slug=slug_id)
        data_load = json.loads(data)
        discontinued = data_load['data']['product']['callToOrder']
        product_id = pdp_url.split('=')[-1]
        if not discontinued:
            item = dict()
            item['vendor'] = 'freshwatersystems'
            for index,data_row in enumerate(data_load['data']['product']['variants']['edges']):
                    var_id = data_row['node']['sku']
                    try:
                        if sku == var_id:
                            try:
                                item['sku'] = data_row['node']['sku']
                                if item['sku'] != sku:
                                    error_['statusCode'] = 410
                                    error_['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
                                    return error_
                            except Exception as e:
                                error_['statusCode'] = 410
                                error_['error_message'] = str(e)
                                return error_

                            item['pdp_url'] = pdp_url

                            instock = data_row['node']['currentlyNotInStock']
                            quantityAvailable = data_row['node']['quantityAvailable']
                            if instock == True:
                                if quantityAvailable == 0:
                                    item_price = dict()
                                    price_ = data_load['data']['product']['variants']['edges'][index]['node']['price']['amount']
                                    item_price['currency'] = 'USD'
                                    item_price['min_qty'] = 1
                                    try:
                                        if not price_:
                                            if price_:
                                                item_price['price_string'] = None
                                            else:
                                                item_price['price_string'] = "Call for price"
                                        else:
                                            item_price['price'] = float(price_)
                                    except:
                                        pass
                                    price_list = list()
                                    price_list.append(item_price)
                                    item['price'] = price_list
                                    item['in_stock'] = True
                                    item['available_to_checkout']= True
                                else:
                                    price_list = list()
                                    item_price = dict()
                                    item_price['min_qty'] = 1
                                    item_price['price_string'] = "Call for price"
                                    price_list.append(item_price)
                                    item['price'] = price_list

                            elif instock == False:
                                if quantityAvailable == 0:
                                    item_price = dict()
                                    price_ = data_load['data']['product']['variants']['edges'][index]['node']['price'][
                                        'amount']
                                    item_price['currency'] = 'USD'
                                    item_price['min_qty'] = 1
                                    try:
                                        if not price_:
                                            if price_:
                                                item_price['price_string'] = None
                                            else:
                                                item_price['price_string'] = "Call For Price"
                                        else:
                                            item_price['price'] = float(price_)
                                    except:
                                        pass
                                    price_list = list()
                                    price_list.append(item_price)
                                    item['price'] = price_list
                                    item['in_stock']= False
                                    item['available_to_checkout']= False
                                else:
                                    item_price = dict()
                                    price_ = data_load['data']['product']['variants']['edges'][index]['node']['price']['amount']
                                    item_price['currency'] = 'USD'
                                    item_price['min_qty'] = 1
                                    try:
                                        if not price_:
                                            if price_:
                                                item_price['price_string'] = None
                                            else:
                                                item_price['price_string'] = "Call For Price"
                                        else:
                                            item_price['price'] = float(price_)
                                    except:
                                        pass
                                    price_list = list()
                                    price_list.append(item_price)
                                    item['price'] = price_list
                                    item['in_stock'] = True
                                    item['available_to_checkout']= True
                            try:
                                if data_row['node']['currentlyNotInStock']:
                                    leadTimeInDays_on = data_row['node']['estimatedShipDate'].get('value')
                                    date_object = datetime.strptime(leadTimeInDays_on, '%Y-%m-%d')
                                    formatted_date = date_object.strftime('%B %d, %Y')
                                    # Prepare lead time data in a specific format.
                                    leadtime_li = []
                                    leadtime_dict1 = {}
                                    leadtime_dict2 = {}
                                    leadtime_dict1['min_qty'] = 1
                                    leadtime_dict2['raw_value'] = formatted_date
                                    leadtime_dict1['time_to_ship'] = leadtime_dict2
                                    leadtime_li.append(leadtime_dict1)
                                    item['lead_time'] = leadtime_li
                                else:
                                    item['lead_time'] = None
                            except:
                                item['lead_time'] = None
                    except:
                        return {"statusCode": 410,
                                "error_message": "Product not found"}
        else:
            return {"statusCode": 410,
                    "error_message": "Product is discontinued"}
        if 'statusCode' in item.keys():
            if item['statusCode'] == 500:
                return item
            elif item['statusCode'] == 410:
                return item
        elif 'sku' not in item.keys():
            for index, data_row in enumerate(data_load['data']['product']['variants']['edges']):
                var_id = data_row['node']['id'].split('/')[-1]
                if product_id == var_id:
                    sku_live = data_row['node']['sku']
                    if sku_live!= sku:
                        error_['statusCode'] = 410
                        error_['error_message'] = f"Scraped SKU:{sku_live} does not match input SKU:{sku}"
                        return error_
            error_['statusCode'] = 410
            error_['error_message'] = f"Product not found"
            return error_
        else:
            return {'statusCode': 200,
                    'data': item}



# if __name__ == '__main__':
# #     event = {
# #   "pdp_url": "https://www.freshwatersystems.com/products/oasis-ebtech-carbon-block-10-mic?variant=13250457763883",
# #   "sku": "030696-001",
# #   "vendor": "freshwatersystems"
# # }
#     event= {"pdp_url": "https://www.freshwatersystems.com/products/60600-nsf-valved-in-line-hose-barb-coupling-body-3-8-id-barb?variant=13249792180267", "sku": "60600:10P", "vendor": "freshwatersystems"}
#     print(freshwatersystems(pdp_url=event['pdp_url'], sku=event['sku']))
    # "https://www.freshwatersystems.com/products/shelf-support-for-remote-chiller?variant=13250561146923"
    # "https://www.freshwatersystems.com/products/optipure-160-50010-fx-11-single-10-system?variant=41742666137784"
    # "https://www.freshwatersystems.com/products/hydroscientific-band-clamp-4r-30-l-2fnpt-ml-gp-304ss?variant=40878484979896"
