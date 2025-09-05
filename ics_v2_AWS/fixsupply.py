import json
import re
import requests
from parsel import Selector
max_retires = 5
def fixsupply(pdp_url,sku):
    error_ = dict()
    url_request = str()
    max_retires = 5
    for i in range(max_retires):
        url_request = requests.get(url=pdp_url)
        if url_request.status_code == 200:
            break
    if url_request.status_code == 200:
        pass
    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}
    if 'data-ui-id="page-title-wrapper"' not in url_request.text:
        error_['statusCode'] = 410
        error_['error_message'] = 'Product not found'
        return error_

    response = Selector(url_request.text)

    # define dictionary for making data dictionary :-
    item = dict()

    # vendor Extracting :-
    item['vendor'] = 'fixsupply'
    # sku Extracting :-
    try:
        json_data = response.xpath('//script[@type="application/ld+json"]//text()').get().strip()
        load_data = json.loads(json_data)
        for key_ in load_data:
            if '@graph' in key_:
                for i in load_data[key_]:
                    if i['@type'] == 'Product':
                        item['sku'] = i['sku']
        if not item['sku']:
            item['sku'] = response.xpath('//div[@class="product attribute product-brand-number-attribute"]/span/text()').get().strip()
        if item['sku'] != sku:
            error_['statusCode'] =410
            error_['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
            return error_
    except Exception as e:
        error_['statusCode'] = 500
        error_['error_message'] = str(e)
        return error_

    # pdp_url Extracting :-
    item['pdp_url'] = pdp_url

    # Price Extracting :-
    item_price = dict()
    item_price['currency'] = 'USD'
    min_qty = re.sub('\s+', '', " ".join(response.xpath('//div[@class="qty-increment-info"]//text()').getall())).strip()
    price_list = list()
    if min_qty:
        find_min = re.findall('\d+', min_qty)
        if find_min[0].isdigit():
            min_qty = int(find_min[0])
        if isinstance(min_qty, int):
            price_xpth = response.xpath('//span[contains(@id,"product-price")]//span[@class="price"]//text()').get('').replace('$', '').replace(',', '')
            if price_xpth:
                price_ = float(price_xpth.replace(',', ''))
            if isinstance(price_, float):
                # actual_price = float(min_qty * price_)
                item_price['min_qty'] = min_qty
                item_price['price']= price_
    else:
        try:
            item_price['min_qty'] = 1
            price_float = response.xpath('//span[contains(@id,"product-price")]//span[@class="price"]//text()').get().replace('$', '').replace(',', '')
            item_price['price'] = float(price_float)
        except:
            item_price['min_qty'] = 1
            item_price['price_string'] = 'Call for price'
    multiprice= list()
    if response.xpath('//div[@class="product-info-main"]//ul[contains(@class, "prices-tier")]//li'):
        for tr in response.xpath('//div[@class="product-info-main"]//ul[contains(@class, "prices-tier")]//li'):
            secprice = dict()
            secprice['currency'] = 'USD'
            all_td = [i.strip() for i in tr.xpath(".//text()").getall() if i.strip()]
            secprice['min_qty'] = int(re.findall("\d+", all_td[0])[0])
            secprice['price'] = float(all_td[1].replace('$','').replace(',',''))
            multiprice.append(secprice)
    price_list.append(item_price)
    price_list.extend(multiprice)
    item['price'] = price_list

    # available_to_checkout and in_stock Extracting :-
    available_to_checkout = response.xpath('//button[@id="product-addtocart-button"]').get()
    if available_to_checkout == None:
        item['available_to_checkout'] = False
        item['in_stock'] = False
    else:
        item['available_to_checkout'] = True
        item['in_stock'] = True
    ship_time = response.xpath("//div[@class='expected-to-ship ']/span[contains(@class,'stock-item')]/text()").getall()
    if ship_time:
        # Check if the item is temporarily unavailable
        if ship_time != "This item is temporarily unavailable.":
            if ship_time[0]:
                if len(ship_time) == 1:
                    lead_time = [{'min_qty': 1, 'time_to_ship': {'raw_value': ship_time[0]}}]
                    estimated_lead_time = json.loads(json.dumps(lead_time))
                    item['lead_time'] = estimated_lead_time
                elif len(ship_time) == 2:
                    min_qty = ''
                    list_time = list()
                    for index, time in enumerate(ship_time):
                        min_qty = min_qty
                        if index:
                            aa = time.split('?')
                            min_qty = min_qty
                            time_ = re.sub('\s+', ' ', ". ".join(aa[1:]).strip())
                            lead_time = {'min_qty': int(min_qty), 'time_to_ship': {'raw_value': time_}}
                            list_time.append(lead_time)
                            estimated_lead_time = json.loads(json.dumps(list_time))
                        else:
                            aa = ship_time[0].split('.')
                            min_qty = 1
                            time_ = re.sub('\s+', ' ', ". ".join(aa[1:3]).strip())
                            lead_time = {'min_qty': int(min_qty), 'time_to_ship': {'raw_value': time_}}
                            list_time.append(lead_time)
                            estimated_lead_time = json.loads(json.dumps(list_time))
                            min_qty = re.sub('[A-Za-z,+\s]+', '', aa[0])
                            min_qty = int(min_qty) + 1
                        # Add estimated lead time to the product loader
                        item['lead_time'] = estimated_lead_time
                else:
                    aa = ship_time[0].split('.')
                    min_qty = re.sub('[A-Za-z,+\s]+', '', aa[0])
                    time_ = re.sub('\s+', ' ', ". ".join(aa[1:3]).strip())
                    # If not unavailable, create a lead time dictionary
                    lead_time = [{'min_qty': int(min_qty), 'time_to_ship': {'raw_value': time_}}]
                    estimated_lead_time = json.loads(json.dumps(lead_time))
                    # Add estimated lead time to the product loader
                    item['lead_time'] =  estimated_lead_time
            else:
                item['lead_time'] = None
        else:
            item['lead_time'] = None
    else:
        item['lead_time']= None

    if 'statusCode' in item.keys():
        if item['statusCode'] == 500:
            return item
        elif item['statusCode'] == 410:
            return item
    else:
        return {'statusCode': 200,
                'data': item}

# if __name__ == '__main__':
#     # event ={
#     #     "pdp_url": "https://www.fixsupply.com/bulk-bolt-849-carriage-bolt-square-neck-round-head-zinc-plated-low-carbon-steel-5-8-11-thread-6-1-2-long",
#     #     "sku": "BULK-BOLT-849",
#     #     "vendor": "fixsupply"
#     # }
#     event ={"vendor": "fixsupply",
#         "pdp_url": "https://www.fixsupply.com/euc-dcs-5-euclid-super-diamond-clear-solvent-based-curing-and-sealing-compound-5-gallon",
#         "sku": "EUC-DCS-"}
#     print(fixsupply(pdp_url=event['pdp_url'], sku=event['sku']))