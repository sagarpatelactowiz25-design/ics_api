import re
import json
import html
import time
import urllib
import itertools
from parsel import Selector
import concurrent.futures
from curl_cffi import requests

# Function to perform an HTTP GET request
def fetch_url(url):
    try:
        response = requests.get(url)
        return response.status_code, url, response.text
    except requests.RequestException as e:
        return f"Error: {e}", url

# List of URLs to fetch


# Perform concurrent requests
def fetch_all_urls(urls):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Map the fetch_url function to the URLs
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            print(url)
            try:
                status_code, url, response_text = future.result()
                results.append((status_code, url, response_text))
            except Exception as exc:
                results.append((f"Generated an exception: {exc}", url))
    return results


def zyte_requests(url):
    import requests as rs

    max_retires = 5
    for i in range(max_retires):
        api_response = rs.post(
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
            print(e)
    else:
        # If request fails after 5 retries it should return following
        return {"statusCode": 408,
                "error_message": "Request timeout, failed to reach host"}


def tequipment(pdp_url, sku, vendor='tequipment'):
    url = pdp_url
    try:
        if 'www.tequipment.net' not in url:
            # The function should return a dictionary having statusCode: 404;
            # If url provided does not belong to the respective store or if url is not a product url
            return {"statusCode": 404,
                    "error_message": "Product not found"}

        # dictionary for final output :-
        product_dict = dict()
        product_dict['pdp_url'] = url
        product_id_url = product_dict['pdp_url']
        product_dict['vendor'] = vendor

        # main Requests :-

        response_text = zyte_requests(product_id_url)
        response_status = response_text[1]
        if response_status == 200:
            response = Selector(response_text[0])

        if response_status == 404:
            return {"statusCode": 404,
                    "error_message": "Product not found"}

        if "?bearer_token" not in response_text[0]:
            # sku :-
            scraped_sku = re.sub(r'\s+', ' ',
                         response.xpath('//span[@class="catalog-number"]//text()').get('').split(':')[-1]
                         ).strip()
            product_dict['sku'] = scraped_sku

            # mpn :-
            mpn = re.sub(r'\s+', ' ',
                         response.xpath('//span[@class="model-number"]//text()').get('')
                         ).split(":")[-1].strip()

            if not product_dict['sku']:
                product_dict['sku'] = mpn

            if product_dict['sku'] != sku :
                return {"statusCode": 404,
                        "error_message": f"Scraped SKU:{product_dict['sku']} does not match input SKU:{sku}"}

            if 'Discontinued' in response_text[0]:
                return {"statusCode": 410,
                        "error_message": "Discontinued Product"}

            try:
                available_to_checkout = (response.xpath('//span[@class="priceButtonText"]//text()').get()).lower()
                product_dict['available_to_checkout'] = True if available_to_checkout == 'add to cart' else False
            except:
                product_dict['available_to_checkout'] = False

            # Instock request and code :-
            list_item = response.xpath('//div[@class="stockText bold text-md"]/span/@item').get()

            data = {
                'F': 'GetStocks',
                'sidcor': 'HzaQ1JYwwMKz4yrndYVMs0K3TIEv+meLPz/A8AnkvtI=',
                'Items': str(list_item),
            }

            # Second requests :-
            max_retires = 5
            for i in range(max_retires):
                response_data = requests.post('http://origin-www.tequipment.net/ajax/store/ajaxssf.aspx',
                                              data=data)
                if response_data.status_code == 200:
                    break
                if response_data.status_code == 404:
                    return {"statusCode": 404,
                            "error_message": "Product not found"}
            else:
                # The function must have logic for retries Max. 5
                # If request fails after 5 retries it should return following
                return {"statusCode": 408,
                        "error_message": "Request timeout, failed to reach host"}

            try:
                instock = int(json.loads(response_data.text)['StockObjs'][0]['Stock'])
            except:
                instock = 0

            if instock >= 1:
                product_dict['in_stock'] = True
            elif instock == 0:
                product_dict['in_stock'] = False
            else:
                product_dict['in_stock'] = False

            product_dict['lead_time'] = None

            price_list = list()
            pricing = dict()
            pricing['min_qty'] = 1
            price_con = False
            if "Chat with us for price" and "Call Us" in response_text[0]:
                if response.xpath('//p[contains(text(), "Your Price: ")]//span/@content'):
                    pricing['price'] = float(response.xpath('//p[contains(text(), "Your Price: ")]//span/@content')
                                             .get('').replace(',', '').replace('$', ''))
                    pricing['currency'] = 'USD'
                else:
                    pricing['price_string'] = "Call For Price"
                price_con = True
            else:
                price = response.xpath('//span[@class="sale"]/@content').get('').strip()
                if price == '':
                    price = response.xpath('//div[@class="listPrice"]/span/@data-price').get('').strip()
                    if price != '':
                        pricing['price'] = float(price.replace('$', '').replace(',', ''))
                        pricing['currency'] = 'USD'
                    elif price == '':
                        price = response.xpath('//div[@class="itemPrice text-secondary"]/span//text()').get(
                            '').replace('$', '')
                        if price != '':
                            pricing['price'] = float(price.replace('$', '').replace(',', ''))
                            pricing['currency'] = 'USD'
                        else:
                            if '$' not in response.xpath('//div[@class="col-md-5"]//text()').get(''):
                                price = response.xpath('//script[@type="application/ld+json"]//text()').get('')
                                price_json = json.loads(price)
                                price = price_json['offers']['price']
                                if price != '' and price != 0:
                                    pricing['price'] = float(price.replace('$', '').replace(',', ''))
                                    pricing['currency'] = 'USD'
                                else:
                                    pricing['price_string'] = "Call For Price"
                            else:
                                pricing['price_string'] = "Call For Price"

                else:
                    pricing['price'] = float(price.replace('$', '').replace(',', ''))
                    pricing['currency'] = 'USD'
            # if price 0 then Call For Price will go :-
            if pricing:
                for key in pricing:
                    if 'price' == key:
                        if pricing[key] == 0:
                            del pricing[key]
                            del pricing['currency']
                            pricing['price_string'] = "Call For Price"

            if pricing:
                price_list.append(pricing)
                product_dict['price'] = price_list
            else:
                product_dict['price'] = None

            return {"statusCode": 200, "data": product_dict}

        else:

            try:
                mpn = re.sub(r'\s+', ' ', response.xpath('//span[@class="model-number"]//text()').get('')).split(":")[-1].strip()
            except Exception as e:
                mpn = None

            # Item Id :-
            item_lis_id = re.sub("\s+", " ",response.xpath('//script[contains(text(),"item_id")]//text()').get()).strip()

            re_item = re.findall('"item_id":"(.*?)"', item_lis_id)[0]

            max_retires = 5
            for i in range(max_retires):
                response_id = requests.get(
                    f'https://admin-fts.threekit.com/api/catalog/products?bearer_token=cc5be84c-4d2a-47f7-9074-7e32a570234f&metadata={{%22ItemId%22:%22{re_item}%22}}&orgId=fd92acd5-7ef7-439e-a4d1-0f302488214b', )
                if response_id.status_code == 200:
                    break
                if response_id.status_code == 404:
                    return {"statusCode": 404,
                            "error_message": "Product not found"}
            else:
                # The function must have logic for retries Max. 5
                # If request fails after 5 retries it should return following
                return {"statusCode": 408,
                        "error_message": "Request timeout, failed to reach host"}

            dictionary_id = json.loads(response_id.text)["products"][0]["id"]

            if dictionary_id:
                max_retires = 5
                for i in range(max_retires):
                    response_json = requests.get(
                        url=f"https://admin-fts.threekit.com/api/cas/{dictionary_id}?branch=main&orgId=fd92acd5-7ef7-439e-a4d1-0f302488214b&type=Node&bearer_token=cc5be84c-4d2a-47f7-9074-7e32a570234f"
                    )
                    if response_json.status_code == 200:
                        break
                    if response_json.status_code == 404:
                        return {"statusCode": 404,
                                "error_message": "Product not found"}
                else:
                    # The function must have logic for retries Max. 5
                    # If request fails after 5 retries it should return following
                    return {"statusCode": 408,
                            "error_message": "Request timeout, failed to reach host"}


                dictionary = json.loads(response_json.text)

                product = []
                global_id = []
                Table_id = ""
                item_id = int()

                for i in dictionary["objects"]:
                    if "id" in dictionary["objects"][i]:
                        if "Global" in dictionary["objects"][i]:
                            global_id.append(json.loads(dictionary["objects"][i])["id"])
                        if "TableId" in dictionary["objects"][i]:
                            Table_id = json.loads(dictionary["objects"][i])["defaultValue"]
                        if "SKU" not in dictionary["objects"][i] and "TableId" not in dictionary["objects"][
                            i] and "Global" not in \
                                dictionary["objects"][i]:
                            if "AEItemId" in dictionary["objects"][i]:
                                item_id = json.loads(dictionary["objects"][i])["defaultValue"]
                            elif "Description" in dictionary["objects"][i]:
                                Description = json.loads(dictionary["objects"][i])["defaultValue"]
                            elif "ItemId" not in dictionary["objects"][i] and "createdBy" not in \
                                    dictionary["objects"][i]:
                                try:
                                    dic = {'name': json.loads(dictionary["objects"][i])["name"],
                                           'value': json.loads(dictionary["objects"][i])["values"]}
                                    product.append(dic)
                                except:
                                    pass

                if product == []:
                    # Product Get From Global_id :-
                    for id in global_id:
                        max_retires = 5
                        for i in range(max_retires):
                            response_json = requests.get(
                                url=f"https://admin-fts.threekit.com/api/cas/{id}?branch=main&orgId=fd92acd5-7ef7-439e-a4d1-0f302488214b&type=Node&bearer_token=cc5be84c-4d2a-47f7-9074-7e32a570234f"
                            )
                            if response_json.status_code == 200:
                                break
                            if response_json.status_code == 404:
                                return {"statusCode": 404,
                                        "error_message": "Product not found"}
                        else:
                            # The function must have logic for retries Max. 5
                            # If request fails after 5 retries it should return following
                            return {"statusCode": 408,
                                    "error_message": "Request timeout, failed to reach host"}

                        dictionary = json.loads(response_json.text)
                        for i in dictionary["objects"]:
                            if "id" in dictionary["objects"][i]:
                                if "SKU" not in dictionary["objects"][i] and "TableId" not in \
                                        dictionary["objects"][
                                            i] and "Global" not in \
                                        dictionary["objects"][i]:

                                    if "AEItemId" in dictionary["objects"][i]:
                                        item_id = json.loads(dictionary["objects"][i])["defaultValue"]
                                    elif "Description" in dictionary["objects"][i]:
                                        Description = json.loads(dictionary["objects"][i])["defaultValue"]
                                    elif "ItemId" not in dictionary["objects"][i] and "createdBy" not in \
                                            dictionary["objects"][i]:
                                        try:
                                            dic = {'name': json.loads(dictionary["objects"][i])["name"],
                                                   'value': json.loads(dictionary["objects"][i])["values"]}
                                            product.append(dic)
                                        except:
                                            pass

                main_dictionary = dict()
                url_query = ""
                for i in dictionary["objects"]:
                    if "tableQuery" in dictionary["objects"][i]:
                        if len(json.loads(dictionary["objects"][i])["tableQuery"]["conditions"]) > 1:
                            url_query = json.loads(dictionary["objects"][i])["tableQuery"]["conditions"]

                url_dict = dict()
                for i in url_query:
                    i.pop('attributeId')
                    i['value'] = ""
                    url_dict[i['column']] = i

                if url_dict == {}:

                    max_retires = 5
                    for i in range(max_retires):
                        url_dict_link = f'https://admin-fts.threekit.com/api/cas/{id}?branch=main&orgId=fd92acd5-7ef7-439e-a4d1-0f302488214b&type=Attribute&bearer_token=cc5be84c-4d2a-47f7-9074-7e32a570234f'
                        url_dict_response = requests.get(url=url_dict_link)
                        if url_dict_response.status_code == 200:
                            break
                        if url_dict_response.status_code == 404:
                            return {"statusCode": 404,
                                    "error_message": "Product not found"}
                    else:
                        # The function must have logic for retries Max. 5
                        # If request fails after 5 retries it should return following
                        return {"statusCode": 408,
                                "error_message": "Request timeout, failed to reach host"}


                combinations = list(itertools.product(*[d['value'] for d in product]))

                if url_dict == {}:
                    for i in product:
                        main_dictionary[i["name"]] = {"column": i["name"], "comparator": "=", "value": ""}

                sku_list = []
                count = 0
                urls_list = list()
                for combo in combinations:

                    main_dictionary["AEItemId"] = {"column": "AEItemId", "comparator": "=", "value": item_id}

                    if url_dict == {}:
                        count = 0
                        for index, j in enumerate(main_dictionary):
                            if 'AEItemId' != j:
                                main_dictionary[j]['value'] = combo[count]
                                count += 1
                        where_data = json.dumps(main_dictionary, ensure_ascii=False).replace('": "', '":"').replace('", "',
                                                                                                                '","')
                    else:
                        count = 0
                        for index, j in enumerate(url_dict):
                            if 'AEItemId' != j:
                                url_dict[j]['value'] = combo[count]
                                count += 1
                            else:
                                url_dict[j]['value'] = item_id
                        where_data = json.dumps(url_dict, ensure_ascii=False).replace('": "', '":"').replace('", "',
                                                                                                                '","')



                    base_url = f"https://admin-fts.threekit.com/api/datatables/{Table_id}/row"

                    query_params = {
                        "branch": "main",
                        "orgId": "fd92acd5-7ef7-439e-a4d1-0f302488214b",
                        "where": where_data,
                        "bearer_token": "cc5be84c-4d2a-47f7-9074-7e32a570234f"
                    }

                    where_param = urllib.parse.quote(str(where_data), safe='')

                    # Construct the URL
                    url = f"{base_url}?branch={query_params['branch']}&orgId={query_params['orgId']}&where={where_param}&bearer_token={query_params['bearer_token']}"

                    urls_list.append(url)

                results = fetch_all_urls(urls_list)

                for status_code, url, response_text in results:
                    if json.loads(response_text)["value"]["SKU"].replace(' ', '') == sku.replace(' ', ''):
                        scraped_sku = json.loads(response_text)["value"]["SKU"]

                        data = {
                            'F': 'GetThreekitItemInfo',
                            'SKU': f'{scraped_sku}',
                            'ItemId': f'{item_id}'
                        }

                        headers = {
                            'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'Accept-Language': 'en-US,en;q=0.9',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://www.tequipment.net',
                            'Referer': 'https://www.tequipment.net/',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-site',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                        }

                        max_retires = 5
                        for i in range(max_retires):
                            response_data = requests.post('https://www.tequipment.net/ajax/store/getcontrol.aspx',
                                headers=headers, data=data)
                            if response_data.status_code == 200:
                                break
                            if response_data.status_code == 404:
                                return {"statusCode": 404,
                                        "error_message": "Product not found"}
                        else:
                            # The function must have logic for retries Max. 5
                            # If request fails after 5 retries it should return following
                            return {"statusCode": 408,
                                    "error_message": "Request timeout, failed to reach host"}

                        product_data = json.loads(response_data.text)

                        if product_data:
                            product_data_sku = product_data['Model']
                            print(product_data_sku)
                            if sku == product_data_sku:
                                # EXTRACTING PRODUCT DETAILS
                                product_dict['sku'] = product_data_sku

                                try:
                                    IsDiscontinued = product_data['IsDiscontinued']

                                    product_dict['available_to_checkout'] = True if IsDiscontinued == False else False
                                except:
                                    product_dict['available_to_checkout'] = False

                                StockCount = product_data['StockCount']

                                if StockCount >= 1:
                                    product_dict['in_stock'] = True
                                else:
                                    product_dict['in_stock'] = False

                                price_list = list()
                                pricing = dict()
                                pricing['min_qty'] = 1
                                price = product_data['Price']

                                if price and float(price) != 0:
                                    pricing['price'] = float(price.replace('$', '').replace(',', ''))
                                    pricing['currency'] = 'USD'
                                else:
                                    pricing['price_string'] = 'Call For Price'
                                    product_dict['available_to_checkout'] = False

                                price_list.append(pricing)

                                product_dict['price'] = price_list

                                product_dict['lead_time'] = None

                                return {"statusCode": 200, "data": product_dict}

                            else:
                                continue

    except Exception as e:
        # The function should return a dictionary having statusCode: 500;
        # If any internal error occurs. i.e If any Exception is caught inside try-except.
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}

#
# if __name__ == '__main__':
#
#     event = {
#         "sku": "OC White 42400-4-CM",
#         "vendor": "tequipment",
#         "pdp_url": "https://www.tequipment.net/OC-White/Green-Lite-6in-Round/Magnifiers/"
#     }
#
#     print(tequipment(pdp_url=event['pdp_url'], sku=event['sku'], vendor=event['vendor']))

