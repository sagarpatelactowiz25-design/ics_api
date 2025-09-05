import re
import requests
from parsel import Selector
import json


def lead_time_req(lead_payload):
    lead_ = requests.post(url="https://www.fishersci.com/shop/products/service/availability",
                          json=lead_payload)
    return lead_

def price_req(price_payload):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'new_hf=true; akacd_FS_Prod_AWS_EKS=3890901011~rv=98~id=c096fcd72fe7698bb98c79f2d8f15db9; locale=en_US; usertype=G; akacd_FS_US_ProdA_Search_LucidWorks=3890901016~rv=42~id=029d447595c19b63bbfe1c0c329e4492; preventSingleResultRedirect=true; new_cart=true; new_overlay=true; f_num=gmr; userTypeDescription=guest; akacd_FS_Prod_AWS_EKS_Users=3890901018~rv=47~id=24d7b2fc3f2396eab58bfede13321d3c; formSecurity=djgo81hxuiv; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_cookie_privacy=permit 1,2,3; mdLogger=false; kampyle_userid=fd91-bd2a-7f16-8f32-4575-05f8-9156-d71a; AMCVS_8FED67C25245B39C0A490D4C%40AdobeOrg=1; s_vi=[CS]v1|331092909E76E464-600003CCDE6A301E[CE]; s_ecid=MCMID%7C05340063993881476880179895272431826554; testTLD=test; WCXUID=11037385662017134893180; _gcl_au=1.1.259503727.1713489320; memberId_AAM=; com.ibm.commerce.ubx.idsync.DSPID_ADOBE%2Cx1VisitorId=com.ibm.commerce.ubx.idsync.DSPID_ADOBE%2Cx1VisitorId; at_check=true; accountId_AAM=Guest%20or%20No%20Account%20Chosen; PFM=unsorted; _gid=GA1.2.1508837673.1713489323; QuantumMetricUserID=c554416fdff43119765df29f8355a23d; _hjSessionUser_341846=eyJpZCI6ImE4NGRjMjQ2LTQ4NjYtNTk0Ny1hZmE2LWY4ZTQ3MjZmYTllMiIsImNyZWF0ZWQiOjE3MTM0ODkzMTc3MDAsImV4aXN0aW5nIjp0cnVlfQ==; aam_uuid=09188941913722890890708937986609819091; com.ibm.commerce.ubx.idsync.DSPID_ADOBE%2CaaUserId%2CmcId%2Cx1VisitorId=com.ibm.commerce.ubx.idsync.DSPID_ADOBE%2CaaUserId%2CmcId%2Cx1VisitorId; BIGipServerwww.fishersci.com_magellan_pool=1271580682.37919.0000; s_days_since_new_s=Less than 1 day; AMCV_8FED67C25245B39C0A490D4C%40AdobeOrg=359503849%7CMCIDTS%7C19833%7CMCMID%7C05340063993881476880179895272431826554%7CMCAAMLH-1714156841%7C7%7CMCAAMB-1714156841%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1713559241s%7CNONE%7CMCAID%7C331092909E76E464-600003CCDE6A301E%7CvVersion%7C5.0.1%7CMCCIDH%7C-1997303517; WCXSID=00002859426171355204645466666666; QuantumMetricSessionID=9c2b8474f3c5d45d6af30f48fecb512e; bm_mi=C4BAB7AF009C65A2EC6CE86D47BADCF4~YAAQRGgBFwTJSu6OAQAACJ5I9ReWiBzQUumvCTUcuFqVMEWtln1C1epvbj2a+HT3chQyc9UfalFD6pSTcnXOqHNW/8q3Xue6MFlEkSvJrLHjm/dklv9SYb3LDYHpkdf/4VJAjkdCFSmNAMpJEElLvQLhz6hIQVf8mF17vY4pD4YT/1YzFeABfIrs7N2f1IQ4puG3uuRUHT23gHAIO1OGXWlux89sQzf6DfhwPvzsXxnpfPa4rbA9sO8qczwZn9FWw12yUEoXgx5LZDTtjnZ1WYHLTqIjzxwQvt9rQz6j0u4gows6Mh450fjZqwgtqBu8+c9LGRmFSfGC5OJ6OYTgYmiBcdBuztFwwwo3Ikk5Xg==~1; _hjSession_341846=eyJpZCI6IjVkMTU5OTZjLWNjYzYtNGEzNi1hMzg3LWE4MjBlOGNmZTcxNSIsImMiOjE3MTM1NTMyNTA1NDcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; ak_bmsc=D1A09A1C1EB22CEE81DECA9C7853EEF8~000000000000000000000000000000~YAAQRGgBF8/MSu6OAQAAhspI9ReNT39E4jhrRTOiSPTnhlLntl3r2i0XQPBYRWh93d12JVeSdzlrm5wF1nsr4dTQQbBzrSLXg5K7sv9G7/otWmu3w8iQUKjnAsubwNGF5ojdyCMTW3c55XjZaVazbEtFZX/Cm7AUYaFAj5/dw8ChjvN4E5GJFFvDnREwDNraQAp7Ey8M+Y36UIf86jZ5y7/NYn2PUi+5fZG0JzZoyZARiHk4DTY7J3lAI50mSBsLuf0VvZBmvwx8fPD3XzMK/7PVff16WcvEN124tauiEFYY83cmOeiyUOxPc7qPc2l957mG0a3Rd7GuPL55EflcC0jcweDGK7SooMnl7hETbxLr2Gms709vCgeetygz3rkXuiVttHVW9KDXxd0MB8x65DMvTq6eywmTpipb7YZppL7YL/OuN4x42S9t+DqIEnmDiWoYfirK3X4pZMb33OevvnAVUk7Z7ZE/q87sJ+LYR7VEvtdwEQaMvcKLDpPN5mQ9tzvlMJy8rWgoVM3LqbCDshw=; WCS_JSESSIONID=0000amAWP0L6J-OtnKefEhLsn7j:15lh8tatj; BIGipServerwww.fishersci.com_commerce_pool=818595850.37151.0000; estore=estore-scientific; vcCookie=1; WCXSID_expiry=1713554365346; s_sess=%20s_sq%3D%3B%20s_cc%3Dtrue%3B; s_days_since_new=1713555171865; kampyleUserSession=1713555191596; kampyleUserSessionsCount=19; kampyleSessionPageCounter=1; mbox=PC#9334cfe3ce03403e8e3791ed8d2fba6e.34_0#1776799993|session#bf9cfc83233c4a80b3893701440e0d54#1713556007; _ga=GA1.1.906955181.1713489323; adcloud={%22_les_v%22:%22c%2Cy%2Cfishersci.com%2C1713557569%22}; cto_bundle=qTDRml8wMFVoRlg3eVVGOW93RmRlJTJGRkdlZ2ZQV2RDMVhaWXIxWjF4bHduYUltcHpZSFNrem44SnclMkZLZ2slMkY0b3VpdnMwVlNZRjQ5eGx2UGRicDNKRXJPRllmSEdjUFR1eFpqenVmNjVsR3Q3R01qTUJ3NzNiWHM3Q2hQJTJGZkpBJTJCekNyMFpjU0xJZExWJTJGUCUyQk1JSUNGdkxSQ3VrSkV2S3dIUzZKc3FIOWdPRWZxdHVYZyUzRA; _ga_TX98RX25ZK=GS1.1.1713552053.3.1.1713556347.60.0.0; bm_sv=3F599766DC6A700890D4F9D1B9BA8A07~YAAQRGgBF9cPTu6OAQAACe539RdNMFbnGG5yFSreW+JRU89C+49lZAqbDGoY5ichS3XybrXYll6r/bPwHR2vghTB+R4uJrsIJlgECg6fvi23/djkva1Wnid/FAKlQAC/HOjNItpTIDi1cxJSVpVk+A+t7uKQRaQJbUe58cp0GyBNcmU1Fr6t9nV0z8sssAvDEaLlN2Nf/PcwULgsJY0LswmRX6cDrfMjtQVM7v8tAlwt0RzqcU9aebu1IixKLWFDQzWK+uw=~1; new_quote=true; new_checkout=gmr; TAsessionID=0b8a7c66-56a8-4907-9afb-c1a53c4cfc59|EXISTING; notice_behavior=implied,eu; cmapi_gtm_bl=; s_pers=%20s_fid%3D1B20FC4BB518AEBF-3B8D521FFEEBED0C%7C1871255721346%3B%20gpv_pn%3D%253Ashop%253Aproducts%253Awater-optima-fisher-chemical-3%253Aw71%7C1713558152074%3B',
        'origin': 'https://www.fishersci.com',
        'referer': 'https://www.fishersci.com/shop/products/water-optima-fisher-chemical-3/W71',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-b3-traceid': '5c420285f43e0c7044cd560f0b599fc3',
        'x-requested-with': 'XMLHttpRequest'
    }
    response_price = requests.post('https://www.fishersci.com/shop/products/service/pricing',
                                   data=price_payload,headers=headers)
    data_price = json.loads(response_price.text)
    return data_price

