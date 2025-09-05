import json# install json
import requests# intall requests
from parsel import Selector # intsall parsel
import re
max_retires = 5

def coleparmer(pdp_url,product_sku,vendor="coleparmer"):
    url_request=''
    error={}
    cookies = {
        'liveagent_oref': '',
        'liveagent_sid': '8262c86e-4a5f-46f1-82a0-dbd16afafe90',
        'liveagent_vc': '2',
        'liveagent_ptid': '8262c86e-4a5f-46f1-82a0-dbd16afafe90',
        'SetContextLanguageCode': 'en-US',
        'locale': 'en-US',
        'SetContextCurrencyCode': 'USD',
        'SetContextBillingCountry': 'US',
        'SetContextDealerNumber': 'WEB031017',
        'ASP.NET_SessionId': 'jvvrsgmnkdj41jfa3vnvwfn3',
        'RecentlyViewedProductsCookie': '5a647ef8-63f9-4aca-8905-c6159dc593ac',
        '_ga': 'GA1.2.390501460.1712820650',
        '_gcl_au': '1.1.943243943.1712820652',
        '_cls_v': '41db8a90-1b04-45b9-a30e-b42b50c8042c',
        '_cls_s': '807baeec-a3c5-4822-a926-67c067d21d31:0',
        'net_sess': '1712820668140168450',
        '_netelix': '3:0::::1712820668140:::630::8518951:0',
        'nex_user': '17128206681412961',
        '_fbp': 'fb.1.1712820669282.298127809',
        'OptanonAlertBoxClosed': '2024-04-11T07:31:22.526Z',
        '__pr.7w5': 'E_HO1zwoH7',
        '_br_uid_2': 'uid%3D8474892350299%3Av%3D15.0%3Ats%3D1712820667824%3Ahc%3D2',
        '2ebb0c9b-39e6-4e58-8f28-a49501067a22_Cart': '7d031340-2684-4d62-b11e-b1500047c83f',
        '__cf_bm': 'hfmuy55Df7b6muH3TffrOxiln2T_T_BUxVWGqmxwVxk-1712922750-1.0.1.1-40vaXL3tML3v0wse5dagD7z_sScY4kb.Q6pKqeVC.jgAlH0UzihoCznS38UueItp_8CnCRqyHfUvy6ED.zBHtg',
        'OptanonConsent': 'isIABGlobal=false&datestamp=Fri+Apr+12+2024+17%3A22%3A30+GMT%2B0530+(India+Standard+Time)&version=6.1.0&consentId=808c4b6f-0c53-4227-8a94-9cdf6f67713f&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=&legInt=&geolocation=US%3BNY&AwaitingReconsent=false',
    }
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    item={}
    for i in range(max_retires):
        url_request = requests.get(url=pdp_url,cookies=cookies,headers=headers)
        if url_request.status_code == 200:
            break


    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}

    response = Selector(text=url_request.text)

    dis = response.xpath('//div[@class="container"]//ul[@class="breadcrumbs"]//text()').getall()
    dis = ''.join(dis)
    if 'Discontinued' in dis:

        return {"statusCode":410,
                "error_messeage":"Product is discontinued"}

    if 'class="eb-sku"' not in url_request.text:
        error['statusCode'] = 404
        error['error_message'] = 'Product not found'
        return error

    item['vendor'] = vendor
    item['pdp_url'] = pdp_url


    try:
        sku = response.xpath('//div[@class="sku-item-block"]//span[@itemprop="sku"]//text()').get().strip()
        sku_value1 = re.findall(r'\d+', sku)
        sku_value = ''.join(sku_value1).strip()
        item['sku'] =sku
        if item['sku'] != product_sku:
            error['statusCode'] = 404
            error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{product_sku}"
            return error
        else:
            pass
    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = str(e)
        return error

        # EXTRACTING THE price USING XPATH
    price_list = []
    price = response.xpath('//div[@class="main-price"]/span[@itemprop="price"]/@content').get()
    if price != None:
        if price == 0.00:
            price_list.append({
                'min_qty': 1,
                'price_string': 'Call for price'.capitalize()
            })
        else:
            price.replace(",", "")
            price_list.append({
                "currency": "USD",
                'min_qty': 1,
                'price': float(price)
            })
    else:
        price_list.append({
            'min_qty': 1,
            'price_string': 'Call for price'
        })

    if price_list:
        item['price'] = price_list
    else:
        item['price'] = None
    available_to_checkout = response.xpath('//div//a[contains(text(),"Add To Cart")]//text()').get()
    if available_to_checkout != None:
        available_to_checkout = True if "Cart" in available_to_checkout else False

    cookies = {
        'liveagent_oref': '',
        'liveagent_sid': '8262c86e-4a5f-46f1-82a0-dbd16afafe90',
        'liveagent_vc': '2',
        'liveagent_ptid': '8262c86e-4a5f-46f1-82a0-dbd16afafe90',
        'SetContextLanguageCode': 'en-US',
        'locale': 'en-US',
        'SetContextCurrencyCode': 'USD',
        'SetContextBillingCountry': 'US',
        'SetContextDealerNumber': 'WEB031017',
        'ASP.NET_SessionId': 'jvvrsgmnkdj41jfa3vnvwfn3',
        'RecentlyViewedProductsCookie': '5a647ef8-63f9-4aca-8905-c6159dc593ac',
        '_ga': 'GA1.2.390501460.1712820650',
        '_gcl_au': '1.1.943243943.1712820652',
        '_cls_v': '41db8a90-1b04-45b9-a30e-b42b50c8042c',
        '_cls_s': '807baeec-a3c5-4822-a926-67c067d21d31:0',
        'net_sess': '1712820668140168450',
        '_netelix': '3:0::::1712820668140:::630::8518951:0',
        'nex_user': '17128206681412961',
        '_fbp': 'fb.1.1712820669282.298127809',
        'OptanonAlertBoxClosed': '2024-04-11T07:31:22.526Z',
        '__pr.7w5': 'E_HO1zwoH7',
        '_br_uid_2': 'uid%3D8474892350299%3Av%3D15.0%3Ats%3D1712820667824%3Ahc%3D2',
        '2ebb0c9b-39e6-4e58-8f28-a49501067a22_Cart': '7d031340-2684-4d62-b11e-b1500047c83f',
        '__cf_bm': 'hfmuy55Df7b6muH3TffrOxiln2T_T_BUxVWGqmxwVxk-1712922750-1.0.1.1-40vaXL3tML3v0wse5dagD7z_sScY4kb.Q6pKqeVC.jgAlH0UzihoCznS38UueItp_8CnCRqyHfUvy6ED.zBHtg',
        'OptanonConsent': 'isIABGlobal=false&datestamp=Fri+Apr+12+2024+17%3A22%3A30+GMT%2B0530+(India+Standard+Time)&version=6.1.0&consentId=808c4b6f-0c53-4227-8a94-9cdf6f67713f&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=&legInt=&geolocation=US%3BNY&AwaitingReconsent=false',
    }
    json_data = {'skusWithComma': sku_value, }

    respons = requests.post('https://www.coleparmer.com/Shared/GetProductInventory', cookies=cookies,
                            headers={
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'},
                            json=json_data)
    respons = respons.json()
    time_to_ship = respons["ProductServiceResposeModel"][0]["AvailabilityDto"]["Message"]

    estimated_lead_time = []
    in_stock = None
    if "Ships" in time_to_ship or "Days" in time_to_ship:
        estimated_lead_time.append({"min_qty": 1, "time_to_ship": {"raw_value": time_to_ship.strip()}})
        in_stock = False
    if "Stock" in time_to_ship:
        in_stock = True
        estimated_lead_time=None

    item['lead_time'] = estimated_lead_time
    item['available_to_checkout'] = available_to_checkout
    item['in_stock'] = in_stock

    # body = {"body": item}
    if item['lead_time'] == []:
        item['lead_time'] = None
    return {'statusCode': 200,
            'data': item}

