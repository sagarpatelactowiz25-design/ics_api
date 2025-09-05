import json# install json
import requests# intall requests
from parsel import Selector # intsall parsel




max_retires = 5
#scraper api key
scraper_key = 'de51e4aafe704395654a32ba0a14494d'
cookies_stock = {
    'SLIData': '0',
    '.WLSS': 'gmmjkmvaisppo3klceipimne',
    '.WLP': '188ee2c4-a408-4630-b700-cba0622a4074',
    '.WLUD': 'eyJsaSI6ZmFsc2UsImFuIjpudWxsLCJmbiI6bnVsbCwidXQiOjAsImNpIjowLCJzYyI6MH0=',
    'SLI_Detail': 'LoggedIn=0&ThomasDomain=www.thomassci.com&CartItemCount=0',
    'ltkpopup-session-depth': '1-2',
    'TRUSR': '0',
    '_gid': 'GA1.2.1192204850.1715943087',
    'ltkpopup-suppression-7e812675-8563-4a95-811e-09486b970474': '1',
    '.WLCC': '1.638515254907713651',
    '_gcl_au': '1.1.2040139439.1715943092',
    '_uetsid': '6c887e00143b11ef93d9eb063d7f5fac',
    '_uetvid': '6c88a2f0143b11ef8802455a75a459d9',
    '_fbp': 'fb.1.1715943092956.359636787',
    '_ga': 'GA1.1.40313632.1715943087',
    '_ga_67DSTZ6EQH': 'GS1.1.1715942643.3.1.1715943138.0.0.0',
}

headers_stock = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'SLIData=0; .WLSS=gmmjkmvaisppo3klceipimne; .WLP=188ee2c4-a408-4630-b700-cba0622a4074; .WLUD=eyJsaSI6ZmFsc2UsImFuIjpudWxsLCJmbiI6bnVsbCwidXQiOjAsImNpIjowLCJzYyI6MH0=; SLI_Detail=LoggedIn=0&ThomasDomain=www.thomassci.com&CartItemCount=0; ltkpopup-session-depth=1-2; TRUSR=0; _gid=GA1.2.1192204850.1715943087; ltkpopup-suppression-7e812675-8563-4a95-811e-09486b970474=1; .WLCC=1.638515254907713651; _gcl_au=1.1.2040139439.1715943092; _uetsid=6c887e00143b11ef93d9eb063d7f5fac; _uetvid=6c88a2f0143b11ef8802455a75a459d9; _fbp=fb.1.1715943092956.359636787; _ga=GA1.1.40313632.1715943087; _ga_67DSTZ6EQH=GS1.1.1715942643.3.1.1715943138.0.0.0',
    'Referer': 'https://www.thomassci.com/Laboratory-Supplies/Tapes/_/Polyethylene-Super-Tack',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

