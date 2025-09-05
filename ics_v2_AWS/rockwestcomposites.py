from parsel import Selector
import json
import requests


def clean_text(value):
    return str(value).replace('\n', '').replace('"', '').replace('+', '').replace('P/N:', '').strip()


def rockwestcomposites(url, sku, vendor="rockwestcomposites"):
    error = {}
    try:
        try:
            response1 = requests.get(url)
        except:
            response1 = requests.get(url)
        if response1.status_code != 200:
            for k_ in range(0, 5):
                response1 = requests.get(url)

                if response1.status_code == 200:
                    break

        data = {}
        if response1.status_code == 200:
            base_sku = sku.replace('P/N:', '').strip()
            price_list = []
            price1 = None
            price2 = None
            qty1 = None
            qty2 = None
            in_stock = None
            available_to_checkout = None
            is_page_available = False
            html_response = Selector(response1.text)
            new_sku = html_response.xpath('//span[@class="product-id product-sku"]/text()').get()
            try:
                if new_sku != None:
                    new_sku = new_sku.replace('P/N:', '').strip()
                    # print(new_sku)
                    sku_model = html_response.xpath(
                        '//div[@class="attribute"]//button[@class="length-attribute "]').getall()
                    if sku_model != []:
                        selected_sku_variant = html_response.xpath(
                            '//button[@class="length-attribute selected"]/@data-attr-value').get()
                        if selected_sku_variant != None:
                            tmp_sku_variant = new_sku + f"""-{selected_sku_variant.replace('"', '')}"""

                            if base_sku.lower() == tmp_sku_variant.lower():
                                is_page_available = True
                                data["sku"] = base_sku
                                qty1 = html_response.xpath(
                                    '//div[@class="tiered"]//span[@class="tier-quantity"]/text()').get()
                                qty2 = html_response.xpath(
                                    '//div[@class="tiered-pricing"]/following-sibling::div/span[@class="tier-quantity"]/text()').get()
                                price1 = html_response.xpath(
                                    '//div[@class="price"]//span[@class="sales default-price"]/@data-price').get()
                                price2 = html_response.xpath(
                                    '//div[@class="tiered"]//span[@class="sales default-price"]/following::span[@class="sales default-price"]/@data-price').get()

                                in_stock = html_response.xpath(
                                    '//button[@class="add-to-cart btn-Primary  js-add-to-cart"]/@disabled').get()
                                if in_stock != None:
                                    if 'disabled' in in_stock:
                                        in_stock = False
                                        available_to_checkout = False
                                    else:
                                        in_stock = True
                                        available_to_checkout = True
                                else:
                                    in_stock = True
                                    available_to_checkout = True
                            else:
                                for sku_button_res in sku_model:
                                    sku_button_res = Selector(sku_button_res)
                                    sku_url = sku_button_res.xpath('.//@data-url').get()
                                    sku_variant = sku_button_res.xpath('.//@data-attr-value').get()
                                    if sku_variant != None:
                                        tmp_sku_variant = new_sku + f"-{clean_text(sku_variant)}"
                                        # tmp_sku_variant = new_sku + f"-{sku_variant.replace('"', '')}"
                                        if base_sku.lower() == tmp_sku_variant.lower():
                                            is_page_available = True
                                            data["sku"] = base_sku
                                            variant = requests.get(sku_url)
                                            dic_data = json.loads(variant.text)
                                            # new_sku = dic_data['product']['gtmGA4Data']['item_variant']
                                            price1 = dic_data['product']['gtmGA4Data']['price']

                                            in_stock = dic_data['product']['inStock']
                                            if in_stock == True:
                                                in_stock = True
                                                available_to_checkout = True
                                            else:
                                                in_stock = False
                                                available_to_checkout = False
                                            break
                        else:
                            error['statusCode'] = 500
                            error['error_message'] = "Internal server error"
                            return error


                    else:
                        sku_div_list = html_response.xpath(
                            '//div[@class="product-detail-right"]/div[@class="grouped-product"]').getall()
                        if sku_div_list != []:
                            for new_data in sku_div_list:
                                sku_div = Selector(new_data)
                                new_sku = sku_div.xpath('//span[@class="product-id product-sku"]/text()').get()
                                if new_sku != None:
                                    # new_sku = new_sku.replace('P/N:', '').strip()
                                    new_sku = clean_text(new_sku)
                                    if new_sku.lower() == base_sku.lower():  # check new and old sku are same
                                        is_page_available = True
                                        data['sku'] = base_sku

                                        qty1 = sku_div.xpath(
                                            '//div[@class="tiered"]//span[@class="tier-quantity"]/text()').get()
                                        qty2 = sku_div.xpath(
                                            '//div[@class="tiered-pricing"]/following-sibling::div/span[@class="tier-quantity"]/text()').get()
                                        price1 = sku_div.xpath(
                                            '//div[@class="price"]//span[@class="sales default-price"]/@data-price').get()
                                        price2 = sku_div.xpath(
                                            '//div[@class="tiered"]//span[@class="sales default-price"]/following::span[@class="sales default-price"]/@data-price').get()

                                        in_stock = sku_div.xpath(
                                            '//button[@class="add-to-cart btn-Primary  js-add-to-cart"]/@disabled').get()
                                        if in_stock != None:
                                            if 'disabled' in in_stock:
                                                in_stock = False
                                                available_to_checkout = False
                                            else:
                                                in_stock = True
                                                available_to_checkout = True
                                        else:
                                            in_stock = True
                                            available_to_checkout = True
                                        break
                                    else:
                                        data = {"sku": 410}

                        else:
                            if new_sku.lower() == base_sku.lower():
                                is_page_available = True
                                data["sku"] = base_sku
                                qty1 = html_response.xpath('//span[@class="tier-quantity"]/text()').get()
                                qty2 = html_response.xpath(
                                    '//div[@class="tiered-pricing"]/following-sibling::div/span[@class="tier-quantity"]/text()').get()
                                price1 = html_response.xpath('//span[@class="sales default-price"]/@data-price').get()
                                price2 = html_response.xpath(
                                    '//div[@class="tiered-pricing"]/following-sibling::div//span[@class="sales default-price"]/@data-price').get()

                                in_stock = html_response.xpath(
                                    '//button[@class="add-to-cart btn-Primary  js-add-to-cart"]/@disabled').get()
                                if in_stock != None:
                                    if 'disabled' in in_stock:
                                        in_stock = False
                                        available_to_checkout = False
                                    else:
                                        in_stock = True
                                        available_to_checkout = True
                                else:
                                    in_stock = True
                                    available_to_checkout = True
                            else:
                                error['statusCode'] = 410
                                error['error_message'] = f"Scraped sku:{new_sku} does not match input sku:{sku}"
                                return error
                    if is_page_available == True:
                        if qty1:
                            # qty1 = qty1.split('-')[0].replace('\n', '').strip()
                            qty1 = clean_text(qty1.split('-')[0])

                        if qty2:
                            qty2 = clean_text(qty2.split('-')[0])
                            # qty2 = qty2.split('-')[0].replace('\n', '').replace('+', '').strip()
                        if price1:
                            if price1 != 'null':
                                price1 = clean_text(price1)
                                # price1 = price1.replace('\n', '').strip().replace('"', '')
                            else:
                                price1 = None
                        if price2:
                            if price2 != 'null':
                                price2 = clean_text(price2)
                                # price2 = price2.replace('\n', '').strip().replace('"', '')
                            else:
                                price2 = None
                        if price1 != None:
                            if qty1 != None:
                                price_list.append({"min_qty": int(qty1), "price": float(price1), "currency": "USD"})
                            else:
                                price_list.append({"min_qty": 1, "price": float(price1), "currency": "USD"})
                        if price2 != None:
                            if qty2 != None:
                                price_list.append({"min_qty": int(qty2), "price": float(price2), "currency": "USD"})
                            else:
                                price_list.append({"min_qty": 1, "price": float(price2), "currency": "USD"})
                        if price1 == None and price2 == None:
                            price_list.append({"min_qty": 1, "price_string": 'Call for Price'})
                        data["price"] = price_list
                        data["vendor"] = vendor
                        data["pdp_url"] = url
                        data["in_stock"] = in_stock
                        data["lead_time"] = None
                        data["available_to_checkout"] = available_to_checkout
                        return {'statusCode': 200,
                                'data': data}
                    else:
                        error['statusCode'] = 410
                        error['error_message'] = f"Input sku:{base_sku} page not found"
                        return error
                else:
                    error['statusCode'] = 410
                    error['error_message'] = f"Input sku:{base_sku} page not found"
                    return error
            except Exception as e:
                print(e)
                error['statusCode'] = 500
                error['error_message'] = "Internal server error"
                return error
        elif response1.status_code==404:
            error['statusCode'] = 410
            error['error_message'] = "Product not found"
            return error
        else:
            error['statusCode'] = 408
            error['error_message'] = "Request timeout, failed to reach host"
            return error
    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = "Internal server error"
        return error


# if __name__ == '__main__':
#     event = {"sku": "1035-253", "vendor": "rockwestcomposites", "pdp_url": "https://www.rockwestcomposites.com/1035-25.html"}
#     print(json.dumps(rockwestcomposites(url=event['pdp_url'], sku=event['sku'])))