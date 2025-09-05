import time
import json
import re
import requests
import urllib.parse
def meetoptics(pdp_url, sku):
    error_ = dict()
    url_request = str()
    max_retires = 5
    try:
        for i in range(max_retires):
            start_time = time.time()
            after_s = pdp_url.split("/s/")[-1]
            after_s = after_s.split("/")
            after_s[0] = re.sub(r"-", r"", after_s[0])
            # sku code-------------------------
            encd = urllib.parse.unquote(after_s[-1])
            sku_demo = re.sub(r"^#+","",sku)
            if sku_demo != encd:
                after_s[-1] = encd
            elif sku_demo == encd:
                after_s[-1] = sku    
            # sku code end----------------------
            after_s = "/".join(after_s)
            modified_url = re.sub(r"/p/", r"/~/", after_s)
            modified_url = urllib.parse.quote(modified_url)
            modified_url = re.sub("/~/","%252F%7E%252F",modified_url)
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'origin': 'https://www.meetoptics.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://www.meetoptics.com/',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'x-aws-waf-token': '58d30b9d-932b-4d9a-9616-7431ec8da218:BQoAfsYGi70LAAAA:b5ceDmlfuBVoN78AnILu/x/j4N/hsA4dmSlMyieQEeJWw/bYsCSOFUkP2uMcJkRB8e91B+9xJrCBraUABS7pSfxMw5T3+Hbiz1GpzgCaU7chttE4dFqoRiToNKkYXNN+z6/KM4fxH1Cc94YIKLXHPkzd0qYbnjpUzZWU3+ejMKWZ0ifTddvzodz839Mf7ywTKmP7zVvSs+zuqCoYdP8Yq1bqZ00qoxHrxsg6IrkQCY2ykmTCn7k828FHLHAGJNhaRBwxanQ=',
            }

            json_data = {
                    'code': [
                        f'{modified_url}',
                    ],
                }
            url_request = requests.get(f'https://search-v3.meetoptics.com/products?code={modified_url}', headers=headers)
            # url_request = requests.post(f'https://search-v3.meetoptics.com/products?code={modified_url}', headers=headers, json=json_data)

            if url_request.status_code == 200:
                break
        if url_request.status_code == 200:
            pass

        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}

        response = json.loads(url_request.text)

        # define dictionary for making data dictionary :-
        item = dict()

        # vendor Extracting :-
        item['vendor'] = 'meetoptics'
        # sku Extracting :
        try:
            try:
                item['sku'] = response['docs'][0]['product']['code_supplier']

            except:
                item['sku'] =None

            if item['sku'] != sku:
                error_['statusCode'] = 404
                error_['error_message'] = f"Scraped SKU does not match input SKU:{sku}"
                return error_

        except Exception as e:
            error_['statusCode'] = 500
            error_['error_message'] = str(e)
            return error_

        # pdp_url Extracting :-
        item['pdp_url'] = pdp_url

        item_price = dict()
        item_price['min_qty'] = 1
        try:
            price_main = response['docs'][0]['product']['Price__u_USD']
            if price_main:
                item_price['price'] = float(price_main)
                item_price['currency']='USD'
            else:
                item_price['price_string'] = 'Call For Price'
        except Exception as e:
            print(e)
            item_price['price_string'] = 'Call For Price'

        price_list = list()
        price_list.append(item_price)
        item['price'] = price_list

        # available_to_checkout and in_stock Extracting :-
        in_Stock = response['docs'][0]['product']['Availability__r_US']
        if in_Stock == "In stock":
            item['in_stock'] = True
        else:
            item['in_stock'] = False

        item['available_to_checkout'] = True
        item['lead_time'] = None
        end_time = time.time()
        print("Execution time :", end_time - start_time)
        return {'statusCode': 200,
                'data': item}
    except Exception as e:
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}

if __name__ == '__main__':
    event = {
        "pdp_url": "https://www.meetoptics.com/fiber-optics/fiber-optomechanics/bare-fiber-optic-holder/s/siskiyou/p/31040000E",
        "sku": "31040000E",
        "vendor": "meetoptics"}
    print(json.dumps(meetoptics(pdp_url=event['pdp_url'], sku=event['sku'])))