cookies = {
    'SLIData': '0',
    '.WLP': '000e7ae4-ed30-4bac-8e7a-3f95eec0ef97',
    'TRUSR': '0',
    '.WLCC': '1.638472111116606889',
    '_gcl_au': '1.1.1945506051.1711628726',
    '_uetvid': '41dde2e0ecfe11eebb896982ed2975a5',
    '_fbp': 'fb.1.1711628726715.206126964',
    '__mmapiwsid': '018e8505-c6a2-7a95-aecc-b5942a7915a2:61d1ff0cf01f024a6b8506e246b5859c70b6840d',
    'SLI_Detail': 'LoggedIn=0&ThomasDomain=www.thomassci.com&CartItemCount=0',
    'ltkpopup-suppression-7e812675-8563-4a95-811e-09486b970474': '1',
    '.WLSS': 'w3nn53thmnujttkjbevilxem',
    '.WLUD': 'eyJsaSI6ZmFsc2UsImFuIjpudWxsLCJmbiI6bnVsbCwidXQiOjAsImNpIjowLCJzYyI6MH0=',
    'ltkpopup-session-depth': '1-2',
    '_gid': 'GA1.2.1460698183.1713179388',
    '_ga': 'GA1.1.994427513.1711628720',
    '_ga_67DSTZ6EQH': 'GS1.1.1713179387.35.1.1713180475.0.0.0',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'SLIData=0; .WLP=000e7ae4-ed30-4bac-8e7a-3f95eec0ef97; TRUSR=0; .WLCC=1.638472111116606889; _gcl_au=1.1.1945506051.1711628726; _uetvid=41dde2e0ecfe11eebb896982ed2975a5; _fbp=fb.1.1711628726715.206126964; __mmapiwsid=018e8505-c6a2-7a95-aecc-b5942a7915a2:61d1ff0cf01f024a6b8506e246b5859c70b6840d; SLI_Detail=LoggedIn=0&ThomasDomain=www.thomassci.com&CartItemCount=0; ltkpopup-suppression-7e812675-8563-4a95-811e-09486b970474=1; .WLSS=w3nn53thmnujttkjbevilxem; .WLUD=eyJsaSI6ZmFsc2UsImFuIjpudWxsLCJmbiI6bnVsbCwidXQiOjAsImNpIjowLCJzYyI6MH0=; ltkpopup-session-depth=1-2; _gid=GA1.2.1460698183.1713179388; _ga=GA1.1.994427513.1711628720; _ga_67DSTZ6EQH=GS1.1.1713179387.35.1.1713180475.0.0.0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
def thomasscientific(pdp_url,product_sku):

    error_dict = {}


    proxies = {
        'http': f'http://scraperapi.keep_headers=true:{scraper_key}@proxy-server.scraperapi.com:8001',
        # 'https': f'https://scraperapi.keep_headers=true:{scraper_key}@proxy-server.scraperapi.com:8000'
    }
    for i in range(max_retires):

        response_data = requests.get(url=pdp_url,cookies=cookies,headers=headers,proxies=proxies, timeout=10)
        # response_data = requests.get(url=f"http://api.scraperapi.com/?api_key={scraper_key}&url="+pdp_url,
        #                              cookies=cookies,
        #                              headers=headers
        #                              )
        if response_data.status_code == 200:
            break
            print("200")
        elif response_data.status_code == 404:
            error_dict['statusCode'] = 404
            error_dict['error_message'] = str("404 Page not found")
            return error_dict
    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}

    if response_data.status_code == 200 and 'itemprop="productID"' in response_data.text:

        response = Selector(text=response_data.text)
        # in pl page multiple sku and price. So every sku and price enter new colum. now this loop for multiples entry
        price_list =[]
        final_lead_time_list =[]
        sku_check = []
        for product_detail in response.xpath('//div[@class="detail-block__wrap"]/div'):
            product_sku_scrape = product_detail.xpath('.//dd[@itemprop="productID"]/text()').get()
            # print("product_sku_scrape",time.time() - t1)

            if product_sku == product_sku_scrape:
                # print("product_sku_scrape in..", time.time() - t1)
                sku_check.append(product_sku)

                count = 0
                data_json = product_detail.xpath('.//div[@class="property-group"]/@data-product-data').get()

                stock_list_check =[]
                for product_price_qty in product_detail.xpath('.//*[@class="prices"]'):

                    # product price
                    price_data = product_price_qty.xpath('.//*[@itemprop="price"]/text()').get('').replace(",", "")
                    # product Quantity
                    min_qty_data = product_price_qty.xpath('.//span[@class="prices__quantity"]/text()').get()

                    if price_data:
                        price_list.append({"min_qty": int(min_qty_data), "price": float(price_data), "currency": "USD"})
                    else:
                        price_list = [{"min_qty": 1, "price_string": "Call For Price"}]

                    if "Call For Price" in str(price_list):
                        final_lead_time_list = None
                        in_stock = False
                        available_to_checkout = False
                    else:

                        # uom_final = product_price_qty.xpath('.//span[@class="prices__measurement"]//text()').get()

                        # new Request for available
                        if data_json:
                            data_dict = json.loads(data_json)
                            SecondaryUnitOfMeasureName = data_dict["SecondaryUnitOfMeasureName"]
                            if not SecondaryUnitOfMeasureName:
                                SecondaryUnitOfMeasureName = ''

                            # AvailablePurchaseInventory = data_dict["AvailablePurchaseInventory"]
                            # if not AvailablePurchaseInventory:
                            #     AvailablePurchaseInventory = ''
                            SecondaryUnitOfMeasure = data_dict["SecondaryUnitOfMeasure"]
                            if not SecondaryUnitOfMeasure:
                                SecondaryUnitOfMeasure = ''

                            count+=1


                            if count == 1:

                                params = {
                                    'TrapCode': '',
                                    'CustomerFulfillmentSystemID': '',
                                    'ProductFulfillmentSystemID': f'{data_dict["ProductFulfillmentSystemID"]}',
                                    'UnitOfMeasure': f'{data_dict["UnitOfMeasure"]}',
                                    'UnitOfMeasureName': f'{data_dict["UnitOfMeasureName"]}',
                                    'SecondaryUnitOfMeasure': f'{SecondaryUnitOfMeasure}',
                                    'SecondaryUnitOfMeasureName': f'{SecondaryUnitOfMeasureName}',
                                    'DropShip': f'{data_dict["DropShip"]}',
                                    'Quantity': '1',
                                    'SecondaryQuantity': '0',
                                }


                                # With scraper api header
                                response_data_stock = requests.get(
                                    "https://www.thomassci.com/AvailableInventory.ashx",params=params,
                                    proxies=proxies,
                                    cookies=cookies_stock,
                                    # headers=headers_stock
                                )

                            elif count == 2:
                                params_1 = {
                                    'TrapCode': '',
                                    'CustomerFulfillmentSystemID': '',
                                    'ProductFulfillmentSystemID': f'{data_dict["ProductFulfillmentSystemID"]}',
                                    'UnitOfMeasure': f'{data_dict["UnitOfMeasure"]}',
                                    'UnitOfMeasureName': f'{data_dict["UnitOfMeasureName"]}',
                                    'SecondaryUnitOfMeasure': f'{SecondaryUnitOfMeasure}',
                                    'SecondaryUnitOfMeasureName': f'{SecondaryUnitOfMeasureName}',
                                    'DropShip': f'{data_dict["DropShip"]}',
                                    'Quantity': '0',
                                    'SecondaryQuantity': '1',
                                }

                                # With scraper api header
                                response_data_stock = requests.get("https://www.thomassci.com/AvailableInventory.ashx",
                                    params = params_1,
                                    proxies = proxies,
                                    cookies = cookies_stock,
                                    # headers = headers_stock,
                                )
                            try:
                                if response_data_stock.status_code==200 :

                                    data_dict = json.loads(response_data_stock.text)
                                    try:

                                        Available = " ".join(data_dict[0]['Availability'])

                                        if "in stock" in Available.lower():
                                            in_stock = True
                                            available_to_checkout = True
                                            stock_list_check.append(True)
                                        else:
                                            in_stock = False
                                            available_to_checkout = False

                                        try:
                                            # make ETA as requirement
                                            if "approximately " in Available:
                                                estimated_lead_time = {
                                                        "min_qty": 1,
                                                        "time_to_ship": {"raw_value": f"{Available}"}
                                                    }

                                                final_lead_time_list.append(estimated_lead_time)
                                            else:
                                                estimated_lead_time = None
                                        except:
                                            estimated_lead_time = None

                                    except Exception as e:
                                        pass
                                else:
                                    available_to_checkout=False
                                    in_stock = False
                                    final_lead_time_list = None
                            except Exception as e:
                                print(e)
                    # break

                else:
                    pass


        # print("insert", time.time() - t1)
        # Data insert
        if not sku_check:
            try:
                error_dict['statusCode'] = 404
                error_dict['error_message'] = f"Scraped SKU does not match input SKU:{product_sku}"
                return error_dict
            except Exception as e:
                error_dict['statusCode'] = 500
                error_dict['error_message'] = str(e)
                return error_dict
        else:
            item = {}
            if stock_list_check:
                in_stock = True
                available_to_checkout = True
            item['vendor'] = "thomasscientific"
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
        error_dict['statusCode'] = 404
        error_dict['error_message'] = str("404 Page not found")
        return error_dict


