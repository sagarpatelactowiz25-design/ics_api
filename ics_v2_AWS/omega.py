import json

import requests
from parsel import Selector
import re


def parse_price(value):
    value = re.sub('<[^<]+?>', '', value)
    try:
        return float(value.strip())
    except ValueError:
        return None


def extract_pricing(response_text):
    item_price = []
    if 'Volume discounts available' in response_text:
        selector = Selector(text=response_text)
        for tr in selector.xpath('//table[@class="volume__prices"]//tr[./td]'):
            all_td = [i.strip() for i in tr.xpath(".//td//text()").getall() if i.strip()]
            min_qty = int(re.findall("\d+", all_td[0])[0])
            price = all_td[1]
            # print("Price after parsing:", price)  # Add this line
            if price is not None:
                price = price.strip().replace('$', '').replace(',', '').strip()  # Remove commas
                price_float = parse_price(price)
                item_price.append({

                    'min_qty': min_qty,
                    'price': price_float,
                    'currency': 'USD'
                })
            else:
                item_price.append({
                    'min_qty': min_qty,
                    'price_string': "Call for price"
                })
    else:
        selector = Selector(text=response_text)
        pricing_rows = selector.xpath(
            '//input[@name="variantPriceValue" and @value!=""]/@value | //div[@class="price-panel-variants js-content-hide-on-invalid"]//strong[normalize-space()]').extract()
        min_qty = selector.xpath('//input[@name="pdpAddtoCartInput"]/@data-min').extract_first()
        min_qty = int(min_qty) if min_qty else None
        if pricing_rows:
            price_string = pricing_rows[0].strip()
            # Extract numerical value from the string
            price_match = re.search(r'[\d,]+\.?\d*', price_string)
            if price_match:
                price = price_match.group().replace(',', '')  # Remove commas
                price_float = float(price)
            item_price.append({

                'min_qty': min_qty,
                'price': price_float,
                'currency': 'USD',
            })
        else:
            item_price.append({
                'min_qty': min_qty,
                'price_string': "Call for price"
            })
    return item_price


