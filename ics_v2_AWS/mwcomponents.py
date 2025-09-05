import requests
from parsel import Selector
import re

def mwcomponents(pdp_url, sku='sku'):
    error = {}
    url_request = str()
    max_retires = 5
    for i in range(max_retires):
        url_request= requests.get(pdp_url, verify=False)
        if url_request.status_code == 200:
            break
    if url_request.status_code == 200:
        pass
    else:
        return {'statusCode': 408,
                'error_message':'Request timeout, failed to reach host'}
    if 'class="hd-ty mb-16 md:hd-xs md:!font-normal"' not in url_request.text:
        error['statusCode'] = 404
        error['error_message'] = 'Product not found'
        return error

    response_text = url_request.text
    if 'class="discontinued"' in response_text:
        return {"statusCode": 410,
                "error_message": "Product is discontinued"}
    else:
        selector = Selector(text=response_text)
        # print(response_text)
        item = dict()
        # Vendor Extracting :-
        item['vendor'] = 'mwcomponents'
        # Sku Extracting :-
        try:
            scrapped_sku = "".join(selector.xpath('//h1[contains(@class,"hd-ty mb-16 md:hd-xs md:!font-normal")]//text()').get().strip()).split(" -")[0].strip().lstrip()
            if scrapped_sku != sku:
                error['statusCode'] = 404
                error['error_message'] = f"Scraped SKU:{scrapped_sku} does not match input SKU:{sku}"
                return error

        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = "Internal server error" + str(e)
            return error

        # Pdp_url Extracting :-
        item['sku'] = sku
        item['pdp_url'] = pdp_url
        #************************************* PRICE *******************
        id_selector = selector.xpath('//div//a[contains(@class,"button-primary min")]//@href | //div//a[contains(@class,"text-sm text-accent-b-100")]//@href')
        id_value = None
        if id_selector:
            href = id_selector[0].get()
            if 'id=' in href:
                id_value = href.split('id=')[-1].split('&')[0]
            elif 'variant=' in href:
                id_value = href.split('variant=')[-1]
        # print("id =", id_value)
        qty = selector.xpath("//div[@class='input-float-label -floating']//input/@value").extract_first()

        cookies = {
            '_vwo_uuid_v2': 'D676F3C79E5A61B27EB7F96AF6598C1A9|b5c4666bf3f3011d648cff93d1f8378c',
            '_vwo_uuid': 'D676F3C79E5A61B27EB7F96AF6598C1A9',
            '_vwo_ds': '3%241712420946%3A60.14309482%3A%3A',
            '_vis_opt_exp_2_exclude': '1',
            '_gcl_au': '1.1.1563174351.1712420948',
            '_ALGOLIA': 'anonymous-c9d3476e-e286-42ab-a1ef-2e9a145fd708',
            'ConstructorioID_client_id': '47cedd61-02b9-4777-a492-ad658e112824',
            '_ga': 'GA1.1.1105216121.1712420948',
            'slireg': 'https://scout.us4.salesloft.com',
            'sliguid': '65211465-3ca9-4836-90b0-9368089feaa3',
            'slirequested': 'true',
            '_uetvid': 'ca896b30f43211eeb3ed2f05bb020930',
            '_uetsid': '3baf1210f6ab11eeac04091d7440ac05',
            '_ga_JPXYZF8MDE': 'deleted',
            '_clck': 'zwda88%7C2%7Cfku%7C0%7C1557',
            '_vis_opt_s': '3%7C',
            '_vis_opt_test_cookie': '1',
            'CraftSessionId': 'aq9mgctf2lei2h68kjff79lcir',
            'CRAFT_CSRF_TOKEN': 'c42f1c9986aeb12f74343fca57e936c26ce43d3cf49d8748069f94327d211198a%3A2%3A%7Bi%3A0%3Bs%3A16%3A%22CRAFT_CSRF_TOKEN%22%3Bi%3A1%3Bs%3A40%3A%22YCdeZeKD0Dl_8QsV64jN8jwuDFxmq5cdQ_yc-ufz%22%3B%7D',
            # '_clsk': '19n6abr%7C1712824292573%7C1%7C1%7Cn.clarity.ms%2Fcollect',
            # 'ff1d04e59fd3f9b7d919198d7b037429_commerce_cart': '7c6705bf26d3deae844091ceac295e8fd6a121f3b45dcfd7137c99d43ef000eca%3A2%3A%7Bi%3A0%3Bs%3A46%3A%22ff1d04e59fd3f9b7d919198d7b037429_commerce_cart%22%3Bi%3A1%3Bs%3A32%3A%22eb1d0f61a815d57f123c8d4d16b5f806%22%3B%7D',
            # '_vwo_sn': '403348%3A1%3A%3A%3A1',
            # '_ga_JPXYZF8MDE': 'GS1.1.1712824301.4.1.1712824301.0.0.0',
        }

        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'referer': f'{pdp_url}',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'template': '0df6c25d1630fcefcaa38920b54264d25f8a3be008cb0f4452da4fb52df199a2_partials/products/pricing-table',
            'id': f'{id_value}',
            'modalTheme': 'false',
            'useInCart': 'false',
            'minimumRuleSet': '',
            'qty': f'{qty}',
        }

        response1 = requests.get(
            'https://www.mwcomponents.com/actions/web/turbo/render-template',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        # print(response1.text)
        item_price = []
        response1 = Selector(response1.text)
        table = response1.xpath('//table[@class="w-full text-sm"]/tbody')
        if table:
            for row in response1.xpath('//tbody/tr[@class="border-b border-primary-200-08"]'):
                price_item = {}
                qty = row.xpath(".//td[1]/text()").get().replace("+", "")
                if "-" in qty:
                    qty = qty.split(" -")[0]
                # Cast min_qty to integer
                price_item['min_qty'] = int(qty)

                price = row.xpath('.//td[@class="py-8"][2]/text()').get()
                if 'Call for price' in price:
                    price_item['price_string'] = 'Call For Price'
                else:
                    price = "".join(re.sub(r"^\$", '', price))
                    if "," in str(price):
                        price = float(price.replace(',', ''))
                    else:
                        price = float(price)
                    price_item['currency'] = "USD"
                    price_item['price'] = price

                item_price.append(price_item)

        else:
            price_item = {}
            qty = selector.xpath('//input[@name="qty"]/@min').get()

            price = selector.xpath("//input[contains(@id,'input')]/@value").get()
            if price is not None:
                if '$' in price:
                    price = "".join(re.sub(r'\$', '', price))
                    if "," in str(price):
                        price = float(price.replace(',', ''))
                    else:
                        price = float(price)
                    price_item['currency'] = "USD"
                    price_item['min_qty'] = int(qty)
                    price_item['price'] = price
            else:
                price_item['min_qty'] = int(qty)
                price_item['price_string'] = 'Call For Price'
            item_price.append(price_item)
        for price_item in item_price:
            if 'price' not in price_item:
                price_item['min_qty'] = int(qty)
                price_item['price_string'] = "Call For Price"
        if not item_price:
            item_price = None
        item['price'] = item_price
        # Lead_time Extracting :-

        lead_time_text = selector.xpath("//div//table[@class='w-full table-fixed text-md']//tr[3]//td//text()").get()
        if 'Backordered parts' in response_text:
            est_list = []
            if lead_time_text:
                cleaned_lead_time_text = lead_time_text.strip().replace("In-stock parts:", "").strip()
                if cleaned_lead_time_text:
                    est_list.append({
                        'min_qty': 1,
                        'time_to_stock': {'raw_value': cleaned_lead_time_text}
                    })
        else:
            est_list = []
            if lead_time_text:
                cleaned_lead_time_text = lead_time_text.strip().replace("In-stock parts:", "").strip()
                if cleaned_lead_time_text:
                    est_list.append({
                        'min_qty': 1,
                        'time_to_ship': {'raw_value': cleaned_lead_time_text}
                    })
        item['lead_time'] = est_list


        # Available_to_checkout Extracting :-
        in_stock_elements = selector.xpath('//table//td//div[contains(@class,"inline-flex items-center gap-8 text-primary-200")]')
        if in_stock_elements:
            in_stock_text = in_stock_elements[0].xpath('.//text()').get(default='').strip()
            if 'Low Stock' in in_stock_text or 'In-stock' in in_stock_text:
                item['in_stock'] = True
            else:
                item['in_stock'] = False
        else:
            item['in_stock'] = False

        if 'Add to Quote' in response1.get():
            item['available_to_checkout'] = False

        elif 'Add to Cart' in response1.get():
            item['available_to_checkout'] = True


        if 'statusCode' in item.keys():
            if item['statusCode'] == 500:
                return item
            elif item['statusCode'] == 404:
                return item
        else:
            return {'statusCode': 200,
                    'data': item}
