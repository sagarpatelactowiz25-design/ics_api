from parsel import Selector
import json
import time
import requests
max_retires = 5
def zyte_requests(url):

    max_retires = 5
    for i in range(max_retires):
        api_response = requests.post(
            "https://api.zyte.com/v1/extract",
            auth=("9dbe950ef6284a5da9e7749db9f7cbd1", ""),
            json={
                "url": f"{url}",
                "browserHtml": True,
            },
            timeout=500
        )
        status = api_response.status_code
        try:
            browser_html: str = api_response.json()["browserHtml"]
            return [browser_html, status]
        except Exception as e:
            time.sleep(3)
    else:
        # The function must have logic for retries Max. 5
        # If request fails after 5 retries it should return following
        return {"statusCode": 408,
                "error_message": "Request timeout, failed to reach host"}

def nbk(pdp_url, sku, vendor="nbk"):

    try:
        response_list = zyte_requests(pdp_url)
        response_text = response_list[0]
        response = Selector(text = response_text)
        status = response_list[1]

        # Checking if  Response is 200 and product_name in the response
        if status == 200 and response.xpath('//div[@class="subtitle"]/p/text()'):
            pdp_sku = response.xpath(
                '//table[contains(@class,"highlight") or contains(@class,"Highlight")]//tbody/tr/td[@class="hinban"]//text()').get()
            if sku == pdp_sku:

                # Extract add_to_cart using xpath
                add_to_cart = response.xpath(
                    '//table[contains(@class,"highlight") or contains(@class,"Highlight")]//tbody/tr/td/a[text()="Cart"]')
                available_to_checkout = True if add_to_cart else False
                try:
                    # Extract price using xpath
                    price_value = response.xpath(
                        '//table[contains(@class,"highlight") or contains(@class,"Highlight")]//tbody/tr/td[@class="buy"]/text()').get().replace(
                        ",", "")
                    minimum_quantity = response.xpath(
                        '//table[contains(@class,"highlight") or contains(@class,"Highlight")]//tbody//td/input[@class="amount"]/@value').get()
                    minimum_quantity = int(minimum_quantity) if minimum_quantity else 1
                    price = [{'min_qty': minimum_quantity, 'price': float(price_value),
                              'currency': 'USD'}]
                except:
                    price = [{'min_qty': 1, 'price_string': "Call For Price".capitalize()}]

                if price_value != "-" and add_to_cart:
                    in_stock = True
                else:
                    in_stock = False

                data = {'vendor': vendor, 'pdp_url': pdp_url, 'sku': pdp_sku, 'price': price,
                        'lead_time': None, 'available_to_checkout': available_to_checkout,
                        'in_stock': in_stock}

                return {"statusCode": 200,
                        "data": data}
            else:
                return {"statusCode": 404,
                        "error_message": f"Scraped SKU:{pdp_sku} does not match input SKU:{sku}"}

        elif status == 404:
            return {"statusCode": 404,
                    "error_message": "Product not found"}
        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}

    except Exception as e:
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}


# if __name__ == "__main__":
#     l = [
# "https://www.nbk1560.com/en-US/products/machine_element/handle/AH/AH-100/",
# "https://www.nbk1560.com/en-US/products/machine_element/handle/AH-N/AH-100-N/",
# "https://www.nbk1560.com/en-US/products/machine_element/handle/AH/AH-125/",
# "https://www.nbk1560.com/en-US/products/machine_element/handle/AH-N/AH-125-N/",
# "https://www.nbk1560.com/en-US/products/machine_element/handle/AH/AH-140/",
# "https://www.nbk1560.com/en-US/products/machine_element/handle/AH-N/AH-140-N/"
# ]
#     for i in l:
#         event = {"pdp_url":i,
#                  "sku":i.split("/")[-2],
#                  "vendor":"nbk"}
#         print(json.dumps(nbk(event["pdp_url"], event["sku"], event["vendor"])))
# #     event = {
# #     "pdp_url": "https://www.nbk1560.com/en-US/products/machine_element/cross_clamper/FBCS-C/FBCS-M8-12-C/",
# #     "sku": "FBCS-M8-12-C",
# #     "vendor": "nbk"
# # }
# #     print(json.dumps(nbk(event["pdp_url"],event["sku"],event["vendor"])))
