import json  # install json
import requests  # intall requests
from parsel import Selector  # intsall parsel
import re
max_retires = 5


def autodir(pdp_url, sku, vendor='autodir'):
    error = {}
    # request to pdp_url :-
    url_request = str()
    cookies = {
        '_ga': 'GA1.1.1424288283.1695893854',
        '__ssid': 'd5de6a813b283a7289bda7bbbc2fe02',
        'BNES__ce.irv': 'v5Kzgy61vGXklB1Nk63vOUoWTZRdsnUuEgGZ0RS8fShZPIakTUn9mQ963V6quIFct9Z5yPdLN04=',
        '_gcl_au': '1.1.2082847971.1704095129',
        '_ce.s': 'v~df40316d464e2552086a31b612fc9bb6386ed49b~lcw~1704174569670~vpv~13~ir~1~gtrk.la~lnbfsszm~lva~1704173757437~v11.cs~341137~v11.s~ce054400-a930-11ee-8cf4-fb0c6c3c2c8d~v11.sla~1704174569656~v11.send~1704194722040~lcw~1704194722041',
        'JSESSIONID': '6AA21FAF7097BE6FED2C17B84D1541CB-n2',
        'BNI_lb_adc': 'OVWxD1c9RFmPcqGTcXUDPylexxOtb0Zbp_lX3yJgwFmhTM1O5l0R-GH_ybdeEETiuBpNANGFXenVIIMTq4n99g==',
        'rv_cookie': 'E58-30DPS280-HLP%2CCPSF-AP-H%2CSTP-MTRH-34066D%2CUK1D-G7-0E%2C.2518ES1BW56C-S',
        '_uetsid': '92ba3890bff711ee868ff54788958608',
        '_uetvid': 'aa4a18105de211ee9fde4340933b5bb5',
        '_ga_RBCPR8BN5Y': 'GS1.1.1706681748.42.0.1706681748.0.0.0',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.1.1424288283.1695893854; __ssid=d5de6a813b283a7289bda7bbbc2fe02; BNES__ce.irv=v5Kzgy61vGXklB1Nk63vOUoWTZRdsnUuEgGZ0RS8fShZPIakTUn9mQ963V6quIFct9Z5yPdLN04=; _gcl_au=1.1.2082847971.1704095129; _ce.s=v~df40316d464e2552086a31b612fc9bb6386ed49b~lcw~1704174569670~vpv~13~ir~1~gtrk.la~lnbfsszm~lva~1704173757437~v11.cs~341137~v11.s~ce054400-a930-11ee-8cf4-fb0c6c3c2c8d~v11.sla~1704174569656~v11.send~1704194722040~lcw~1704194722041; JSESSIONID=6AA21FAF7097BE6FED2C17B84D1541CB-n2; BNI_lb_adc=OVWxD1c9RFmPcqGTcXUDPylexxOtb0Zbp_lX3yJgwFmhTM1O5l0R-GH_ybdeEETiuBpNANGFXenVIIMTq4n99g==; rv_cookie=E58-30DPS280-HLP%2CCPSF-AP-H%2CSTP-MTRH-34066D%2CUK1D-G7-0E%2C.2518ES1BW56C-S; _uetsid=92ba3890bff711ee868ff54788958608; _uetvid=aa4a18105de211ee9fde4340933b5bb5; _ga_RBCPR8BN5Y=GS1.1.1706681748.42.0.1706681748.0.0.0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    item = {}

    for i in range(max_retires):

        url_request = requests.get(url=pdp_url,
                                   headers=headers,
                                   cookies=cookies
                                   )
        if url_request.status_code == 200:
            break

    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}

    if 'class="col-12 col-sm-6"' not in url_request.text:
        error['statusCode'] = 404
        error['error_message'] = 'Product not found'
        return error

    response = Selector(text=url_request.text)

    try:
        item['sku'] = response.xpath('//div[@id="topMiddleContent"]//h1//text()').get().replace("\n", " ").strip()
        if item['sku'] != sku:
            error['statusCode'] = 404
            error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
            return error

    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = str(e)
        return error
    available_to_checkout = response.xpath('//div[@class="adc-green"]//span[@class="adc-green"]//text()').getall()
    available_to_checkout = ''.join(available_to_checkout)
    if available_to_checkout:
        if 'available' in available_to_checkout.lower():
            a = True
        else:
            a = False
    else:
        a = False

    item['vendor'] = vendor
    item['pdp_url'] = pdp_url
    item['sku'] = sku

    price_list = []

    if response.xpath('//div[@id="google-ad-price"]'):
            price = response.xpath('//div[@id="google-ad-price"]//text()').get().split("=")[0].replace('$', '').replace("\n", "").strip()
            if price:
                price_list.append({
                    "currency": "USD",
                    'min_qty': 1,
                    'price': float(price)
                })

            else:
                price_list.append({
                    'min_qty': 1,
                    'price_string': 'Call for price'
                })



    elif response.xpath('//div[@style="display: table; width: 100%"]//div[@class="adc-green"]'):
            price = response.xpath('//div[@style="display: table; width: 100%"]//div[@class="adc-green"]//text()').get().replace('$', '').replace("\n", "").strip()
            if price:
                price_list.append({
                    "currency": "USD",
                    'min_qty': 1,
                    'price': float(price)
                })

            else:
                price_list.append({
                    'min_qty': 1,
                    'price_string': 'Call for price'
                })

    else:

            price_list.append({
                'min_qty': 1,
                'price_string': 'Call for price'
            })




    if price_list:
        item['price'] = price_list
    else:
        item['price'] = None

    estimated_lead_time = []
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': '_gcl_au=1.1.617190834.1685023103; __ssid=3ccbe1f9886c4d215801ea897296480; BNES_cebsp_=umE7K18J1ZWq4tVuYXOZDRE9s+D3bGPpnC3s/uMZmFOxdmGFrpvvCRzxrpG5TpFkfdiRnxfZ1EQ=; _gid=GA1.2.195688930.1685336375; cebs=1; _ce.s=v~db8d48b29a237cc669c5e94e4445d841faa39fd6~lcw~1685162974899~vpv~3~lcw~1685336375898; cebsp_=18; JSESSIONID=6870B203297C5A5205FE48AA89866E6F-n2; BNI_lb_adc=OVWxD1c9RFmPcqGTcXUDPylexxOtb0Zb6hjcS6A41lUyWExZOwpIvaPvpRElUYSO2hoICxXlmqLFbR1Obwg_mA==; ln_or=eyI4Nzk3IjoiZCJ9; rv_cookie=OPT2103%2CPK-M-1000-L%2COPT2030%2C6150E-6501%2CABP1H51Z11%2CLZE19-300A-00-10S%2CGS13N-40P5%2CA32060DD%2CPC-M-0150-L%2CGIB-XY-015-V-2A; _ga_RBCPR8BN5Y=GS1.1.1685424616.16.1.1685427452.0.0.0; _ga=GA1.2.1874894313.1685023103; _gat=1; _uetsid=9b939950fddd11ed9b961995039838db; _uetvid=376eccf0fb0411edb320f3cfd0a972e2',
        'Referer': sku,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    params = {
        'item': sku,
    }
    response1 = requests.get('https://www.automationdirect.com/rest/location/freeDeliveryEstimate',
                             params=params,
                             headers=headers)
    lead_time = response1.text.replace("<br> ", " ")
    # print(estimated_lead_time)
    estimated_lead = ''
    if 'na' in lead_time:
        pass
    if 'within' in lead_time:
        estimated_lead = lead_time
    elif '2 day' in lead_time or '2-Day' in lead_time:
        if 'after' in lead_time:
            pass
        else:
            estimated_lead = lead_time

    if estimated_lead == '':
        pass
    else:
        lead_time_1 = {'raw_value':estimated_lead}
        estimated_lead_time.append({
                              'min_qty': 1,
                              'time_to_ship': lead_time_1
                          }),
        # estimated_lead_time.append(lead_time_1)

    es = ''
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': '_gcl_au=1.1.585257038.1695893851; _ga=GA1.1.1424288283.1695893854; __ssid=d5de6a813b283a7289bda7bbbc2fe02; JSESSIONID=31F6B38C1011AE1145D2F40EB8A48EE0-n2; BNI_lb_adc=OVWxD1c9RFmPcqGTcXUDPylexxOtb0ZbkjPG5kE8Za-__FZYqSmmHlNAKTcOowuUijwj3rREZXALjeGH3vVw2g==; cebs=1; _ce.clock_event=1; ln_or=eyI4Nzk3IjoiZCJ9; _ce.clock_data=34%2C45.114.64.66%2C1%2C22210ca73bf1af2ec2eace74a96ee356; rv_cookie=7000-19061-7051000%2C7000-19162-9790050%2C7000-19162-9790100%2C214825%2C107007%2C15575711%2C7000-14521-0000000%2CAR16G5N-C2E3G%2CSC242404G%2CA14030DN; _uetsid=c8b8ba1061b311eeb73acfab83bfd4c0; _uetvid=aa4a18105de211ee9fde4340933b5bb5; cebsp_=16; _ce.s=v~df40316d464e2552086a31b612fc9bb6386ed49b~lcw~1696319020425~vpv~1~ir~1~gtrk.la~lna0ksqs~lcw~1696319071878; _ga_RBCPR8BN5Y=GS1.1.1696318496.3.1.1696319342.0.0.0',
        'Referer': 'https://www.automationdirect.com/adc/shopping/catalog/drives_-a-_soft_starters/ac_variable_frequency_drives_(vfd)/high-performance_vfds/15575711',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response22 = requests.get(f'https://www.automationdirect.com/rest/instock-notifications/backorderInfo/{sku}/2147483647',
                              headers=headers, )
    data = json.loads(response22.text)
    k = data['expected']
    s = Selector(text=k)
    n = s.xpath('//p//text()').getall()
    final_qty = 1
    for jj in range(0, len(n)):
        if jj == None:
            pass
        elif 'More' in k:
            try:
                int_qty = final_qty + int(re.findall(r'\d+ ', n[jj])[0])
                final_qty = int_qty
            except:
                pass
            date_lead = "TBD"
            try:
                date_lead = re.findall(r'\b(\d{1,2}/\d{1,2}/\d{4})\b', n[jj + 1])[0]
                # print(date_lead)
                date_lead = 'More' + ' ' + date_lead
            except Exception as e:
                date_lead = "TBD"
                # print()

            estimated_lead_time.append({
                'min_qty': int_qty,
                'time_to_stock': {'raw_value': date_lead}
            }),
        elif 'arliest' in k:
            try:
                int_qty = final_qty + int(re.findall(r'\d+ ', n[jj])[0])
                final_qty = int_qty
            except:
                pass
            date_lead = "TBD"
            try:
                date_lead = re.findall(r'\b(\d{1,2}/\d{1,2}/\d{4})\b', n[jj + 1])[0]
                # print(date_lead)
                date_lead = 'earliest' + ' ' + date_lead
            except Exception as e:
                date_lead = "TBD"
                # print()

            estimated_lead_time.append({
                'min_qty': int_qty,
                'time_to_stock': {'raw_value': date_lead}
            }),
    item['lead_time'] = estimated_lead_time
    item['available_to_checkout'] = a
    item['in_stock'] = a
    # body = {"body": item}
    if item['lead_time'] == []:
        item['lead_time'] = None

    return {'statusCode': 200,
            'data': item}


# Input Params
# vendor = "AutomationDirect"
# sku = 'GS13N-40P5'
# pdp_url = 'https://www.automationdirect.com/adc/shopping/catalog/drives_-a-_soft_starters/ac_variable_frequency_drives_(vfd)/micro_vfds/gs13n-40p5'
# print(json.dumps(autodir(pdp_url, sku)))
