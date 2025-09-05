import json
import random
import time
from datetime import datetime, timedelta
from curl_cffi import requests

proxies = {
  "http": "http://scraperapi:64a773e99ca0093e4f80e217a71f821b@proxy-server.scraperapi.com:8001"
  # "http": "http://scraperapi.country_code=us:64a773e99ca0093e4f80e217a71f821b@proxy-server.scraperapi.com:8001"
}

def parse(response, keyword, sku):
    try:
        html_content = response.text
        data_dict = json.loads(html_content)
        pro_part = data_dict['productId']
        data = dict()
        data['vendor'] = 'lowes'
        try:
            data['sku'] = data_dict['productDetails'][pro_part]['product']['itemNumber']
        except:
            data['sku'] = None

        if str(sku) != data['sku']:
            return {"statusCode": 404,
                    "error_message": f"Scraped SKU:{data['sku']} does not match input SKU:{sku}"}

        data['pdp_url'] = keyword
        try:
            price_ = data_dict['productDetails'][pro_part]['location']['price']['pricingDataList'][0]['finalPrice']
            price_list=[]
            price_text={
                "min_qty": 1,
                "price": float(price_),
                "currency": "USD",
            }
            price_list.append(price_text)
            data['price'] = price_list
        except Exception as e:
            price_list = list()
            price_text = {
                "min_qty": 1,
                "price_string": "Call For Price",

            }
            price_list.append(price_text)
            data['price'] = price_list

        if data_dict.get("productDetails").get(pro_part).get("itemInventory").get("totalAvailableQty"):
            data['available_to_checkout'] = True
            data['in_stock'] = True
        else:
            data['available_to_checkout'] = False
            data['in_stock'] = False

        leads = None
        estimated_lead_time = []

        try:
            if data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][1].get('itmLdDateTm'):
                leads = data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][1]['itmLdDateTm']
            elif data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][1].get('itmLdTm'):
                leads = data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][1]['itmLdTm']

            elif data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][1].get('fullPath'):
                try:
                    if data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][1]['fullPath'][0]['shipDateTime']:
                        leads = data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][1]['fullPath'][0]['shipDateTime']
                except (KeyError, IndexError):
                    pass

            elif data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][2].get('itmConsolidationDate'):
                leads = data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][2]['itmConsolidationDate']

            # else:
            #     lead_time_path = data_dict['productDetails'][pro_part]['location']['itemInventory']['itemAvailList'][0]['fullPath'][0]['parcelDates']
            #     for i in lead_time_path:
            #         if i.get('carrierType') in {'STANDARD', 'BASIC'}:
            #             leads = i.get('promiseDate')
            #             break

            if leads:
                try:
                    input_date = datetime.strptime(leads, "%Y-%m-%d")
                except ValueError:
                    try:
                        input_date = datetime.strptime(leads, "%m-%d-%Y-%H:%M %Z")
                    except ValueError:
                        try:
                            input_date = datetime.strptime(leads, "%Y-%m-%dT%H:%M%z")
                        except ValueError:
                            input_date = datetime.strptime(leads, "%Y-%m-%dT%H:%M:%S%z")

                today_date = datetime.today().strftime("%Y-%m-%d")

                if today_date == input_date.strftime("%Y-%m-%d"):
                    output_date_str = "As soon as Today"
                else:
                    output_date_str = f"As soon as {input_date.strftime('%a')}, {input_date.strftime('%b')} {input_date.day}"

                estimated_lead_time.append(
                    {
                        "min_qty": 1,
                        "time_to_arrive": {
                            "raw_value": output_date_str
                        }
                    }
                )

                data['lead_time'] = estimated_lead_time
            else:
                data['lead_time'] = None

        except (KeyError, IndexError, ValueError) as e:
            print(f"Error: {e}")
            data['lead_time'] = None

        # return json output :-
        # The function should return a dictionary having statusCode: 200;
        # If all above given headers are scraped properly
        return {"statusCode": 200, "data": data}

    except Exception as e:
        # The function should return a dictionary having statusCode: 500;
        # If any internal error occurs. i.e If any Exception is caught inside try-except.
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}