def omega(pdp_url, sku='sku'):
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
    if 'class="sku-number"' not in url_request.text:
        error['statusCode'] = 410
        error['error_message'] = 'Product not found'
        return error

    response_text = url_request.text
    # print(response_text)
    # 'class="discontinued"' in response_text or
    if 'temporary hold' in response_text:
        return {"statusCode": 410,
                "error_message": "Product is discontinued"}
    else:
        selector = Selector(text=response_text)
        item = dict()
        # Vendor Extracting :-
        item['vendor'] = 'omega'
        # Sku Extracting :-
        try:
            scrapped_sku = "".join(selector.xpath('//span[@itemprop="sku"]/text()').get(''))
            if scrapped_sku != sku:
                error['statusCode'] = 410
                error['error_message'] = f"Scraped SKU:{scrapped_sku} does not match input SKU:{sku}"
                return error

        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = "Internal server error" + str(e)
            return error

        # Pdp_url Extracting :-
        item['sku'] = sku
        item['pdp_url'] = pdp_url
        # if 'discontinued' in response_text:
        #     item['price'] = [{'min_qty': 1, 'price_string': 'Call for price'}]
        #     item['lead_time'] = None
        #     item['available_to_checkout'] = False
        #     item['in_stock'] = False
        #     return {'statusCode': 200,
        #             'data': item}
        # else:
        item['price'] = extract_pricing(response_text)
        # Lead_time Extracting :-
        lead_time = None
        lead_time_text = "".join(
            selector.xpath('//div[@class="lead-time js-content-hide-on-invalid"]//text()').getall()).strip()
        if lead_time_text is None:
            lead_time_text = []
        if lead_time_text == 'Limited Stock':
            lead_time_text = []
        if "Lead Time" in lead_time_text:
            lead_time_text = lead_time_text.replace('Lead Time (If not in stock):',
                                                    'If not in stock:')
            lead_time = [{
                'min_qty': 1,
                'time_to_ship': {
                    'raw_value': lead_time_text
                }
            }]
        item['lead_time'] = lead_time

        # Available_to_checkout Extracting :-
        check_out = selector.xpath('//div[@class="AddToCart-AddToCartAction"]//button/text()').get()
        try:
            check_out = check_out.strip()
            if check_out == "Add to cart":
                item['available_to_checkout'] = True
            else:
                item['available_to_checkout'] = False
        except:
            item['available_to_checkout'] = False

        # In_stock Extracting :-

        cookies = {
            '_gcl_au': '1.1.825910564.1740041681',
            '_ga': 'GA1.1.826065655.1740041682',
            'hubspotutk': 'ccbcf2b5882be8affbf960e0f6be498d',
            '__hssrc': '1',
            '_zitok': '84d3f24330d52e5f25281740041684',
            'JSESSIONID': 'Y7-62544cc2-171a-475d-bbde-c263dfd07645.accstorefront-574b9b8bbb-7n8lb',
            'ROUTE': '.accstorefront-574b9b8bbb-7n8lb',
            '__hstc': '55502388.ccbcf2b5882be8affbf960e0f6be498d.1740041683485.1740041683485.1740114506838.2',
            'AKA_A2': 'A',
            'QSI_SI_78yiBGcFdTaLkDb_intercept': 'true',
            '_br_uid_2': 'uid%3D2669982892951%3Av%3D15.0%3Ats%3D1740041682506%3Ahc%3D24',
            '_uetsid': '52d5e600ef6811efbc5c7114de5f6d81',
            '_uetvid': '52d62090ef6811efb45b65ee25b3e9e8',
            '__hssc': '55502388.17.1740114506838',
            'fs_uid': '#JG4SA#9d528312-4874-4022-8332-e61b7c72f660:439efb13-6a25-4541-b952-45970601eddf:1740114507411::17#/1771577733',
            'QSI_HistorySession': 'https%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2F~1740041684085%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2F0-260-in-bore-diameter-threaded-heavy-duty-thermowells%2FSERIES-260H%2Fp%2F1-260H-U101-2-CS~1740041735626%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Ftemperature%2Fc%2Ftemperature-wire-cable~1740041870590%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Fcopper-extension-wire-for-rtd-and-thermistor%2Fp%2FEXGG-2CU-3CU-WIRE~1740041876195%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Fcoming-soon~1740041889454%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Ferror~1740041902494%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2F~1740114507444%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Fadvanced-digital-pressure-gauge-with-data-logging%2FDPG280%2Fp%2FDPG280-10-0KG~1740114531301%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Fadvanced-digital-pressure-gauge-with-data-logging%2FDPG280%2Fp%2FDPG280-005G~1740114585835%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Fdigital-pressure-gauge-with-rugged-housing%2Fp%2FDPG110-120~1740115508223%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Fdigital-pressure-gauge-with-rugged-housing%2FDPG110-120%2Fp%2FDPG120~1740115787871%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2F~1740116521017%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Ftemperature%2Fc%2Fthermowells-protection-heads-tubes~1740116533364%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Ftemperature%2Fthermowells-protection-heads-tubes%2Fc%2Fthermowells~1740116539232%7Chttps%3A%2F%2Fwww.dwyeromega.com%2Fen-us%2Fdigital-pressure-gauge-with-rugged-housing%2Fp%2FDPG110-120%3Fview%3Dlist%26dest%3Dallmodels~1740116867600',
            'fs_lua': '1.1740117309812',
            '_ga_WQRLLHBF43': 'GS1.1.1740114504.3.1.1740117519.60.0.0',
        }
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://www.dwyeromega.com/en-us/digital-pressure-gauge-with-rugged-housing/DPG110-120/p/DPG110',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',

        }
        sku_ = scrapped_sku.replace('/', '-').replace('_', '-').replace('.', '-').replace(' ', '-')

        response_1 = requests.get(f'https://www.dwyeromega.com/en-us/p/{sku_}/stock', cookies=cookies, headers=headers)

        json_data = response_1.json()
        stock_level = json_data.get('stockLevel', 0)
        if stock_level > 0:
            item['in_stock'] = True
        else:
            item['in_stock'] = False

        if 'discontinued' in response_text:
            item_price = extract_pricing(response_text)
            if item_price and not any('Call for price' in price.get('price_string', '') for price in item_price):
                return {'statusCode': 200,
                        'data': item}
            else:
                return {"statusCode": 410, "error_message": "Product is discontinued"}

        if 'statusCode' in item.keys():
            if item['statusCode'] == 500:
                return item
            elif item['statusCode'] == 410:
                return item
        else:
            return {'statusCode': 200,
                    'data': item}

# if __name__ == '__main__':
#     # parse function call with products_url and sku :-
#     event = {"sku": "GW-001-3-NA", "vendor": "omega", "pdp_url": "https://www.dwyeromega.com/en-us/omega-link-long-range-wireless-modbus-iiot-ethernet-gateways/GW-001-Series/p/GW-001-3-NA"}
# 
# 
#     print(json.dumps(omega(pdp_url=event['pdp_url'], sku=event['sku'])))

