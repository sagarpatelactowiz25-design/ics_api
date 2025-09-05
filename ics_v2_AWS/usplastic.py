import json# install json
import requests# intall requests
from parsel import Selector # intsall parsel
max_retires = 5

def usplastic(pdp_url,product_sku,vendor="usplastic"):
    url_request=''
    error={}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_vuid=ef632752-2753-4312-8850-812da08e8490; _ga=GA1.1.585901471.1693810076; mt.v=2.1674097132.1693810076229; _gcl_au=1.1.1415447978.1693810076; hawkVisitorId=3b6504d6-9655-4257-a37c-8539a6bcecca; x-bni-fpc=5091ff99001baa3f47d022340dad9ff6; GSID5xrP77VpwPKH=74117054-87d8-4704-9531-5ec2ea870ada; STSID329660=5d0efa64-8e33-4f02-a4a1-5347d0f3a6f8; ltkpopup-suppression-932372fd-4483-44d6-b48d-b3d6b4376206=1; __utmz=105665415.1693982002.12.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ASP.NET_SessionId=yk01hl1vrtxkyzs0b4vjgvha; __utm_is_wdck=false; __utma=105665415.585901471.1693810076.1694006515.1694415585.19; __utmc=105665415; __utmt=1; __utmb=105665415.1.10.1694415585; __utm_is_did=hawkVisitId; ln_or=eyIxNTIxMjg0IjoiZCJ9; ltkSubscriber-AccountCreate=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; ltkSubscriber-CatalogRequest=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; ltkSubscriber-FooterMiniform=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; _ga_SJQ9F59SXT=GS1.1.1694415582.23.0.1694415586.56.0.0; ltkpopup-session-depth=1-2; x-bni-rncf=1694415571954; fcaid=e1e42bc8ad73444edde795f52775ff7fa9935d4340927ba7a50ec3b9df75278d; fcuid=c0ba036c-f98e-48cb-a213-b6cc7a5d889c; fccid=ba2d365b-a0ce-4173-add6-21cf4d6263eb; _uetsid=ccc25200507011eea02bef341a1ac3e9; _uetvid=00b649104aef11ee85148f63368655ef; _dd_s=logs=1&id=49d8adaa-afc3-46fb-b811-7651271f1647&created=1694415584708&expire=1694416546127',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    item={}
    for i in range(max_retires):
        url_request = requests.get(url=pdp_url,headers=headers)
        if url_request.status_code == 200:
            break

    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}

    if 'id="jsSku"' not in url_request.text:
        error['statusCode'] = 404
        error['error_message'] = 'Product not found'
        return error

    item['vendor'] = vendor
    item['pdp_url'] = pdp_url
    response = Selector(text=url_request.text)
    try:
        item['sku'] =response.xpath('//section[@class="productSummary"]//div[@class="sku"]//span//text()').get()
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
    # price_item['currency'] = "USD"
    if response.xpath('//div[@class="item-price"]//span[1]'):
        if response.xpath('//span[@class="item-price-new"][1]'):
            price = response.xpath('//span[@class="item-price-new"][1]//span[@class="jsFormatCurrency"]//text()').get()
            price_list.append({
                "currency": "USD",
                'min_qty': 1,
                'price': float(price)
            })
        else:

            price = response.xpath('//div[@class="item-price"]//span[@class="jsFormatCurrency"]//text()').get()
            price_list.append({
                "currency": "USD",
                'min_qty': 1,
                'price': float(price)
            })


    if response.xpath('//table[@class="table-discounts"]//tr'):
        for pro_price in response.xpath('//table[@class="table-discounts"]//tr'):
            min_qty = pro_price.xpath('.//td[1]//text()').get().split('at')[1].replace('+', '').strip()
            price_1 = pro_price.xpath('.//td[2]//span[@class="price"]//span[1]//text()').get()
            if price_1:
                try:
                    float_price = float(price_1)
                    price = "{:.2f}".format(float_price)
                    price_list.append({
                        "currency": "USD",
                        'min_qty': int(min_qty),
                        'price': float(price)
                    })
                except ValueError:
                    print("Failed to convert the price to a float.")
            else:
                price_list.append({
                    'min_qty': 1,
                    'price_string': 'Call for price'.capitalize()
                })

    if price_list:
        item['price'] = price_list
    else:
        item['price'] = None

    # EXTRACTING THE available_to_checkout USING XPATH
    available_to_checkout = response.xpath('//section[@class="productSummary"]//div[@id="skuOptions"]//text()').getall()
    available_to_checkout = ''.join(available_to_checkout).strip()
    if 'dd to Cart' in available_to_checkout:
        available_to_checkout = True
    else:
        available_to_checkout = False


    # EXTRACTING THE in_stock USING XPATH
    in_stock = response.xpath('//div[@class="item-stock"]//a//text()').getall()
    in_stock = ''.join(in_stock)
    estimated_lead_time = []
    # print(in_stock)
    if 'In Stock' in in_stock:
        in_stock = True
        # EXTRACTING THE estimated_lead_time USING XPATH
        estimated_lead_time = []
        lead_time = {'raw_value': "In-stock items ordered before 5:00 PM EST Monday to Friday (excluding holidays) are usually shipped out the same day."}
        estimated_lead_time.append(
            {
                'min_qty': 1,
                'time_to_ship': lead_time
            }
        )

    elif 'Overstock' in in_stock:
        in_stock = True

    elif 'vailable' in in_stock:
        in_stock = True

    elif 'Out of Stock (On Order)' in  in_stock:
        in_stock=False
        estimated_lead_time = []
        lead_time = {'raw_value': '''These items are temporarily out of stock. Placing an order for one of these items will put you in line to receive your shipment on a first-come, first-served basis. In most cases, you may choose to accept partial shipments during checkout. Click the bell icon or Get Notified, if available, to receive notifications about these items availability.'''}
        estimated_lead_time.append(
            {
                'min_qty': 1,
                'time_to_ship': lead_time
            }
        )

    elif'Out of Stock (Extended)'in in_stock:
        in_stock=False
        estimated_lead_time = []
        lead_time = {'raw_value': '''These items have been out of stock for a while. Click the bell icon or Get Notified, if available, to receive notifications about these items availability. You can also contact us for an estimate on when this product will be back in stock.'''}
        estimated_lead_time.append(
            {
                'min_qty': 1,
                'time_to_ship': lead_time
            }
        )

    elif 'Drop Ship' in in_stock:
        in_stock= False
        estimated_lead_time = []
        lead_time = {
            'raw_value': '''These items ship directly from the manufacturing plant. In many cases, items are shipped quickly, but we cannot guarantee a ship date. Return policy may vary depending on the vendor.'''}
        estimated_lead_time.append(
            {
                'min_qty': 1,
                'time_to_ship': lead_time
            }
        )
    else:
        in_stock = False
        estimated_lead_time=None


    item['lead_time'] = estimated_lead_time
    item['available_to_checkout'] = available_to_checkout
    item['in_stock'] = in_stock

    # body = {"body": item}
    if item['lead_time'] == []:
        item['lead_time'] = None
    return {'statusCode': 200,
            'data': item}
