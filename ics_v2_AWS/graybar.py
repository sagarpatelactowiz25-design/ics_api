import re
import requests
from parsel import Selector

def graybar(url, sku, vendor='graybar'):
    try:
        url_request = str()
        error = dict()
        try:
            max_retires = 5
            for i in range(max_retires):
                url_request = requests.get(url=url)
                if url_request.status_code == 200:
                    break
            else:
                # The function must have logic for retries Max. 5
                # If request fails after 5 retries it should return following
                return {'statusCode': 408,
                        'error_message': 'Request timeout, failed to reach host'}
        except Exception as e:
            print(e)

        if '<span>SKU: </span>' not in url_request.text:
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
            item['sku'] = response.xpath('//div[@class="col-md-12"]//div[@class="sku"]//span[@class="code"]/text()').get('').strip()
            if item['sku'] != sku:
                error['statusCode'] = 404
                error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
                return error
            else:
                pass
        except Exception as e:
            # The function should return a dictionary having statusCode: 500;
            # If scraped sku does not match sku passed in input parameter
            error['statusCode'] = 500
            error['error_message'] = str(e)

        # url Extracting :-
        item['pdp_url'] = url

        # Price Extracting :-
        item_price = dict()


        price_list = list()
        if response.xpath('//div[@class="flex-row first-column pdpDesktopView"]//div[@class="sell-uom"]/span[last()]'):
            # Extract minimum quantity from the response using XPath and remove non-digit characters
            min_qty =re.sub(r'\D','',response.xpath('//div[@class="flex-row first-column pdpDesktopView"]//div[@class="sell-uom"]/span[last()]/text()').get().replace('$', '').replace(',', '').strip())
            original_price = dict(item_price)
            original_price['min_qty'] = int(min_qty)
        else:
            original_price = dict(item_price)
            original_price['min_qty'] = 1
        if response.xpath('//div[@class="flex-row first-column pdpDesktopView"]//p[@class="price"]/text()'):
            price = response.xpath('//div[@class="flex-row first-column pdpDesktopView"]//p[@class="price"]/text()').get().replace('$', '').replace(',', '').strip()
            original_price['price'] = float(price)
            original_price['currency'] = 'USD'
        else:
            original_price['price_string'] =  "Call For Price".capitalize()

        price_list.append(original_price)

        if 'Volume discounts available' in url_request.text:
            for tr in response.xpath('//table[@class="volume__prices"]//tr[./td]'):
                all_td = [i.strip() for i in tr.xpath(".//td//text()").getall() if i.strip()]
                original_price['min_qty'] = re.findall(r"\d+", all_td[0])
                original_price['price'] = all_td[1].replace('$', '').replace(',', '').strip()
                price_list.append(original_price)

        item['price'] = price_list
        # available_to_checkout Extracting :-

        if response.xpath('//button[@id="addToCartButton"]'):
            item['available_to_checkout'] = True
        else:
            item['available_to_checkout'] = False

        if response.xpath('//div[@class="flex-row first-column pdpDesktopView"]//i[@class="material-icons material-icons-green"]'):
            if response.xpath('//div[@class="flex-row first-column pdpDesktopView"]//i[@class="material-icons material-icons-green"]/text()').get() == "check_circle":
                item['in_stock'] = True
            else:
                item['in_stock'] = False
        else:
            item['in_stock'] = False

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
                "error_message": "Internal server error" + str(e) + url_request}