def lowes(pdp_url, sku):

    if '//www.lowes.com/pd/' not in pdp_url:
        return {"statusCode": 404,
                "error_message": f"Product Not Found"}

    try:
        request_id = pdp_url.split('/')[-1]
    except Exception as e:
        request_id = ''

    try:
        max_retires = 5
        for i in range(max_retires):
            try:
                timings = [0.5, 1, 1.5, 2]
                browsers = ['edge101', 'edge99', 'chrome99', 'chrome101',]
                cookies = {
                    '_fbp': 'fb.1.1723124700986.60403275754779713',
                    'dbidv2': 'a0593143-6d25-47b2-b17a-667fe16cc676',
                    'EPID': 'a0593143-6d25-47b2-b17a-667fe16cc676',
                    'region': 'east',
                    'ph_aid': '1d58552d-94d0-4094-3600-d95bb2377e39-7536daab5f935-4d4e0e0febc2d-6e0fedfde9565',
                    'g_amcv_refreshed': '1',
                    'AMCV_5E00123F5245B2780A490D45%40AdobeOrg': '-1303530583%7CMCIDTS%7C20674%7CMCMID%7C14185120640697670470907859922131089360%7CMCAAMLH-1723729505%7C7%7CMCAAMB-1723729505%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1723131905s%7CNONE%7CvVersion%7C3.3.0',
                    'purchase-test-promoprice-sfl': 'abt-12639a',
                    'services-test-atc-cart-noplan': 'abt12754b',
                    'salsify_session_id': 'b4b37592-bb85-4e03-93f4-3cce7b85d4f8',
                    'sn': '1883',
                    'sd': "%7B%22id%22%3A%221883%22%2C%22zip%22%3A%2214228%22%2C%22city%22%3A%22Amherst%22%2C%22state%22%3A%22NY%22%2C%22name%22%3A%22W.%20Amherst%20Lowe's%22%2C%22region%22%3A%2218%22%7D",
                    'audience': 'DIY',
                    'zipcode': '04769',
                    'nearbyid': '2209',
                    'zipstate': 'ME',
                    '_gcl_au': '1.1.226820782.1723124717',
                    'ndp_session_id': 'b9d06714-31d9-4fdc-9f12-42128eff17c9',
                    '_tt_enable_cookie': '1',
                    '_ttp': 'bKMSfbaA7yPXeXfVFWm-zkGVIky',
                    'mdLogger': 'false',
                    'kampyle_userid': '7894-0c4d-09c5-388d-53ae-398d-ed0b-ded7',
                    '_pin_unauth': 'dWlkPU1qWmhOVGs1WVRRdE1XRmxPQzAwTldRMExXRXdOMkl0T0RrNE5qYzNPREUwWXpjMQ',
                    'BVBRANDID': 'e641f16d-c42c-4cf7-b60e-42a1b3f9cc42',
                    'al_sess': 'FuA4EWsuT07UWryyq/3foIStLyo+I6ML6wPhVrtX7uNEyQUZvgescPYwAnw9+kbb',
                    '_abck': 'A3CE07F497B7F6374416C2C02656F3D0~0~YAAQ6MgwF7bmUDWRAQAA+KaANQwXjV7YDTx8GOeP+4RX73N01ewLjFkocJSR4cwDKv1TMec4oJuiFRiHdbS66CRvKvQoSS55XbqIDWzlafMhuRO3yjUa+fzQDuxc1zSYwPCcbzmzpgGFdTrwv05p1/9vKKmcSRODpqtPN4TZAbm1d2oTDSuhRoHIbBMEIgo3fBs1ZpgUJrhNJAsHk2zWR85TkkOX0CzPV37NYRmJc7CVLEBDHL8tiSz4FwIg28Ic5q3W9LOWkznsFkDgSi75M+vfVKsBUL8qJ6WpogrnmD8vJDYpsTlXIrPB3yv4lijH3KH2gB7yTKEuDLMsZDjv/zTHNrgNhs7asAlLUYdGBy3Zv8Jb5o+sFEXd89J2JaXQzwu1/rmF37iAm+CGiszuZ62UR9TxcMbwyNYaq4hN3oeU/NY8QFSMtjAYzPrDeMUgmQnWK2D8VJ0=~-1~-1~-1',
                    'AMCVS_5E00123F5245B2780A490D45%40AdobeOrg': '1',
                    'IR_gbd': 'lowes.com',
                    'seo-partner': 'gDTMXB9g7l46qsQ3gCM3qCMsoDgSmXpC',
                    '_lgsid': '1723186309675',
                    'bm_mi': '6FB722CAD684F76728F13EECC8729112~YAAQ7cgwF3i0yzSRAQAA7B/wNRgSoGFOj0BR9qEfv421peIjBpcKwILPaZn8namN/aKUWt/LlWrxhNjKZN5dKqiVBS5GYvyosYp4o48G9cG8Ti0uowNOPSFdDAOGCnZwMxMAGBeu1w3WS3VF/1zmQ+kI4rhr3k9Us+vcb/u5TLauAIQ9v+5d5hVZ00Ek//TMt0zNQzIowHBKK1JXB/1Whp0lMktSjwa9fZtlaFxNZGxRJYKBfF7Kb0OhXO6WTXtAF/D9B/amehjdyRCm1AEvNHN0LaQvYHLMD/KFgbVFDa1iTMQsz7xc9di0ithCLTXLAwCSFKITij1vjLOUlMoAZRgRa4+PW1x2wcN6SXKNo/nzkr42Osi61fg+kC4NcAKwlnbvjRkzpk7IZwok7wpGcV09BGQF1M5JgfdBcX/BXfD9/LcN6nG6vv+rZn8sfbTLVafh9FbGsDePFcQ=~1',
                    'akaalb_prod_single': '1723276037~op=PROD_GCP_EAST_DFLT:PROD_DEFAULT_EAST|~rv=55~m=PROD_DEFAULT_EAST:0|~os=352fb8a62db4e37e16b221fb4cefd635~id=70f702a0a05aa7a3b91bb0434a1d73cd',
                    'AKA_A2': 'A',
                    'sbsd_ss': 'ab8e18ef4e',
                    'TAsessionID': 'f21b0b9f-bf23-4da8-ade0-b97e66b9d45e|NEW',
                    '__gads': 'ID=9b945c7d3100c940:T=1722939230:RT=1723190453:S=ALNI_MZSC4Zzclg_j4jWRx_eHBByCadKxA',
                    '__gpi': 'UID=00000e9fbd3bd424:T=1722939230:RT=1723190453:S=ALNI_MbSI18DlkN2LTAMOGaG8BqdANwZgA',
                    '__eoi': 'ID=3de4755326d43140:T=1722939230:RT=1723190453:S=AA-AfjbnVhpLYhiBkXPAP2IwPvvL',
                    'ecrSessionId': 'F0579734E1B457ABCBC363780E99DABD',
                    'BVBRANDSID': 'a9a57788-f887-49c1-855f-946634992f07',
                    'akavpau_cart': '1723190850~id=ea122fe4e14bd827c6a0950a40fdf190',
                    'IR_12374': '1723190550914%7C0%7C1723190550914%7C%7C',
                    'IR_PI': '4ed89796-2973-11ef-8ded-8b65d6232029%7C1723190550914',
                    'p13n': '%7B%22zipCode%22%3A%2214228%22%2C%22storeId%22%3A%221883%22%2C%22state%22%3A%22NY%22%2C%22audienceList%22%3A%5B%5D%7D',
                    'fs_lua': '1.1723190552492',
                    'fs_uid': '#Q8RZE#f3822e8d-b821-4056-bfd9-e3ca08f8c5f2:c8485b2c-5636-4457-b660-0a751df1157e:1723186316976::8#f9e75fec#/1754660750',
                    'g_previous': '%7B%22gpvPageLoadTime%22%3A%220.00%22%2C%22gpvPageScroll%22%3A%2215%7C32%7C17%7C4361%22%2C%22gpvSitesections%22%3A%22bathroom%2Cbathroom_faucets_shower_heads%2Cbathroom_sink_faucets%22%2C%22gpvSiteId%22%3A%22desktop%22%2C%22gpvPageType%22%3A%22product-display%22%7D',
                    '_rdt_uuid': '1723124699864.ea5364d7-8326-4ce8-8f3b-860a56b2482a',
                    '_uetsid': '78a22020558c11ef9f54fb080ad2ac05',
                    '_uetvid': '78a24960558c11efa79383e797afff41',
                    'kampyleUserSession': '1723190556871',
                    'kampyleUserSessionsCount': '7',
                    'kampyleSessionPageCounter': '1',
                    'kampyleUserPercentile': '24.390148893893503',
                    'akaalb_prod_dual': '1723277195~op=PROD_GCP_CTRL_DFLT:PROD_DEFAULT_CTRL|PROD_GCP_CTRL_B:PROD_CTRL_B|PROD_GCP_EAST_CTRL_C:PROD_EAST_C|PROD_GCP_EAST_CTRL_DFLT:PROD_DEFAULT_EAST|PROD_GCP_EAST_CTRL_B:PROD_EAST_B|~rv=94~m=PROD_DEFAULT_CTRL:0|PROD_CTRL_B:0|PROD_EAST_C:0|PROD_DEFAULT_EAST:0|PROD_EAST_B:0|~os=352fb8a62db4e37e16b221fb4cefd635~id=fa50f628fd4cfd0ee86c05ec677ca8f5',
                    'akavpau_default': '1723191095~id=a8312ee19807dc7dcaa83d405f2a983f',
                    'sbsd': 's7hWOhhlYx8xz4cmgTxaWzFFY6YmZZIToLqPnfbso62wxTYomWn5K/ARWDWXV8PZeWdscz3UH+18rZMlKCy2W6Ibyc4wtHj0ObsVGVG8QVRLJykdkGUrKnp3KSsG6WvFucfj4GGnO+jiNrR2AhxzbHKdabeVzdztSby4dsNHM5cuxrEa7eJ9rkNsrBasPafJg',
                    'sbsd_o': 'BE46F7E51DDF4D259FBCAB21C924B45CC725F4D1BD76C88F50C1E38602750F95~sOsAhQflLYUr8YzdfTeAesB0VF86krIL1YsXIOxwh32OVMfUYZQCqP34gpLdqnbumP8YI+8wXN4t6qhxjX59zvTLeyeiOXl2bMk+y23tkJSWf3hTevA9epOiZic7cKvPfvy+79wTGiW9kO9pPlOCCJaGZkW7WVMc+MT+kDnfwyf5phN0pqDci4U5CJ6RMH0gM6tvvhaVfL6qLhOla5WWrfLgYt1nKf78EFRqz59SxTEnIsHT1iKu00UnbA8RM0porpTXEYFlXGyZUo7iVipsTx7Axi3W3cwN9L+gP6TamM4d0+uRZ55FSQEQj2BSMYkAcHUhpJWzu5lhIycgdBdWKUrBQKXXVMq0DWAlDv45JyK0=',
                    'ak_bmsc': 'D42082A7B66AE4FC13086E4C4BE9DD86~000000000000000000000000000000~YAAQ8cgwF8x7UTSRAQAAVt0sNhjMFHNHVQInKmP+aGePuccHNtb5fOhja+Yri7fMAKzEjmStGtbzo7R1iOeGUJ/Z67h+m5EgSSi2/k/SAG3jBMxa9pV/WGcRBKbTR2/DXzF/LOlIX568Jjde6xyOgQ7BIrczplwQImPvBN1O8nA95Bu9rFPTLUn5vbaQLEEVnVy2WKzmTTXQ1aamsm4Yh4Dril3pD/Kilhx1m5x597Ezld3TurJ3WTi/9NKXakF622iLXDpyRQAZNvJ2fjesO1z8bDfZz4lI0eYJ/lp/sYCO1COj8EyO4mzTZQ4hwsgjcy2W7eJ8F+MW7VJw6mK8laiYdWS2w3Sf/MC53o+hohg3XQoLYy0jBATFfJTt6uEiVqHx70n0L8zO9cVDsR2lNg42eynEA0rkPlpNsgmJHeQqAp6YRUKMGJv3NXpK7enlNmb2iZdDbmZTTDJWwjF37LK6NjKkb9aBGkCy4i13T5TJgXpByE6HmxL5n16L+d19X8zYLl/8IeZYM9gTOI+SXjdp/LVtJvgCc1ZUTFi5qZ+kpZNjNq8fNcwZRw8RJSEveafeiIpY1cJ2pXqBrT+XQYUyCVx6kMJU91AnSfCExNQ/Y5LgaJYyG1vJOXbun8BzDH7dJP/PYso9go/EX95AP98HPD9mQwgknXXjOCmnaRDadGCzmRhVQW2KbmOHuABSMnP9liGr3796PvXVANZbIxiCejNlYC2lf6UxdWWAlj+8KecgoAzc36tnZ9kRb5jhVkjnI8k3siTs/GsqGw==',
                    'bm_sv': '892AA508C3753F9AE72D7DCD79F3090F~YAAQ8cgwF817UTSRAQAAVt0sNhjZPpCjBeoWytTsiV5ttnZn6ojV2JKLbmkbUzC2ThbiSofv46nMZSjEr0Do155rvwCWh6ViV3uLWKVhi88RJojIebNQrh1Fi61igFScfMoJpG8Ddo12MqnA/qzTk7nfA35ARVD2OoNj5RZ0uqc+a4IWHncyJtJdWhr1SfX8jTgEBTWWFTFNvG4kCb0uRIgPjHmmeSMaiyXrD/AqDY1GwAWKUrRhcGKYxJPlPqPKnQ==~1',
                    'bm_sz': '9184125A5E4D3526D45954342F312ADC~YAAQ8cgwF857UTSRAQAAVt0sNhjcp6TtV8FrtO1q8tuqmTyy7Y2nkF9mUNva2u4GhczLpxQjpEdKVTr9OAyunQofZjiNZmANL0D/FORRDTvrkyTBTTd0Lfa6eMVQC71doOg/NHHcfoGz8j5G7poxbHmW0Rvge+eJO6qycGsDmYTnAfWv5Gv5FIVpjHNM/b1vnAZqa/qMd7s0zyo2anVz3Bllii/w2p1RK4JCh02TQfXbBOYSizsdtLk9bmhmvQ7Xk6pmrkIZfIK+sLDQd/+q+vazilayZxJxJ7qrTnYIpTVVPPzGeFcTfbXEBiscnMtTdLfGWtJQvPpalBy19cTjeevBE5105SQbiACKNOTmgdZUSh+XyeMKPjIlMgcPE2mDmFDH3zmZTJLnhziFA/bPAPHus2A6LaOY+3lI6OHcR2AKjtBz6s5PraPQhHhGCQoQz6rQ4PAtMeqevbowuqAONz2ldkvgTdXsjKN0tdjtZ3KVsS2Z~3163705~4539447',
                    'RT': '"z=1&dm=lowes.com&si=d571f202-9e68-45d5-9a76-ef44b09fba76&ss=lzmdtz35&sl=9&tt=1p6z&bcn=%2F%2F68794911.akstat.io%2F&obo=1"',
                    'notice_behavior': 'implied,eu',
                }
                params = {
                    'nearByStore': '2209',
                    'zipState': 'ME',
                }
                time.sleep(random.choice(timings))
                url = f"https://www.lowes.com/wpd/{request_id}/productdetail/1883/Guest/20001"
                response = requests.get(url=url,
                                        cookies=cookies,
                                        params=params,
                                        # cookies=random.choice(cookies_list),
                                        impersonate=random.choice(browsers),
                                        # proxies=proxies
                                        )
            except:
                continue

            if response.status_code == 200:
                break
            if response.status_code == 404:
                return {"statusCode": 404,
                        "error_message": "Product not found"}
        else:
            # The function must have logic for retries Max. 5
            # If request fails after 5 retries it should return following
            return {"statusCode": 408,
                    "error_message": "Request timeout, failed to reach host"}

        if response.status_code == 200:
            final_item_dict = parse(response, pdp_url, sku)
            return final_item_dict

        else:
            data = dict()
            data['statusCode'] = 408
            data['message'] = 'Request timeout, failed to reach host'
            return data

    except Exception as e:
        # The function should return a dictionary having statusCode: 500;
        # If any internal error occurs. i.e If any Exception is caught inside try-except.
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}


