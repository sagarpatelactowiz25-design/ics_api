import json
import requests
from parsel import Selector

def reidsupply(url, sku, vendor='reidsupply'):

    try:
        cookies = {
            '01_userCurrency': 'USD',
            '01_visitorNewReturning': '1713254551459',
            'ECOM_JSESSIONID_01': 'FF595422C4CC271CF6689F144505E660',
            'OptanonAlertBoxClosed': '2024-04-15T08:03:42.345Z',
            '_gcl_au': '1.1.647555996.1713168222',
            '_ga': 'GA1.1.1946421427.1713168214',
            'ECOM_JSESSIONID_GB': '196897C69179D693282F0D6632F35A3F',
            'GB_userCurrency': 'GBP',
            'GB_sessionTimeoutInfo': '1713168283781-889032704',
            '01_continueShoppingPage': '/p/drills/1013645',
            '01_lastPage': '/p/drills/1013645',
            'OptanonConsent': 'isIABGlobal=false&datestamp=Mon+Apr+15+2024+13%3A46%3A09+GMT%2B0530+(India+Standard+Time)&version=6.17.0&hosts=&consentId=943785b6-78a5-4ee2-bf12-a57ee6e5f020&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=IN%3BGJ',
            '_hjSessionUser_2413596': 'eyJpZCI6IjM2ZDc1ZWI5LWViZTktNTJhMy1iYmYyLWM0NjJmMjE2NTJhYSIsImNyZWF0ZWQiOjE3MTMxNjg5NjkzMDIsImV4aXN0aW5nIjpmYWxzZX0=',
            '_hjSession_2413596': 'eyJpZCI6IjU0ODVjNGMxLTk0MDYtNDZjYi1hM2RjLTJlNWZjM2I0NmJlNCIsImMiOjE3MTMxNjg5NjkzMDQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
            'CMS_JSESSIONID': 'A32CADCFEC658B73A84E3307C310BA11',
            '01_sessionTimeoutInfo': '1713168972876-889032704',
            '_ga_VK2L32C073': 'GS1.1.1713168213.1.1.1713169018.10.0.0',
            'ABTasty': 'uid=18xnsxtmc19ynmbf&fst=1713168148913&pst=-1&cst=1713168148913&ns=1&pvt=3&pvis=3&th=',
            'ABTastySession': 'mrasn=&lp=https%253A%252F%252Fwww.reidsupply.com%252Fen-us',
            'RT': '"z=1&dm=reidsupply.com&si=ed12whjqfsn&ss=lv0o2z22&sl=0&tt=0"',
        }

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '01_userCurrency=USD; 01_visitorNewReturning=1713254551459; ECOM_JSESSIONID_01=FF595422C4CC271CF6689F144505E660; OptanonAlertBoxClosed=2024-04-15T08:03:42.345Z; _gcl_au=1.1.647555996.1713168222; _ga=GA1.1.1946421427.1713168214; ECOM_JSESSIONID_GB=196897C69179D693282F0D6632F35A3F; GB_userCurrency=GBP; GB_sessionTimeoutInfo=1713168283781-889032704; 01_continueShoppingPage=/p/drills/1013645; 01_lastPage=/p/drills/1013645; OptanonConsent=isIABGlobal=false&datestamp=Mon+Apr+15+2024+13%3A46%3A09+GMT%2B0530+(India+Standard+Time)&version=6.17.0&hosts=&consentId=943785b6-78a5-4ee2-bf12-a57ee6e5f020&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=IN%3BGJ; _hjSessionUser_2413596=eyJpZCI6IjM2ZDc1ZWI5LWViZTktNTJhMy1iYmYyLWM0NjJmMjE2NTJhYSIsImNyZWF0ZWQiOjE3MTMxNjg5NjkzMDIsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_2413596=eyJpZCI6IjU0ODVjNGMxLTk0MDYtNDZjYi1hM2RjLTJlNWZjM2I0NmJlNCIsImMiOjE3MTMxNjg5NjkzMDQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; CMS_JSESSIONID=A32CADCFEC658B73A84E3307C310BA11; 01_sessionTimeoutInfo=1713168972876-889032704; _ga_VK2L32C073=GS1.1.1713168213.1.1.1713169018.10.0.0; ABTasty=uid=18xnsxtmc19ynmbf&fst=1713168148913&pst=-1&cst=1713168148913&ns=1&pvt=3&pvis=3&th=; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.reidsupply.com%252Fen-us; RT="z=1&dm=reidsupply.com&si=ed12whjqfsn&ss=lv0o2z22&sl=0&tt=0"',
            'origin': 'https://www.reidsupply.com',
            'referer': 'https://www.reidsupply.com/en-us/p/drills/1013645',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        url_request = str()
        error = dict()
        try:
            max_retires = 5
            for i in range(max_retires):
                url_request = requests.get(url=url)
                if url_request.status_code == 200:
                    break
                elif url_request.status_code == 404:
                    error['statusCode'] = 410
                    error['error_message'] = 'Product not found'
                    return error
                else:
                    # The function must have logic for retries Max. 5
                    # If request fails after 5 retries it should return following
                    return {'statusCode': 408,
                            'error_message': 'Request timeout, failed to reach host'}
        except Exception as e:
            print(e)

        if '<span>Item code</span>' not in url_request.text:
            error['statusCode'] = 410
            error['error_message'] = 'Product not found'
            return error

        # pass response to Selector :-
        response = Selector(url_request.text)

        # define dictionary for making data dictionary :-
        item = dict()

        # vendor Extracting :-
        item['vendor'] = vendor

        # sku Extracting :-
        try:
            ld_json_data = None
            for ld_json in response.xpath('//script[@type="application/ld+json"]//text()').getall():
                tmp = json.loads(ld_json)
                if tmp['@type'] == "Product":
                    ld_json_data = tmp
                    break
            item['sku'] = ld_json_data['sku']

            if item['sku'] != sku:
                error['statusCode'] = 410
                error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
                return error
            else:
                pass
        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = str(e)
            return error

        # url Extracting :-
        item['pdp_url'] = url

        # Price Extracting :-
        url_req = url.split('https://www.reidsupply.com/')[-1]
        data = {
            'skuIds': '',
            'url': f'{url_req}',
        }

        response_req = requests.post('https://www.reidsupply.com/en-us/component/user-context',
                                 cookies=cookies,
                                 headers=headers,
                                 data=data)

        response_data = Selector(response_req.text)

        item_price = dict()
        price_list = list()
        try:
            sku_qty = int(response.xpath('//input[@name="standardPackQuantity"]/@value').get(1))
        except:
            sku_qty = 1
        if sku_qty:
            sku_qty = sku_qty
        else:
            sku_qty = 1

        pricing_tier = response_data.xpath('//script[contains(text(), "PriceDataTier")]//text()').get()
        qty = response.xpath('//td[@class="cell-center"]/b[1]/text()').get()
        if pricing_tier:
            pricing_dict = dict()
            pricing_json = json.loads(pricing_tier.split("overrideSkuPriceDataTier")[-1][1:-1].split(';var')[0])

            for pricing_key in pricing_json:
                for pricing in pricing_json[pricing_key]:
                    if len(pricing_json[pricing_key]) > 1:
                        if sku_qty == 1:
                            original_price = dict(item_price)
                            original_price['min_qty'] = pricing['minQuantity']
                            price = pricing['salePrice'].replace('$', '').replace(',', '').strip()
                            original_price['price'] = round(float(price), 2)
                            # price = round(float(v) * sku_qty, 2)
                            original_price['currency'] = 'USD'
                            price_list.append(original_price)
                            continue
                        else:
                            original_price = dict(item_price)
                            original_price['min_qty'] = pricing['minQuantity']
                            price = pricing['salePrice'].replace('$', '').replace(',', '').strip()
                            original_price['price'] = round(float(price), 2)
                            original_price['currency'] = 'USD'
                            price_list.append(original_price)
                            continue
                    elif len(pricing_json[pricing_key]) == 1:
                        original_price = dict(item_price)
                        original_price['min_qty'] = sku_qty
                        price = pricing['salePrice'].replace('$', '').replace(',', '').strip()
                        price1 = round(sku_qty * float(price), 2)
                        original_price['price'] = price1
                        original_price['currency'] = 'USD'
                        price_list.append(original_price)
                    else:
                        original_price = dict(item_price)
                        original_price['min_qty'] = sku_qty
                        price = response.xpath('//span[@id="salePrice"]/text()').get().replace('$', '').strip()
                        price1 = round(sku_qty * float(price), 2)
                        original_price['price'] = price1
                        original_price['currency'] = 'USD'
                        price_list.append(original_price)
            # if pricing_dict:
            #     for k, v in pricing_dict.items():
            #         original_price = dict(item_price)
            #         original_price['currency'] = 'USD'
            #         original_price['min_qty'] = int(k)
            #         v = str(v).replace('$', '').replace(',', '').strip()
            #         price = round(float(v) * sku_qty, 2)
            #         price = str(price).replace('$', '').replace(',', '').strip()
            #         original_price['price'] = float(price)
            #         price_list.append(original_price)
            if not pricing_dict and not pricing_json:
                original_price = dict(item_price)
                original_price['price_string'] = "Call For Price"
                try:
                    original_price['min_qty'] = int(response.xpath('''//div[@class="text-left labels-qty"]/span[contains(text(), 'Standard')]/following-sibling::span/text()''').get())
                except:
                    original_price['min_qty'] = 1
                price_list.append(original_price)
        elif qty:
            original_price = dict(item_price)
            original_price['currency'] = 'USD'
            qty = response.xpath('//td[@class="cell-center"]/b[1]/text()').get()
            qty = qty.replace('+', '').strip()
            price = response.xpath('//td[@class="cell-center"]/span/text()').get()
            price = price.replace('$', '').strip()
            original_price['min_qty'] = int(qty)
            original_price['price'] = round(float(price.replace('$', '').replace(',', '')), 2)
            price_list.append(original_price)
        else:
            original_price = dict(item_price)
            original_price['price_string'] = "Call For Price"
            original_price['min_qty'] = 1
            price_list.append(original_price)

        item['price'] = price_list

        # available_to_checkout Extracting :-

        in_stock = response.xpath('//div[@class="prod-meta"]//strong[contains(text(),"In stock")]/text()').getall()
        in_stock = (True if in_stock else False)
        available_to_checkout = response.xpath('//a[@class="btn btn-cta tealium-addToCart js-addToCart ShoppingCart"]/@disabled').get()
        if available_to_checkout == 'disabled':
            available_to_checkout = False
        elif available_to_checkout == None:
            available_to_checkout = False
        else:
            available_to_checkout = True

        if in_stock == True and available_to_checkout == False:
            try:
                in_stock = int(response_req.text.split('overrideSkuStock')[-1].split('};')[0].split(':')[-1])
            except:
                in_stock = 1
            if in_stock == 0:
                in_stock = False
                available_to_checkout = False
            else:
                in_stock = True
                available_to_checkout = True
        elif in_stock == False and available_to_checkout == False:
            if 'var overrideSkuPriceDataTier={};' not in response_req.text:
                in_stock = response_req.text.split('overrideSkuStock')[-1].split('};')[0].split(':')[-1]
                if in_stock == '0':
                    in_stock = False
                    if 'var overrideSkuPriceDataTier = {};' in response_req.text:
                        available_to_checkout = False
                    else:
                        available_to_checkout = True
                else:
                    in_stock = True
                    available_to_checkout = True
            elif in_stock == False and available_to_checkout == False and original_price['price_string'] == 'Call For Price':
                in_stock = False
                available_to_checkout = False

        item['in_stock'] = in_stock
        item['available_to_checkout'] = available_to_checkout

        item['lead_time'] = None

        # return json output :-
        # The function should return a dictionary having statusCode: 200;
        # If all above given headers are scraped properly
        return {"statusCode": 200,
                "data": item}

    except Exception as e:
        # The function should return a dictionary having statusCode: 500;
        # If any internal error occurs. i.e If any Exception is caught inside try-except.
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}


if __name__ == '__main__':
    # url = "https://www.reidsupply.com/en-us/p/abrasive-belts/arcab-70323"
    # sku = "ARCAB-70323"
    event={"sku": "SHS-250", "vendor": "reidsupply", "pdp_url": "https://www.reidsupply.com/en-us/p/machine-tool-sleeves/shs-250"}
    url = event['pdp_url']
    sku = event['sku']
    print(json.dumps(reidsupply(url, sku, vendor='reidsupply')))
