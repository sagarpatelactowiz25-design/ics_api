import requests
from parsel import Selector

final_list = []
def futek(url, sku, vendor='futek'):
    if "accessories" not in url:
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
                    sku1 = "".join(response.xpath("//div[contains(@class, 'row miniaturepanelm1 ng')]//div/span[@class='subproductDetailstextb1']/text()").getall()).strip()
                except:
                    sku1 = "".join(response.xpath("//div[contains(@class, 'row miniaturepanelm1 ng')]//div/span[@class='subproductDetailstextb1']/text()").getall()).strip()
                if sku1 ==sku:
                    in_stock_1 = response.xpath('//div[@class="inproductDetailscapl1"]/text()').get()
                    if in_stock_1:
                        instock = True
                    else:
                        instock = False
                    prd_sting = ''
                    price_list = []

                    prd_price = response.xpath('//span[@class="prListPricep1"]/text()').get()
                    if not prd_price:
                        prd_url = url
                        prd_url = prd_url.split('store/')[1].split('/')[0]
                        json_data = {
                            'productId': f'{sku}',
                            'custId': 0,
                            'isAdmin': False,
                            'webEnable': False,
                            'obselete': False,
                            'productClass': f'{prd_url}',
                        }
                        data = requests.post(url="https://api.futek.com/Product/GetByStockId/", json=json_data)
                        mydata = data.json()
                        product_id = mydata['Id']
                        model_id = mydata['ModelId']
                        prd_qty = []
                        prd_price = []
                        if mydata["PriceBreaks"]:
                            for i in mydata["PriceBreaks"]:
                                qrty = i["PriceBreak"]["QtyFrom"]
                                price = i["PriceBreak"]["PriceFormatted"]
                                prd_qty.append(qrty)
                                prd_price.append(price)
                            for m, n in zip(prd_qty, prd_price):
                                price_dict = {}
                                price_dict['min_qty'] = m
                                price_dict['price'] = float(n.replace("$", '').replace(',', '').strip())
                                price_dict['currency'] = "USD"
                                price_list.append(price_dict)
                                # yield price_item
                        else:
                            price_dict = {}
                            prd_qty = mydata['Quantity']
                            prd_qty = 1 if prd_qty == 0 else prd_qty
                            price_dict['min_qty'] = prd_qty
                            prd_price = mydata['Price']
                            prd_price = None if not prd_price or prd_price.replace('$','').strip() == "0.00" else prd_price.replace('.00', '').replace('$', '')
                            prd_sting = "Call For Price" if prd_price == "0" or prd_price is None else None
                            if prd_price:
                                if ',' in prd_price:
                                    prd_price = prd_price.replace(',', '')
                                price_dict['price'] =  float(prd_price)
                                price_dict['currency'] =  'USD'
                            if prd_sting:
                                price_dict['price_string'] = prd_sting
                            price_list.append(price_dict)
                    if prd_qty and prd_sting != "Call For Price":
                        available_to_checkout = True
                    else:
                        available_to_checkout= False
                    estimated_lead_time = []
                    json_data = {
                        'StockId': f'{sku}',
                        'QuantityRequested': '1',
                        'type': 'product',
                    }
                    myresponse = requests.post('https://api.futek.com/ProductLeadTime/GetLeadTime',json=json_data)
                    if myresponse.status_code == 200:
                        text = myresponse.text.split('<br/>')[0]
                        if text.strip() and 'in stock' not in text and 'For 1 item(s), please contact factory' not in text:
                            estimated = text.replace('"', '').split('in')[-1].strip()
                            # self.cursor.execute(f"update {db.product_table} set estimated_lead_time='{estimated}' where pdp_url='{url}' ")
                            # self.con.commit()
                            if estimated:
                                if instock:
                                    estimated_lead_time = [{"min_qty": 1,"time_to_ship": {"raw_value": estimated}}]
                                else:
                                    estimated_lead_time = [{"min_qty": 1,"time_to_stock": {"raw_value": estimated}}]
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
                else:
                    error['statusCode'] = 404
                    error['error_message'] = "Product not found"
                    return error
            except Exception as e:
                error['statusCode'] = 500
                error['error_message'] = "Internal server error" + str(e)
                return error
        else:
                error['statusCode'] = 408
                error['error_message'] = "Request timeout, failed to reach host"
                return error

    else:
        result = {}
        error = {}
        myurl = url.split('accessories/')[1].split('/')[0]
        try:
            StockId = url.split('accessories/')[1].split('/')[1]
        except:
            StockId = url.split('accessories/')[-1]
        json_data = {
            'CustomerId': None,
            'AccessoryName': f'{myurl}',
            'StockId': StockId,
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': 'Bearer null',
            'content-type': 'application/json',
            'origin': 'https://www.futek.com',
            'referer': 'https://www.futek.com/',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        cookies = {
            'ai_user': 'TU9Rlxfp/2wWFBxyA6L4iV|2023-03-24T07:31:18.506Z',
            'hblid': '4kiwtrK9ZcGubwxs7B1V40JoBbr6j0Aa',
            'olfsk': 'olfsk6111072831461213',
            'cookieconsent_status': 'dismiss',
            'wcsid': '7cJKZN6JIRpcM9rC7B1V40J6oajB0BA6',
            '_okdetect': '%7B%22token%22%3A%2216807719511920%22%2C%22proto%22%3A%22about%3A%22%2C%22host%22%3A%22%22%7D',
            '_okbk': 'cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1680771952228%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C',
            '_ok': '9227-663-10-1117',
            'ai_session': 'Vo0P5gNZbeSaaP52hU//l2|1680771951052|1680772841479',
            '_oklv': '1680773021209%2C7cJKZN6JIRpcM9rC7B1V40J6oajB0BA6',
        }

        try:
            mydata = requests.post(url="https://api.futek.com/Accessory/List", json=json_data, headers=headers,cookies=cookies)
        except:
            mydata = requests.post(url="https://api.futek.com/Accessory/List", json=json_data, headers=headers,cookies=cookies)

        if mydata.status_code!=200:
            for k_ in range(0,5):
                mydata = requests.post(url="https://api.futek.com/Accessory/List", json=json_data, headers=headers,cookies=cookies)
                if mydata.status_code==200:
                    break
        if mydata.status_code ==200:
            myjson = mydata.json()
            accessories_list = myjson.get('AccessoriesList', [])
            if accessories_list:
                for i in accessories_list:
                    try:
                        instock = False
                        if i['InStock']:
                            instock = True
                        productsku = i.get('ProductName', '').strip()
                        if sku == productsku:
                            price_list = []
                            price_dict = {}
                            price = str(i.get('Price')).replace('.0', '').replace(',', '')
                            price = None if price == '0' or price == '0.0' else price
                            quantity = i.get('Quantity')
                            price_dict['min_qty'] = quantity
                            if price:
                                price_dict['price'] = float(price)
                                price_dict['currency'] = "USD"
                                price_list.append(price_dict)
                            prd_sting = "Call For Price" if not price else None
                            if prd_sting:
                                price_dict['price_string'] = prd_sting
                                price_list.append(price_dict)
                            if prd_sting != "Call For Price":
                                available_to_checkout = True
                            else:
                                available_to_checkout = False

                            result['vendor'] = vendor
                            result['sku'] = sku
                            result['pdp_url'] = url
                            result['price'] = price_list
                            result['available_to_checkout'] = available_to_checkout
                            result['in_stock'] = instock
                            result['lead_time'] = None
                            return {'statusCode': 200,
                                    'data': result}
                        else:
                            error['statusCode'] = 404
                            error['error_message'] = "Product not found"
                            return error
                    except Exception as e:
                        error['statusCode'] = 500
                        error['error_message'] = "Internal server error" + str(e)
                        return error
            else:
                error['statusCode'] = 404
                error['error_message'] = "Product not found"
                return error
        else:
            error['statusCode'] = 408
            error['error_message'] = "Request timeout, failed to reach host"
            return error



