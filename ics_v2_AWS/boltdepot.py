import requests
from parsel import Selector
import re


def boltdepot(pdp_url, sku='sku'):
    try:
        error = {}
        url_request = str()
        max_retires = 5
        for i in range(max_retires):
            url_request = requests.get(pdp_url, verify=False)
            if url_request.status_code == 200:
                break
        if url_request.status_code == 200:
            pass
        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}
        if 'class="product-details-table"' not in url_request.text:
            error['statusCode'] = 404
            error['error_message'] = 'Product not found'
            return error
        response_text = url_request.text
        if 'class="discontinued"' in response_text:
            return {"statusCode": 410,
                    "error_message": "Product is discontinued"}
        else:
            selector = Selector(text=response_text)
            item = dict()
            # Vendor Extracting :-
            item['vendor'] = 'boltdepot'
            # Sku Extracting :-
            try:
                item['pdp_url'] = pdp_url
                scrapped_sku = selector.xpath(
                    "//span[@id='ctl00_ctl00_Body_Body__productsTableControl__sectionsRepeater_ctl00__itemsRepeater_ctl00__productIdLabel']/text()").get()
                if sku:
                    scrapped_sku = scrapped_sku
                else:
                    scrapped_sku = pdp_url.split("product=")[1]
                    if scrapped_sku.strip().lower() != sku.strip().lower():
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
            # ************************************* PRICE *******************
            item_price = []
            # Extracting all prices and quantities
            all_prices = selector.xpath("//td[@class='cell-price cell-price-single']/span/text()").getall()
            all_quantities = selector.xpath(
                "//td[@class='cell-price cell-price-single']//span[@class='perQty']/text()").getall()

            # Pre-processing prices and quantities
            all_prices = [price.replace("\r", "").replace("\n", "").strip().replace("$", "") for price in all_prices if
                          price.strip()]
            all_quantities = [quantity.replace("ea", "1") for quantity in all_quantities]

            # Extracting numerical quantities
            for i, quantity in enumerate(all_quantities):
                number_matches = re.findall(r'\b\d{1,3}(?:,\d{3})*(?: \d+)?\b', quantity)
                if number_matches:
                    all_quantities[i] = int(number_matches[0].replace(",", ""))

            # Creating item_price list
            for price, quantity in zip(all_prices, all_quantities):
                try:
                    price_per_unit = round(float(price.replace(',','')) / quantity, 2)
                    item_price.append({'currency': 'USD', 'min_qty': quantity, 'price': price_per_unit})
                except Exception as e:
                    print(f"Error processing price {price} and quantity {quantity}: {e}")

            # if not item_price:
            #     item_price = [{'min_qty': 1, 'price_string': "Call for price"}]

            if not item_price:
                item_price = None
            item['price'] = item_price

            # Lead_time Extracting :-
            item['lead_time'] = None  # Lead time not available in this case
            # Avaliable & InStock Extracting :-
            available_to_checkout = selector.xpath(
                "//div//table[@id='product-list-table']//button[contains(@onclick, 'productTable')]")
            if not available_to_checkout:
                item['available_to_checkout'] = False
                item['in_stock'] = False
            else:
                item['available_to_checkout'] = True
                item['in_stock'] = True

            if 'statusCode' in item.keys():
                if item['statusCode'] == 500:
                    return item
                elif item['statusCode'] == 404:
                    return item
            else:
                return {'statusCode': 200,
                        'data': item}
    except Exception as e:
        return {'statusCode': 500, 'error_message': "An unexpected error occurred: " + str(e)}


# if __name__ == '__main__':
#     # parse function call with products_url and sku :-
#     event = {'sku': '20750',
#              'pdp_url': 'https://www.boltdepot.com/Product-Details.aspx?product=20750',
#              'vendor': 'boltdepot'}
#     print(boltdepot(pdp_url=event['pdp_url'], sku=event['sku']))