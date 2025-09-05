import json# install json
import requests# intall requests
from parsel import Selector # intsall parsel

import api_key as api_token


max_retires = 5


def teconnectivity(pdp_url,sku,vendor='teconnectivity'):
    token=api_token.scraperDo_key
    url_request=''
    pdp_url=pdp_url.replace("/usa-en/","/en/")
    error={}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # # 'Cookie': 'country_info=usa; site_info=usa|en; language_id=1; TECewt5=7bf39732-a966-44bf-94f9-d8d42e044813; TECewt7=9a8b0956-f840-4c56-936e-9513b129c1a0; IR_PI=3dd80257-690a-11ee-9a27-870a94f60e01%7C1697206761316; s_ecid=MCMID%7C58648963887400562022220646830085753637; _gcl_au=1.1.187185946.1706177535; _fbp=fb.1.1706177540875.1335288431; QSI_SI_5uIX2NZ1U3nltKB_intercept=true; drift_aid=d8540062-e6ac-4a1c-b0ab-a06e5445f681; driftt_aid=d8540062-e6ac-4a1c-b0ab-a06e5445f681; aam_uuid=66002759247785693341454096758550561241; cdn_geo_info=AG; dtCookie=v_4_srv_1_sn_BA547663249C2B3BD3CED9C4B6107B42_perc_100000_ol_0_mul_1_app-3A619a1bcb124cd83e_1; AKA_A2=A; ak_bmsc=645ECF2ABEF9527AACCB589CC851055D~000000000000000000000000000000~YAAQEKMTAsuHiKKOAQAARnxxrRd8xn2oj15/9UzppuxzlnMpzTDWrX7Pv9iuLQWfZU8YV+nUzsi573pxAVuT4RMMtu2bXrsjfRc7Vdo4/qQ9QVOjv8YZ0pNaG52EH8EccT1lmqbfYqe9xp+pCrIJvofy3/eyEuGACuJvqGwhJrminZWV5IQefhJB3ES7XLKmdStznb49q8GiK/tPCHirKAqN8zKGmsJCCqvk5GWDxgqJVac4zNt3Ney3gW958SzlmS/6VUH/Wc0rzhw5RBO2ieFnzE9Y9Ro+F6L0LyLS2PaiO20NXCdHUksnWUtOoF2mmB8eumfKk7LtejPWzVepa2iumKkDctXHoN4bGB3csKOA0UrGGg==; PIM-SESSION-ID=gLmA3eizA9B89gkq; rxVisitor=1712306864068G5UJ3RFDDJIEJSC3034M03UM5IIFGUTR; dtSa=-; RT="z=1&dm=te.com&si=snv1dtjwdec&ss=lu9fls1k&sl=0&tt=0"; SSO=guestusr@te.com; SMIDENTITY=GYKoZKVS02vIjDZlDz3RqeftS8otByhP4QdLi3mORNCT6JE0roPzV+/IqBriO6VDE+bOmX/4k9FjuB3o91Ag1SQtHKJq1fLzdm8P6+7aSqvVuYynE6rBzhyo5VOvbpRmUz/8In5AUP0GpgB4p3peP83up55+2iBvqHhQiqJ4McLiMJSkvJ+mCavhWTXk8C1N70C177zzv3TahvYT10twJUbjLxExD14T5KZYCAkNDDT3xXoC1qKYBpRE/2UemsxWtsYVngUXpphXe08Vjo8zUtX+SSMGjBznViRkmcoM5rUXYbNW9xx85GD4E8iKZA4cSC+/PrhoDlFHJ/aJig3PH9U33FIBCeuvcvEXzTBAOv0hRJCqc7Qn5NYeWpeVK9ncupiTdZmKjIJ6GWqU+8qQCn+fZ0LzxlSXKm9egxFeAESQTF+3bL0xffQY+kZD7VvrPC1vsxt0oZRIaO7BHCx3xyDHQJ2HBfXfpK2IGYL83hJlJ0JrImi81s9C9vHeuMcx51AoUfJr39w3kycdN5C+Zxlp9J0sMhfiI85o+grO6o5/eaFJQKoinTacUKh4Oll7; _ga_7XPK4TC9TD=GS1.1.1712306872.11.0.1712306872.60.0.0; _ga=GA1.2.729334068.1697120363; _gid=GA1.2.535302352.1712306872; _gat_UA-71955962-1=1; IR_gbd=te.com; IR_10771=1712306865591%7C2083231%7C1712306865591%7C%7C; AMCVS_A638776A5245AFE50A490D44%40AdobeOrg=1; AMCV_A638776A5245AFE50A490D44%40AdobeOrg=-432600572%7CMCIDTS%7C19819%7CMCMID%7C58648963887400562022220646830085753637%7CMCAAMLH-1712911674%7C9%7CMCAAMB-1712911674%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1712314074s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.5.2; _dtm_v1=1712306874755%2C1712144103262%2C1711536592147%2C5; rxvt=1712308681033|1712306864071; dtPC=1$506864067_641h-vASRRRJFWNACDGKFIULULIAKKFEWDQANA-0e0; bm_sv=2AD3D10070AC7A9FA75A84FD6B641C45~YAAQEKMTApaIiKKOAQAAgtZxrRfGVUIdZQvCSjXFwa0mY/zawWKNCa31w+JQjzHfrWhDETctEkv77fpQP0EvoMM/mEiLJyf58we25FPMhMXVKt98ylsTCBJvp9Rl4R5wvnADWolzMytG2L2Rh4a2p+s/gtswc0fw5+5tz7088ZmBRCiQms8Nv7GCFftFDvW3rs2d4G6sQo8K9tDEocz+8uLbygzNlMZuH5EkGhlw179vmCZo1KdzODEmQR4=~1; s_tp=3701; s_cc=true; s_ppv=products%253Aproduct%2520001308%2520000%2C11%2C8%2C420; _dtm_v=1712306889927%2C1712306884895%2C1712143963077%2C9',
        # 'If-Modified-Since': 'Fri, 05 Apr 2024 08:47:58 GMT',
        # 'If-None-Match': 'W/"4c366-61555834c025d:dtagent10285240307101407HFPn"',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'none',
        # 'Sec-Fetch-User': '?1',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',

    }
    item={}
    for i in range(max_retires):
        # urls = f"http://api.scraperapi.com?api_key=de51e4aafe704395654a32ba0a14494d&url={pdp_url}"
        urls = f"http://api.scrape.do?url={pdp_url}&token={token}"

        url_request = requests.get(url=urls,headers=headers)
        if url_request.status_code == 200:
            break

    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}

    if 'class="part-basic-detail-value"' not in url_request.text:
        error['statusCode'] = 410
        error['error_message'] = 'Product not found'
        return error

    item['vendor'] = vendor
    item['pdp_url'] = pdp_url
    response = Selector(text=url_request.text)
    try:
        item['sku']  = response.xpath('//div[@id="te-page"]//li[@class="product-tcpn"]/span[@class="part-basic-detail-value"]//text()').get()
        if item['sku'] != sku:
            error['statusCode'] = 410
            error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
            return error
        else:
            pass
    except Exception as e:
        error['statusCode'] = 500
        error['error_message'] = str(e)
        return error


    item['sku'] = sku

    abd = response.xpath('//script[contains(text(),"schema.org")]//text()').get()
    data = abd.strip().replace('\n', '').replace('\t', '')
    InStock=''
    data1 = json.loads(data)
    # print(data1)
    off_ = data1.get('offers')
    if off_:
        d = data1['offers']['availability']
        if 'InStock' in d:
            InStock = True

        else:
            InStock = False
            # product_loader.add_value('estimated_lead_time', '')
    else:
        InStock = False

    headers =  {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.te.com',
    'priority': 'u=1, i',
    'referer': 'https://www.te.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    urls = f'https://api.te.com/api/v1/exp-tecom-commerce-api/b2c/price-inventory/products?tcpn={sku}&country=usa&language=en'
    requests_url = requests.get(url=urls, headers=headers)
    data = json.loads(requests_url.text)

    try:
        price_on=data['orderable']
    except:
        price_on=False
    price_list = []
    lead_time = []
    if price_on==True:
        off_1 = data.get('prices')
        if off_1:
            for i in data['prices']:
                price = i['formattedValue']
                min_qty = i['minQuantity']
                price = price.replace("$", "").replace(",", "")
                price_list.append({
                    "currency": "USD",
                    'min_qty': min_qty,
                    'price': float(price)
                })
        else:
            price_list.append({
                'min_qty': 1,
                'price_string': 'Call for price'
            })

        if InStock == True:
            standardLeadTime = data['stock']['standardLeadTime']
            if standardLeadTime != 0:
                min_qty = data["stockMetaData"]["minimumOrderQuantity"]
                lead_time.append(
                    {"min_qty": min_qty, "time_to_ship": {"raw_value": f"Ships within {standardLeadTime} days"}})
            else:
                lead_time.append({"min_qty": 1, "time_to_ship": {"raw_value": "SHIPS IMMEDIATELY"}}
                                 )
        else:
            pass

        if price_list:
            item['price'] = price_list
        else:
            item['price'] = None

        item['lead_time'] = lead_time
        item['available_to_checkout'] = InStock
        item['in_stock'] = InStock


    else:
        price_list.append({
            'min_qty': 1,
            'price_string': 'Call for price'
        })
        item['price'] = price_list
        item['lead_time'] = lead_time
        item['available_to_checkout'] = InStock
        item['in_stock'] = InStock

    # return item
    if item['lead_time'] == []:
        item['lead_time'] = None

    return {'statusCode': 200,
            'data': item}

# if __name__ == '__main__':
#     # event = {"sku": "T4111502041-000", "vendor": "teconnectivity", "pdp_url": "https://www.te.com/usa-en/product-T4111502041-000.html"}
#     # event = {"sku": "1-2212115-4", "vendor": "teconnectivity", "pdp_url": "https://www.te.com/usa-en/product-1-2212115-4.html"}
#     event = {"sku": "1-1423673-7", "vendor": "teconnectivity", "pdp_url": "https://www.te.com/en/product-1-1423673-7.html"}
#     print(json.dumps(teconnectivity(pdp_url=event['pdp_url'], sku=event['sku'])))