def thermofisherscientific(url, sku, vendor='thermofisherscientific'):
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

    if 'class="product_carousel_container"' not in url_request.text:
        error['statusCode'] = 404
        error['error_message'] = 'Product not found'
        return error
    if '>Item Discontinued<' in url_request.text:
        error['statusCode'] = 410
        error['error_message'] = "Product Discontinued"
        return error
    # if 'This item has been discontinued' in url_request.text:
    #     error['statusCode'] = 410
    #     error['error_message'] = "Product Discontinued"
    #     return error

    # pass response to Selector :-
    response = Selector(url_request.text)
    # define dictionary for making data dictionary :-
    item = dict()
    # vendor Extracting :-
    item['vendor'] = vendor
    item['pdp_url'] = url
    # sku Extracting :-
    try:
        if '_productServiceResponse' in url_request.text:
            abc = url_request.text
            if '_productServiceResponse.items =' in abc:
                ab = abc.split('_productServiceResponse.items =')[1]
            else:
                print('nothing')
            abcd = ab.split('];')[0]
            data = abcd + ']'
            main_data = json.loads(data)
            for index, data in enumerate(main_data):
                if not index:
                    if 'This item has been discontinued by the supplier' in data['rules']['message']:
                        error['statusCode'] = 410
                        error['error_message'] = "Product Discontinued"
                        return error
                    item['sku'] = data['uncondensedPartNumber'].strip()
                    try:
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
                    try:
                        item['available_to_checkout'] = data["rules"]["buyable"]
                        item['in_stock'] = data["rules"]["buyable"]
                    except Exception as e:
                        item['available_to_checkout'] = False
                        item['in_stock'] = False
                    data_payload = {
                        'partNumber': f'{data["partNumber"]}',
                        "callerId": "products-ui-single-page"
                    }
                    price_res = price_req(price_payload=data_payload)
                    price = price_res['priceAndAvailability'][f'{data["partNumber"]}']
                    price_list = list()
                    if len(price) == 1:
                        uom_list = list()
                        for j in price:
                            price_item = dict()
                            price_item['currency'] = "USD"
                            if 'Pack' in j["displayUnitString"].split(' ') or 'pack' in j["displayUnitString"].split(' '):
                                uom_list.append('PK')
                                price_item['min_qty'] = 1
                                if j['price']:
                                    prc1 = float(j['price'].replace('$', '').replace(',', ''))
                                    prc1 = "{:.2f}".format(prc1)
                                    price_item['price'] = float(prc1)
                                else:
                                    price_item['price_string'] = "Call for price"
                                price_list.append(price_item)
                            elif 'Case' in j["displayUnitString"].split(' ') or 'case' in j["displayUnitString"].split(' '):
                                uom_list.append('CS')
                                price_item['min_qty'] = 1
                                if j['price']:
                                    prc_1 = float(j['price'].replace('$', '').replace(',', ''))
                                    price_item['price'] = float("{:.2f}".format(prc_1))
                                else:
                                    price_item['price_string'] = "Call for price"
                                price_list.append(price_item)
                            else:
                                uom_list.append('EA')
                                valid_qty = "".join([i for i in j['displayUnitString'].split(' ') if i.isdigit()])
                                price_item['min_qty'] = int(j['quantity'] if not valid_qty else j['quantity'] if valid_qty == j['quantity'] else valid_qty)
                                if j['price']:
                                    prc2 = float(j['price'].replace('$', '').replace(',', ''))
                                    prc2 = "{:.2f}".format(prc2)
                                    price_item['price'] = float(prc2)
                                else:
                                    price_item['price_string'] = "Call for price"
                                price_list.append(price_item)
                        slug_id = url.split('/')[-1]
                        if uom_list[0] == "PK":
                            uom = 'PK'
                        elif uom_list[0] == "CS":
                            uom = "CS"
                        else:
                            uom = "EA"
                        data_ = {'parts': [{'partNumber': f"{slug_id}", 'uom': f'{uom}', 'quantity': '1'}],
                                 'zipCode': '00501'}
                        if 'Due to product restrictions, please' not in url_request.text:
                            lead_time_ = lead_time_req(data_)
                            try:
                                lead_time_json = json.loads(lead_time_.text)
                                for i in lead_time_json["priceAndAvailability"][f"{slug_id}"]:
                                    text_ = Selector(i['availability'])
                                    if text_.xpath("//div[@class='lead-time']//text()"):
                                        lead_time = " ".join(text_.xpath('//div[@class="lead-time"]//text()').getall())
                                        if 'Estimated' in lead_time or 'Available ' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_arrive": {"raw_value": f"{lead_time}"}}]
                                        elif 'Usually' in lead_time or 'business days' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_ship": {"raw_value": f"{lead_time}"}}]
                                        else:
                                            estimated_lead_time_ = []
                                    elif text_.xpath("//span[@class='backorder-qty display_inline_msg']//text()"):
                                        if 'Estimated to ship' in "".join(text_.xpath(
                                                "//span[@class='backorder-qty display_inline_msg']//text()").getall()):
                                            time = " ".join(text_.xpath(
                                                "//span[@class='backorder-qty display_inline_msg']//text()").getall()).split(
                                                'to')
                                            lead_time = re.sub('\s+', ' ', time[0]).strip()
                                            if lead_time == "Estimated":
                                                _time_chek = re.sub('\s+', ' ', time[-2].strip())
                                                lead_time = "Estimated to " + _time_chek
                                        else:
                                            time = " ".join(text_.xpath(
                                                "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                                'to')
                                            lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        # time = " ".join(text_.xpath(
                                        #     "//span[@class='backorder-qty display_inline_msg']//text()").getall()).split(
                                        #     'to')
                                        # lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        if 'Estimated' in lead_time or 'Available ' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_arrive": {"raw_value": f"{lead_time}"}}]
                                        elif 'Usually' in lead_time or 'business days' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_ship": {"raw_value": f"{lead_time}"}}]
                                        else:
                                            estimated_lead_time_ = []
                                    elif text_.xpath("//span[@class='available-qty display_inline_msg']//text()"):
                                        if ' Available to ship' in "".join(text_.xpath(
                                                "//span[@class='available-qty display_inline_msg']//text()").getall()):
                                            time = " ".join(text_.xpath(
                                                "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                                'to')
                                            lead_time = re.sub('\s+', ' ', time[0]).strip()
                                            if lead_time == "Available":
                                                _time_chek = re.sub('\s+', ' ', time[-2].strip())
                                                lead_time = "Available to " + _time_chek
                                        else:
                                            time = " ".join(text_.xpath(
                                                "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                                'to')
                                            lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        # time = " ".join(text_.xpath(
                                        #     "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                        #     'to')
                                        # lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        if 'Estimated' in lead_time or 'Available' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_arrive": {"raw_value": f"{lead_time}"}}]
                                        elif 'Usually' in lead_time or 'business days' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_ship": {"raw_value": f"{lead_time}"}}]
                                        else:
                                            estimated_lead_time_ = None
                                    else:
                                        estimated_lead_time_ = None
                                    item['lead_time'] = estimated_lead_time_
                            except:
                                item['lead_time'] = None
                        else:
                            item['lead_time'] = None
                    else:
                        cnt = 1
                        uom_li = list()
                        for j in price:
                            if j['displayUnitString']:
                                qty = re.findall(r'\d+', j['displayUnitString'])
                                uom_li.append(j['uom'])
                                if not qty:
                                    p_qty = j['quantity']
                                else:
                                    p_qty = qty[0]
                                price_item = dict()
                                price_item['currency'] = "USD"
                                if cnt == 1:
                                    if j['price']:
                                        prc3 = float(j['price'].replace('$', '').replace(',', ''))
                                        prc3 = "{:.2f}".format(prc3)
                                        price_item['price'] = float(prc3)
                                        price_item['price'] = float(j['price'].replace('$', '').replace(',', ''))
                                    else:
                                        price_item['price_string'] = "Call for price"
                                    if j['displayUnitString']:
                                        qty = re.findall(r'\d+', j['displayUnitString'])
                                        if not qty:
                                            p_qty = j['quantity']
                                        else:
                                            p_qty = qty[0]
                                        price_item['min_qty'] = p_qty
                                    price_list.append(price_item)
                                elif qty != j['quantity'] and cnt != 1:
                                    if j['price']:
                                        prc4 = float(j['price'].replace('$', '').replace(',', ''))
                                        price_item['price'] = float("{:.2f}".format(prc4))
                                    else:
                                        price_item['price_string'] = "Call for price"
                                    price_item['min_qty'] = j['quantity']
                                    price_list.append(price_item)
                        slug_id = url.split('/')[-1]
                        if uom_li[0] == 'PK':
                            uom = 'PK'
                        elif uom_li[0] == 'CS':
                            uom = 'CS'
                        else:
                            uom = 'EA'
                        data_ = {'parts': [{'partNumber': f"{slug_id}", 'uom': f'{uom}', 'quantity': '1'}],
                                 'zipCode': '00501'}
                        lead_time_ = lead_time_req(data_)
                        try:
                            lead_time_json = json.loads(lead_time_.text)
                            for i in lead_time_json["priceAndAvailability"][f"{slug_id}"]:
                                text_ = Selector(i['availability'])
                                if text_.xpath("//div[@class='lead-time']//text()"):
                                    lead_time = " ".join(text_.xpath('//div[@class="lead-time"]//text()').getall())
                                    if 'Estimated' in lead_time or 'Available ' in lead_time:
                                        estimated_lead_time_ = [
                                            {"min_qty": 1, "time_to_arrive": {"raw_value": f"{lead_time}"}}]
                                    elif 'Usually' in lead_time or 'business days' in lead_time:
                                        estimated_lead_time_ = [
                                            {"min_qty": 1, "time_to_ship": {"raw_value": f"{lead_time}"}}]
                                    else:
                                        estimated_lead_time_ = []
                                elif text_.xpath("//span[@class='backorder-qty display_inline_msg']//text()"):
                                    if 'Estimated to ship' in "".join(text_.xpath(
                                            "//span[@class='backorder-qty display_inline_msg']//text()").getall()):
                                        time = " ".join(text_.xpath(
                                            "//span[@class='backorder-qty display_inline_msg']//text()").getall()).split(
                                            'to')
                                        lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        if lead_time == "Estimated":
                                            _time_chek = re.sub('\s+', ' ', time[-2].strip())
                                            lead_time = "Estimated to " + _time_chek
                                    else:
                                        time = " ".join(text_.xpath(
                                            "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                            'to')
                                        lead_time = re.sub('\s+', ' ', time[0]).strip()
                                    # time = " ".join(text_.xpath(
                                    #     "//span[@class='backorder-qty display_inline_msg']//text()").getall()).split(
                                    #     'to')
                                    # lead_time = re.sub('\s+', ' ', time[0]).strip()
                                    if 'Estimated' in lead_time or 'Available ' in lead_time:
                                        estimated_lead_time_ = [
                                            {"min_qty": 1, "time_to_arrive": {"raw_value": f"{lead_time}"}}]
                                    elif 'Usually' in lead_time or 'business days' in lead_time:
                                        estimated_lead_time_ = [
                                            {"min_qty": 1, "time_to_ship": {"raw_value": f"{lead_time}"}}]
                                    else:
                                        estimated_lead_time_ = []
                                elif text_.xpath("//span[@class='available-qty display_inline_msg']//text()"):
                                    if ' Available to ship' in "".join(text_.xpath(
                                            "//span[@class='available-qty display_inline_msg']//text()").getall()):
                                        time = " ".join(text_.xpath(
                                            "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                            'to')
                                        lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        if lead_time == "Available":
                                            _time_chek = re.sub('\s+', ' ', time[-2].strip())
                                            lead_time = "Available to " + _time_chek
                                    else:
                                        time = " ".join(text_.xpath(
                                            "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                            'to')
                                        lead_time = re.sub('\s+', ' ', time[0]).strip()
                                    # time = " ".join(text_.xpath(
                                    #     "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                    #     'to')
                                    # lead_time = re.sub('\s+', ' ', time[0]).strip()
                                    if 'Estimated' in lead_time or 'Available' in lead_time:
                                        estimated_lead_time_ = [
                                            {"min_qty": 1, "time_to_arrive": {"raw_value": f"{lead_time}"}}]
                                    elif 'Usually' in lead_time or 'business days' in lead_time:
                                        estimated_lead_time_ = [
                                            {"min_qty": 1, "time_to_ship": {"raw_value": f"{lead_time}"}}]
                                    else:
                                        estimated_lead_time_ = None
                                else:
                                    estimated_lead_time_ = None
                                item['lead_time'] = estimated_lead_time_
                        except:
                            item['lead_time'] = None
                    item['price'] = price_list

        else:
            if response.xpath("//script[@type='application/ld+json']"):
                prd_myjson1 = response.xpath("//script[@type='application/ld+json']").get('')
                prd_myjson = prd_myjson1.replace('<script type="application/ld+json">', '').replace('\n','').replace('</script>', '')
                try:
                    myjson = eval(prd_myjson)
                except:
                    return None
                item['sku'] = myjson["sku"].strip()
                try:
                    if item['sku'] != sku:
                        error['statusCode'] = 404
                        error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
                        return error
                    elif 'p-' in item['sku']:
                        error['statusCode'] = 404
                        error['error_message'] = f"Product not found"
                        return error
                    else:
                        pass
                except Exception as e:
                    # The function should return a dictionary having statusCode: 500;
                    # If scraped sku does not match sku passed in input parameter
                    error['statusCode'] = 500
                    error['error_message'] = str(e)
                try:
                    item['available_to_checkout'] = True if response.xpath(
                        "//div[@id='SKUAddToCartContainer']//div[@id='qa_add_to_cart_button_0']") else False
                    item['in_stock'] = True if response.xpath(
                        "//div[@id='SKUAddToCartContainer']//div[@id='qa_add_to_cart_button_0']") else False
                except:
                    pass
                packe_label_validateor = 0
                try:
                    if myjson['offers']:
                        try:
                            uom_li =list()
                            for ind, d in enumerate(myjson['offers']):
                                if "Pack" in d['eligibleQuantity']['unitText'].split(' ') or "pack" in d['eligibleQuantity']['unitText'].split(' '):
                                    pack_label = 'PK'
                                    uom_li.append(pack_label)
                                elif "case" in d['eligibleQuantity']['unitText'].split(' ') or "Case" in d['eligibleQuantity']['unitText'].split(' '):
                                    uom = 'CS'
                                    uom_li.append(uom)
                                else:
                                    default = 'EA'
                                    uom_li.append(default)
                            slug_id = url.split('/')[-1]
                            first_uom = uom_li[0]
                            if first_uom == 'CS':
                                payload_lead = {'parts': [{'partNumber': f"{slug_id}", 'uom': f'{first_uom}', 'quantity': '1'}],'zipCode': '00501'}
                            elif first_uom == "PK":
                                payload_lead = {
                                    'parts': [{'partNumber': f"{slug_id}", 'uom': f'{first_uom}', 'quantity': '1'}],'zipCode': '00501'}
                            else:
                                payload_lead = {
                                    'parts': [{'partNumber': f"{slug_id}", 'uom': f'EA', 'quantity': '1'}],'zipCode': '00501'}
                            lead_time_ = lead_time_req(payload_lead)
                            try:
                                lead_time_json = json.loads(lead_time_.text)
                                for i in lead_time_json["priceAndAvailability"][f"{slug_id}"]:
                                    text_ = Selector(i['availability'])
                                    if text_.xpath("//div[@class='lead-time']//text()"):
                                        lead_time = " ".join(
                                            text_.xpath('//div[@class="lead-time"]//text()').getall())
                                        if 'Estimated' in lead_time or 'Available ' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_arrive": {"raw_value": f"{lead_time}"}}]
                                        elif 'Usually' in lead_time or 'business days' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_ship": {"raw_value": f"{lead_time}"}}]
                                        else:
                                            estimated_lead_time_ = []
                                    elif text_.xpath("//span[@class='backorder-qty display_inline_msg']//text()"):
                                        if 'Estimated to ship' in "".join(text_.xpath(
                                                "//span[@class='backorder-qty display_inline_msg']//text()").getall()):
                                            time = " ".join(text_.xpath(
                                                "//span[@class='backorder-qty display_inline_msg']//text()").getall()).split(
                                                'to')
                                            lead_time = re.sub('\s+', ' ', time[0]).strip()
                                            if lead_time == "Estimated":
                                                _time_chek = re.sub('\s+', ' ', time[-2].strip())
                                                lead_time = "Estimated to " + _time_chek
                                        else:
                                            time = " ".join(text_.xpath(
                                                "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                                'to')
                                            lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        # time = " ".join(text_.xpath(
                                        #     "//span[@class='backorder-qty display_inline_msg']//text()").getall()).split(
                                        #     'to')
                                        # lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        if 'Estimated' in lead_time or 'Available ' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_arrive": {"raw_value": f"{lead_time}"}}]
                                        elif 'Usually' in lead_time or 'business days' in lead_time:
                                            estimated_lead_time_ = [
                                                {"min_qty": 1, "time_to_ship": {"raw_value": f"{lead_time}"}}]
                                        else:
                                            estimated_lead_time_ = []
                                    elif text_.xpath("//span[@class='available-qty display_inline_msg']//text()"):
                                        if ' Available to ship' in "".join(text_.xpath(
                                                "//span[@class='available-qty display_inline_msg']//text()").getall()):
                                            time = " ".join(text_.xpath(
                                                "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                                'to')
                                            lead_time = re.sub('\s+', ' ', time[0]).strip()
                                            if lead_time == "Available":
                                                _time_chek = re.sub('\s+', ' ', time[-2].strip())
                                                lead_time = "Available to " + _time_chek
                                        else:
                                            time = " ".join(text_.xpath(
                                                "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                                'to')
                                            lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        # time = " ".join(text_.xpath(
                                        #     "//span[@class='available-qty display_inline_msg']//text()").getall()).split(
                                        #     'to')
                                        # lead_time = re.sub('\s+', ' ', time[0]).strip()
                                        if 'Estimated' in lead_time or 'Available' in lead_time:
                                            estimated_lead_time_ = [{"min_qty": 1, "time_to_arrive": {"raw_value": f"{lead_time}"}}]
                                        elif 'Usually' in lead_time or 'business days' in lead_time:
                                            estimated_lead_time_ = [{"min_qty": 1, "time_to_ship": {"raw_value": f"{lead_time}"}}]
                                        else:
                                            estimated_lead_time_ = None
                                    else:
                                        estimated_lead_time_ = None
                                    item['lead_time'] = estimated_lead_time_
                            except:
                                item['lead_time'] = None
                        except:
                            pass

                        price_list = list()
                        for ind, d in enumerate(myjson['offers']):
                            price_item = dict()
                            if ind == 0:
                                try:
                                    price_item['min_qty'] = int("".join([i for i in d['eligibleQuantity']['unitText'].split(' ') if i.isdigit()])) if packe_label_validateor == 0 else 1
                                    if not price_item['min_qty']:
                                        price_item['min_qty'] = 1
                                except:
                                    price_item['min_qty'] = 1
                                descount_rate = response.xpath("//div[@class='promo_price']//span[@class='qa_webdiscount_msg_link']//text()").get()
                                try:
                                    if d["price"]:
                                        if not descount_rate:
                                            myprd = float(d["price"].replace(',', ''))
                                            myprc = "{:.2f}".format(myprd)
                                            price_item['price'] = float(myprc)
                                            price_item['currency'] = "USD"
                                        else:
                                            myprc_2 = response.xpath("//div[@class='promo_price']//span[@itemprop='price']/@content").get()
                                            if not myprc_2:
                                                myprc_2 = response.xpath("//label[@class='price']//span[@itemprop='price']/@content").get()
                                            myprc_2 = myprc_2.replace(',', '').replace('$', '').strip()
                                            try:
                                                price_item['price'] = float("{:.2f}".format(myprc_2))
                                                price_item['currency'] = "USD"
                                            except:
                                                myprc_error = float(myprc_2)
                                                price_item['price'] = float(round(myprc_error, 2))
                                                price_item['currency'] = "USD"
                                    else:
                                        price_item['price_string'] = "Call for price"
                                    price_list.append(price_item)
                                except:
                                    price_item['price_string'] = "Call for price"
                                    price_list.append(price_item)
                            elif "Pack" in d['eligibleQuantity']['unitText'].split(' ') or "pack" in d['eligibleQuantity']['unitText'].split(' ') and ind != 0:
                                price_item['min_qty'] = int(" ".join([i for i in d['eligibleQuantity']['unitText'].split(' ') if
                                                                 i.isdigit()])) if packe_label_validateor != 0 else 1
                                if not price_item['min_qty']:
                                    price_item['min_qty'] = 1
                                descount_rate = response.xpath("//div[@class='promo_price']//span[@class='qa_webdiscount_msg_link']//text()").get()
                                if d["price"]:
                                    if not descount_rate:
                                        myprd_3 = float(d["price"].replace(',', ''))
                                        price_item['price'] = float("{:.2f}".format(myprd_3))
                                        price_item['currency'] = "USD"
                                    else:
                                        myprc_2 = response.xpath("//div[@class='promo_price']//span[@itemprop='price']/@content").getall()[-1]
                                        if not myprc_2:
                                            myprc_2 = response.xpath("//label[@class='price']//span[@itemprop='price']/@content").getall()[-1]
                                        myprc_2 = myprc_2.replace(',', '').replace('$', '').strip()
                                        try:
                                            price_item['price'] = float("{:.2f}".format(myprc_2))
                                            price_item['currency'] = "USD"
                                        except:
                                            myprc_error = float(myprc_2)
                                            price_item['price'] = round(myprc_error, 2)
                                            price_item['currency'] = "USD"
                                else:
                                    price_item['price_string'] = "Call for price"
                                price_list.append(price_item)
                            elif "Each" in d['eligibleQuantity']['unitText'].split(' ') and ind != 0:
                                price_item['min_qty'] = int("".join([i for i in d['eligibleQuantity']['unitText'].split(' ') if i.isdigit()]))
                                if not price_item['min_qty']:
                                    price_item['min_qty'] = 1
                                descount_rate = response.xpath("//div[@class='promo_price']//span[@class='qa_webdiscount_msg_link']//text()").get()
                                if d["price"]:
                                    if not descount_rate:
                                        myprd_4 = float(d["price"].replace(',', ''))
                                        price_item['price'] = float("{:.2f}".format(myprd_4))
                                        price_item['currency'] = "USD"
                                    else:
                                        myprc_2 = response.xpath("//div[@class='promo_price']//span[@itemprop='price']/@content").getall()[-1]
                                        if not myprc_2:
                                            myprc_2 = response.xpath("//label[@class='price']//span[@itemprop='price']/@content").getall()[-1]
                                        myprc_2 = myprc_2.replace(',', '').replace('$', '').strip()
                                        try:
                                            price_item['price'] = float("{:.2f}".format(myprc_2))
                                            price_item['currency'] = "USD"
                                        except:
                                            myprc_error = float(myprc_2)
                                            price_item['price'] = float(round(myprc_error, 2))
                                            price_item['currency'] = "USD"
                                else:
                                    price_item['price_string'] = "Call for price"
                                price_list.append(price_item)
                            elif "Case" in d['eligibleQuantity']['unitText'].split(' ') and ind != 0:
                                price_item['min_qty'] = int("".join([i for i in d['eligibleQuantity']['unitText'].split(' ') if i.isdigit()]))
                                if not price_item['min_qty']:
                                    price_item['min_qty'] = 1
                                descount_rate = response.xpath("//div[@class='promo_price']//span[@class='qa_webdiscount_msg_link']//text()").get()
                                if d["price"]:
                                    if not descount_rate:
                                        myprd = float(d["price"].replace(',', ''))
                                        myprc = float("{:.2f}".format(myprd))
                                        price_item['price'] = myprc
                                        price_item['currency'] = "USD"
                                    else:
                                        myprc_2 = response.xpath(
                                            "//div[@class='promo_price']//span[@itemprop='price']/@content").getall()[-1]
                                        if not myprc_2:
                                            myprc_2 = response.xpath(
                                                "//label[@class='price']//span[@itemprop='price']/@content").getall()[-1]
                                        myprc_2 = myprc_2.replace(',', '').replace('$', '').strip()
                                        try:
                                            price_item['price'] = float("{:.2f}".format(myprc_2))
                                            price_item['currency'] = "USD"
                                        except:
                                            myprc_error = float(myprc_2)
                                            price_item['price'] = float(round(myprc_error, 2))
                                            price_item['currency'] = "USD"
                                else:
                                    price_item['price_string'] = "Call for price"
                                price_list.append(price_item)
                        item['price'] = price_list
                except Exception as e:
                    error['statusCode'] = 500
                    error['error_message'] = str(e)
                    return error


    except Exception as e:
        # The function should return a dictionary having statusCode: 500;
        # If scraped sku does not match sku passed in input parameter
        error['statusCode'] = 500
        error['error_message'] = str(e)
        return error
        # url Extracting :-

    return {'statusCode': 200,
            'data': item}
