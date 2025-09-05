import re
from curl_cffi import requests
from parsel import Selector

def knightoptical(pdp_url, sku, vendor='knightoptical'):
    try:
        url_request = str()
        error = dict()
        try:
            max_retires = 5
            for i in range(max_retires):
                url_request = requests.get(url=pdp_url,
                                           impersonate="edge101")
                if url_request.status_code == 200:
                    break
            else:
                # The function must have logic for retries Max. 5
                # If request fails after 5 retries it should return following
                return {'statusCode': 408,
                        'error_message': 'Request timeout, failed to reach host'}
        except Exception as e:
            print(e)


        if 'class="product attribute sku"' not in url_request.text:
            error['statusCode'] = 404
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
            item['sku'] = "".join(response.xpath("//*[contains(@class,'sku')]//text()").getall()).replace("SKU:", "").strip()
            if item['sku'] != sku:
                error['statusCode'] = 404
                error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
                return error
            else:
                pass
        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = str(e)
            return error

        # url Extracting :-
        item['pdp_url'] = pdp_url

        # Price Extracting :-
        item_price = dict()
        item_price['currency'] = 'USD'

        price = "".join([i.strip() for i in response.xpath('//div[@data-role="priceBox"]//text()').getall() if i.strip()])
        price_discount = " ".join(
            [i.strip() for i in response.xpath('//ul[@class="prices-tier items"]//li//text()').getall() if i.strip()])

        price_list = list()
        if price:
            original_price = dict(item_price)
            # print(price)
            if '$' in price:
                original_price['price'] = float(price.replace('US', '').replace('$', '').replace(',', ''))
            elif '£' in price:
                price = price.replace('£', '').replace(',', '')
                price = float(price) * 1.39
                price = round(price, 2)
                original_price['price'] = price
            elif '€' in price:
                price = price.replace('€', '').replace(',', '')
                price = float(price) * 1.0944
                price = round(price, 2)
                original_price['price'] = price
            original_price['min_qty'] = 1
            price_list.append(original_price)
        else:
            item_price['price'] = 'Call For Price'

        if price_discount:
            if "$" in price_discount:
                price_discount_qty = "".join(re.findall("(\d+(?:\.\d+)?)", price_discount.split("$")[0]))
                price_discount_1 = "".join(re.findall("(\d+(?:\.\d+)?)", price_discount.split("$")[1])[0])

                discount_price = dict(item_price)
                # if '$' in price_discount_1:
                discount_price['price'] = float(price_discount_1.replace('US', '').replace('$', '').replace(',', ''))
                discount_price['min_qty'] = int(price_discount_qty)
                price_list.append(discount_price)
            elif '£' in price_discount:
                price_discount_qty = "".join(re.findall("(\d+(?:\.\d+)?)", price_discount.split("£")[0]))
                price_discount_1 = "".join(re.findall("(\d+(?:\.\d+)?)", price_discount.split("£")[1])[0])
                discount_price = dict(item_price)
                price_discount_1 = price_discount_1.replace('£', '').replace(',', '')
                price_discount_1 = float(price_discount_1) * 1.39
                price_discount_1 = round(price_discount_1, 2)
                discount_price['price'] = price_discount_1
                discount_price['min_qty'] = int(price_discount_qty)
                price_list.append(discount_price)
            elif '€' in price_discount:
                price_discount_qty = "".join(re.findall("(\d+(?:\.\d+)?)", price_discount.split("€")[0]))
                price_discount_1 = "".join(re.findall("(\d+(?:\.\d+)?)", price_discount.split("€")[1])[0])
                price_discount_1 = price_discount_1.replace('£', '').replace(',', '')
                price_discount_1 = float(price_discount_1) * 1.0944
                price_discount_1 = round(price_discount_1, 2)
                item_price['price'] = price_discount_1
                item_price['min_qty'] = int(price_discount_qty)
                price_list.append(item_price)


        item['price'] = price_list

        # available_to_checkout Extracting :-
        add_to_cart_re = response.xpath('//div[@class="col-md-12"]//button[@disabled="false"]')
        if add_to_cart_re:
            item['available_to_checkout'] = False
        else:
            item['available_to_checkout'] = True

        item['lead_time'] = None
        estimated_lead_time_list = list()
        # Lead_time request function and return json :-
        if 1 == len(response.xpath('//div[@class="text-right"]//div')):
            estimated_lead_time_check = " ".join(
                [i.strip() for i in response.xpath('//div[@class="text-right"]//text()').getall() if i.strip()])
            if "in stock" in estimated_lead_time_check.lower():
                estimated_lead_time_check = estimated_lead_time_check
                if "sku" in estimated_lead_time_check.lower():
                    estimated_lead_time_check1 = estimated_lead_time_check.split("SKU:")[0]
                    if "in stock" in estimated_lead_time_check1.lower():
                        estimated_lead_time = ' '
                    else:
                        estimated_lead_time = estimated_lead_time_check1
                    if estimated_lead_time.strip():
                        estimated_lead_time_list.append({'min_qty': 1, 'time_to_ship': {'raw_value': estimated_lead_time}})
                        if estimated_lead_time_list:
                            item['lead_time'] = estimated_lead_time_list
                        else:
                            item['lead_time'] = None

                item['in_stock'] = True
            else:
                item['in_stock'] = False
                if "sku" in estimated_lead_time_check.lower():
                    estimated_lead_time_check1 = estimated_lead_time_check.split("SKU:")[0].strip()
                    if "in stock" in estimated_lead_time_check1.lower():
                        estimated_lead_time = ' '
                    else:
                        estimated_lead_time = estimated_lead_time_check1
                    if estimated_lead_time.strip():
                        estimated_lead_time_list.append(
                            {'min_qty': 1, 'time_to_ship': {'raw_value': estimated_lead_time}})
                        if estimated_lead_time_list:
                            item['lead_time'] = estimated_lead_time_list
                        else:
                            item['lead_time'] = None

        elif 2 == len(response.xpath('//div[@class="text-right"]//div')):
            estimated_lead_time_check = " ".join(
                [i.strip() for i in response.xpath('//div[@class="text-right"]//div//text()').getall() if i.strip()])
            if "in stock" in estimated_lead_time_check.lower():
                estimated_lead_time_check = estimated_lead_time_check.strip()
                if "sku" in estimated_lead_time_check.lower():
                    estimated_lead_time_check1 = estimated_lead_time_check.split("SKU:")[0].strip()
                    if "in stock" in estimated_lead_time_check1.lower():
                        estimated_lead_time = ' '
                    else:
                        estimated_lead_time = estimated_lead_time_check1
                    if estimated_lead_time.strip():
                        estimated_lead_time_list.append(
                            {'min_qty': 1, 'time_to_ship': {'raw_value': estimated_lead_time}})
                        if estimated_lead_time_list:
                            item['lead_time'] = estimated_lead_time_list
                        else:
                            item['lead_time'] = None
                item['in_stock'] = True
            else:
                item['in_stock'] = False

                if "sku" in estimated_lead_time_check.lower():
                    estimated_lead_time_check1 = estimated_lead_time_check.split("SKU:")[0].strip()
                if "in stock" in estimated_lead_time_check1.lower():
                    estimated_lead_time = ' '
                else:
                    estimated_lead_time = estimated_lead_time_check1

                if estimated_lead_time.strip():
                    estimated_lead_time_list.append({'min_qty': 1, 'time_to_ship': {'raw_value': estimated_lead_time}})
                    if estimated_lead_time_list:
                        item['lead_time'] = estimated_lead_time_list
                    else:
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


# if __name__ == '__main__':
#     # parse function call with products_url and sku :-
#
#     data = knightoptical(url="https://www.knightoptical.com/stock/default/dichroic-colour-correction-filter-6300k-to-5100k-dia-12-5mm.html",
#                          sku="009FCC12")
#     # print json :-
#     print(data)