# if __name__ == '__main__':
#     pdp_urls = [
#                 # "https://www.lowes.com/pd/Pfister-Masey-Brushed-Nickel-2-handle-4-in-Centerset-WaterSense-Bathroom-Sink-Faucet-with-Drain/1000244317",
#                 # "https://www.lowes.com/pd/Pfister-Masey-Polished-Chrome-2-handle-4-in-Centerset-WaterSense-Bathroom-Sink-Faucet-with-Drain/1000244329",
#                 # "https://www.lowes.com/pd/allen-roth-Duncan-2-Handle-Widespread-Lavatory-Faucet-Matte-Black/1003092546",
#                 # "https://www.lowes.com/pd/DreamLine-Alliance-Pro-BG-Matte-Black-56-in-to-60-in-x-70-375-in-Semi-frameless-Bypass-Sliding-Shower-Door/5014020721",
#                 # "https://www.lowes.com/pd/allen-roth-30-in-Oak-Undermount-Single-Sink-Bathroom-Vanity-with-White-Engineered-Stone-Top/5014599903",
#                 # "https://www.lowes.com/pd/Diamond-NOW-Kaley-60-in-White-Double-Sink-Bathroom-Vanity-with-White-Cultured-Marble-Top/5014794253",
#                 "https://www.lowes.com/pd/Delta-Modern-Matte-Black-1-handle-Single-Hole-WaterSense-Mid-arc-Bathroom-Sink-Faucet-with-Drain/5014110463",
#                 # "https://www.lowes.com/pd/Moen-Adler-Spot-Resist-Brushed-Nickel-1-Handle-Bathtub-and-Shower-Faucet-with-Valve/1000126709",
#                 # "https://www.lowes.com/pd/CALHOME-24-in-x-84-in-Colonial-Maple-2-panel-Solid-Core-Stained-Knotty-Pine-Wood-Double-Barn-Door-Hardware-Included/5014621187",
#                 # "https://www.lowes.com/pd/DEWALT-12-in-15-Amp-Dual-Bevel-Sliding-Compound-Corded-Miter-Saw/5013610507"
#                 ]
#
#     skus = [
#             # '820529',
#             # '820531',
#             # '1102764',
#             # '5272837',
#             # '5502082',
#             # '5649468',
#             '5286755',
#             # '812939',
#             # '5435987',
#             # '1097900'
#             ]
#
#
#     for pdp_url, sku in zip(pdp_urls, skus):
#         vendor = 'lowes'
#         # for _ in range(5):
#         a = lowes(pdp_url, sku)
#         print(json.dumps(a))

