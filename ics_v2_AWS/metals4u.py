import requests
import time
import json
import re
from parsel import Selector
def metals4u(pdp_url, sku, vendor="metals4u"):
    start_time = time.time()
    sess = requests.Session()
    url_request = str()
    error_ = dict()
    max_retries = 5
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9","Cache-Control": "no-cache",
            "Connection": "keep-alive","Pragma": "no-cache",
            "Referer": "https://www.google.com/","Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate","Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1","Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0","sec-ch-ua-platform": '"Windows"',
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }
        for i in range(max_retries):
            url_request = requests.get(
                pdp_url,
                headers=headers,
                verify=False
            )



            if url_request.status_code == 200:
                break
            else:
                print(url_request.status_code)
        if url_request.status_code == 200:
            pass
        else:
            return {
                "statusCode": 408,
                "error_message": " Request timeout, failed to reach host ",
            }

        response = Selector(url_request.text)
        # Defind dictionary for making data dictionary
        item = dict()
        # vendor Extracting :-
        item["vendor"] = "metals4u"
        item["pdp_url"] = pdp_url

        # SKU Extracting :-
        try:
            # sku1 = response.xpath("//div[@class='detailid']/span[@itemprop='productID']/text()").get()
            sku1 = response.xpath("//div[@class='product_meta']//span[@class='sku']/text()").get().replace("\n","").replace("\t","")
            item["sku"] = sku1

        except Exception as e:
            item["sku"] = None

        if item['sku'] != sku:
            error_['statusCode'] = 410
            error_['error_message'] = f"Scraped SKU does not match input SKU:{sku}"
            return error_

        # price extracting:-
        price_list = []
        dict_price = dict()
        try:
            # min_qty = response.xpath("//div[@class='quantitydiv detailquantityinput']/input/@value").get()
            min_qty = response.xpath('//div[@class="quantity"]/input[@name="quantity"][@aria-label="Product quantity"]/@value').get()
            if min_qty:
                dict_price["min_qty"] = int(min_qty)
            else:
                dict_price["min_qty"] = 1
        except Exception as e:
            dict_price["min_qty"] = 1
        try:
            price_multiple = response.xpath('//form[@class="variations_form cart"]/@data-product_variations').get()
            if price_multiple:
                price_multiple = json.loads(price_multiple)
                for price_data in price_multiple:
                    variant_name = price_data["attributes"]["attribute_pa_length-size"]
                    variant_price = price_data["display_price"]
                    multy_price = dict()
                    try:
                        price = variant_price.replace("$", "").replace(",","")
                        price = float(price)
                    except:
                        price = float(variant_price)
                    multy_price["min_qty"] = dict_price["min_qty"]
                    multy_price["price"] = price
                    multy_price["currency"] = "USD"
                    price_list.append(multy_price)
                item["price"] = price_list
            else:
                # for single price
                price_main = (response.xpath('//p[@class="price"]//span[contains(text(),"$")]/following-sibling::text()').get().replace("$", ""))
                price_main = price_main.replace(",", "")
                if price_main or price_main != "":
                    dict_price["price"] = float(price_main)
                    dict_price["currency"] = "USD"
                    price_list.append(dict_price)
                    item["price"] = price_list
                else:
                    dict_price["price_string"] = "Call for price"
                    price_list.append(dict_price)
                    item["price"] = price_list
        except Exception as e:
            print(e)
            dict_price["price_string"] = "Call for price"
            price_list.append(dict_price)
            item["price"] = price_list

        # available_to_checkout and in_stock Extracting :-
        try:
            # in_stock = response.xpath("//div[@class='addtocart detailaddtocart']/input[@class='buybutton detailbuybutton']")
            in_stock = response.xpath('//button[contains(text(),"Add to cart")]/text()').get()
            if in_stock:
                item["in_stock"] = True
                item["available_to_checkout"] = True
            else:
                item["in_stock"] = False
                item["available_to_checkout"] = False
        except Exception as e:
            return {"statusCode": 500, "error_message": "Internal Server Error" + str(e)}
        # Lead time
        try:
            if re.findall("https://www.metals4uonline.com/tool-steel", pdp_url) or re.findall("http://www.metals4uonline.com/tool-steel", pdp_url):
                lead_dict = {}
                lead_dict["min_qty"] = 1
                lead_dict["time_to_arrive"] = {"raw_value": "1 Day (delivered to your door) "}
                lead_list = []
                lead_list.append(lead_dict)
                item["lead_time"] = lead_list
            else:
                item["lead_time"] = None
        except Exception as e:
            return {"statusCode": 500, "error_message": "Internal Server Error" + str(e)}
        sess.close()
        # return response of statuscode and item dict
        total_time = f"total time :{time.time() - start_time}"
        print(total_time)
        return {"statusCode": 200, "data": item}
    except Exception as e:
        return {"statusCode": 500, "error_message": "Internal Server Error" + str(e)}
# if __name__ == "__main__":
#     event = {
#         "pdp_url": "https://www.metals4uonline.com/piano-hinge-1-1-4-x-1-1-4-x-1-16-6-long/",
#         "sku": "APIANOHINGE114",
#         "vendor": "metals4u",
#     }
#     print(json.dumps(metals4u(event["pdp_url"], event["sku"])))
