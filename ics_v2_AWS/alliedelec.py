import json
import random
import time
import requests
from parsel import Selector

def datadom():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://us.rs-online.com',
        'priority': 'u=1, i',
        'referer': 'https://us.rs-online.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }
    data = 'jsData=%7B%22ttst%22%3A9.699999988079071%2C%22ifov%22%3Afalse%2C%22hc%22%3A16%2C%22br_oh%22%3A816%2C%22br_ow%22%3A1536%2C%22ua%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F127.0.0.0%20Safari%2F537.36%22%2C%22wbd%22%3Afalse%2C%22dp0%22%3Atrue%2C%22tagpu%22%3A9.738121195946311%2C%22wdif%22%3Afalse%2C%22wdifrm%22%3Afalse%2C%22npmtm%22%3Afalse%2C%22br_h%22%3A730%2C%22br_w%22%3A508%2C%22isf%22%3Afalse%2C%22nddc%22%3A1%2C%22rs_h%22%3A864%2C%22rs_w%22%3A1536%2C%22rs_cd%22%3A24%2C%22phe%22%3Afalse%2C%22nm%22%3Afalse%2C%22jsf%22%3Afalse%2C%22lg%22%3A%22en-US%22%2C%22pr%22%3A1.25%2C%22ars_h%22%3A816%2C%22ars_w%22%3A1536%2C%22tz%22%3A-330%2C%22str_ss%22%3Atrue%2C%22str_ls%22%3Atrue%2C%22str_idb%22%3Atrue%2C%22str_odb%22%3Afalse%2C%22plgod%22%3Afalse%2C%22plg%22%3A5%2C%22plgne%22%3Atrue%2C%22plgre%22%3Atrue%2C%22plgof%22%3Afalse%2C%22plggt%22%3Afalse%2C%22pltod%22%3Afalse%2C%22hcovdr%22%3Afalse%2C%22hcovdr2%22%3Afalse%2C%22plovdr%22%3Afalse%2C%22plovdr2%22%3Afalse%2C%22ftsovdr%22%3Afalse%2C%22ftsovdr2%22%3Afalse%2C%22lb%22%3Afalse%2C%22eva%22%3A33%2C%22lo%22%3Afalse%2C%22ts_mtp%22%3A0%2C%22ts_tec%22%3Afalse%2C%22ts_tsa%22%3Afalse%2C%22vnd%22%3A%22Google%20Inc.%22%2C%22bid%22%3A%22NA%22%2C%22mmt%22%3A%22application%2Fpdf%2Ctext%2Fpdf%22%2C%22plu%22%3A%22PDF%20Viewer%2CChrome%20PDF%20Viewer%2CChromium%20PDF%20Viewer%2CMicrosoft%20Edge%20PDF%20Viewer%2CWebKit%20built-in%20PDF%22%2C%22hdn%22%3Afalse%2C%22awe%22%3Afalse%2C%22geb%22%3Afalse%2C%22dat%22%3Afalse%2C%22med%22%3A%22defined%22%2C%22aco%22%3A%22probably%22%2C%22acots%22%3Afalse%2C%22acmp%22%3A%22probably%22%2C%22acmpts%22%3Atrue%2C%22acw%22%3A%22probably%22%2C%22acwts%22%3Afalse%2C%22acma%22%3A%22maybe%22%2C%22acmats%22%3Afalse%2C%22acaa%22%3A%22probably%22%2C%22acaats%22%3Atrue%2C%22ac3%22%3A%22%22%2C%22ac3ts%22%3Afalse%2C%22acf%22%3A%22probably%22%2C%22acfts%22%3Afalse%2C%22acmp4%22%3A%22maybe%22%2C%22acmp4ts%22%3Afalse%2C%22acmp3%22%3A%22probably%22%2C%22acmp3ts%22%3Afalse%2C%22acwm%22%3A%22maybe%22%2C%22acwmts%22%3Afalse%2C%22ocpt%22%3Afalse%2C%22vco%22%3A%22%22%2C%22vcots%22%3Afalse%2C%22vch%22%3A%22probably%22%2C%22vchts%22%3Atrue%2C%22vcw%22%3A%22probably%22%2C%22vcwts%22%3Atrue%2C%22vc3%22%3A%22maybe%22%2C%22vc3ts%22%3Afalse%2C%22vcmp%22%3A%22%22%2C%22vcmpts%22%3Afalse%2C%22vcq%22%3A%22%22%2C%22vcqts%22%3Afalse%2C%22vc1%22%3A%22probably%22%2C%22vc1ts%22%3Atrue%2C%22dvm%22%3A8%2C%22sqt%22%3Afalse%2C%22so%22%3A%22landscape-primary%22%2C%22wdw%22%3Atrue%2C%22cokys%22%3A%22bG9hZFRpbWVzY3NpYXBwcnVudGltZQ%3D%3DL%3D%22%2C%22ecpc%22%3Afalse%2C%22lgs%22%3Atrue%2C%22lgsod%22%3Afalse%2C%22psn%22%3Atrue%2C%22edp%22%3Atrue%2C%22addt%22%3Atrue%2C%22wsdc%22%3Atrue%2C%22ccsr%22%3Atrue%2C%22nuad%22%3Atrue%2C%22bcda%22%3Afalse%2C%22idn%22%3Atrue%2C%22capi%22%3Afalse%2C%22svde%22%3Afalse%2C%22vpbq%22%3Atrue%2C%22ucdv%22%3Afalse%2C%22spwn%22%3Afalse%2C%22emt%22%3Afalse%2C%22bfr%22%3Afalse%2C%22dbov%22%3Afalse%2C%22cfpfe%22%3A%22RXJyb3I6IENhbm5vdCByZWFkIHByb3BlcnRpZXMgb2YgbnVsbA%3D%3D%22%2C%22stcfp%22%3A%22M2Z0NDR5NDQ4TnhIcE1mNDE6MTozOTk1NykKICAgIGF0IGEgKGh0dHBzOi8vdXMucnMtb25saW5lLmNvbS92aWV3L2J1bmRsZXMvanF1ZXJ5LW9ubHktc2NyaXB0cz92PTIzNURlQ1J5YzJLS3RtNS11LVdvd2FHbVdIVTNmdDQ0eTQ0OE54SHBNZjQxOjE6NDAyNjUp%22%2C%22ckwa%22%3Atrue%2C%22prm%22%3Atrue%2C%22tzp%22%3A%22Asia%2FCalcutta%22%2C%22cvs%22%3Atrue%2C%22usb%22%3A%22defined%22%2C%22emd%22%3A%22k%3Aai%2Cvi%2Cao%22%2C%22glvd%22%3A%22Google%20Inc.%20(Intel)%22%2C%22glrd%22%3A%22ANGLE%20(Intel%2C%20Intel(R)%20Iris(R)%20Xe%20Graphics%20(0x000046A6)%20Direct3D11%20vs_5_0%20ps_5_0%2C%20D3D11)%22%2C%22wwl%22%3Afalse%2C%22jset%22%3A1722931790%7D&eventCounters=%5B%5D&jsType=ch&cid=MHlQrFSxuA8aDUsj04lO3v0u85dWFiYcuMoercKX5flGsLPlsZ~JBH8WXKWqN8iiRr4Qx7F~FaznaN403KfwZoAfOAByyqugNs5o5KOo01OmEYrb4CRIRy_2BDPQ9i7E&ddk=7D79E840AC75256A7237A6A4517118&Referer=https%253A%252F%252Fus.rs-online.com%252Fproduct%252Fsick%252Fwtm10l-241612d0a00zwzzzzzzzzz1%252F75115458%252F&request=%252Fproduct%252Fsick%252Fwtm10l-241612d0a00zwzzzzzzzzz1%252F75115458%252F&responsePage=origin&ddv=4.32.5'

    response = requests.post('https://api-js.datadome.co/js/', headers=headers, data=data)
    datadom_key = ((json.loads(response.text)['cookie']).split(';')[0]).replace('datadome=','')
    return datadom_key

def alliedelec(url, sku, vendor='alliedelec'):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': f'datadome={datadom()}',
        'priority': 'u=0, i',
        'referer': url,
        'sec-ch-device-memory': '8',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.89", "Chromium";v="127.0.6533.89"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    try:
        url_request = str()
        error = dict()
        try:
            max_retires = 5
            for i in range(max_retires):
                time.sleep(2)
                # final_url = f'http://api.scraperapi.com?api_key=6f507304665b4976de10f9e4cdd1b5f0&url={url}&keep_headers=true'
                url_request = requests.get(url, headers=headers)
                if url_request.status_code == 200:
                    break
            else:
                # The function must have logic for retries Max. 5
                # If request fails after 5 retries it should return following
                return {'statusCode': 408,
                        'error_message': 'Request timeout, failed to reach host'}
        except Exception as e:
            print(e)

        if 'class="allied-stock-number"' not in url_request.text:
            error['statusCode'] = 404
            error['error_message'] = 'Product not found'
            return error

        response = Selector(url_request.text)
        if 'PRODUCT DISCONTINUED' in url_request.text:
            return {"statusCode": 410,
                    "error_message": "Product is discontinued"}
        else:
            item = dict()
            item['vendor'] = vendor

            # sku Extracting :-
            try:
                item['sku'] = response.xpath("//span[@class='allied-stock-number']//span[@class='OneLinkNoTx']/text()").get()
                if item['sku'] != sku:
                    error['statusCode'] = 404
                    error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
                    return error
                else:
                    pass
            except Exception as e:
                error['statusCode'] = 500
                error['error_message'] = str(e)
                return error

            item['pdp_url'] = url

            price_list = []
            discontinue = response.xpath('//span[@class="pdp-purchase-button-disabled-label"]/text()').get()

            price_111 = response.xpath('//div[contains(@class,"price-scale")]')
            for abhi in price_111:
                item_price = {}
                qty = abhi.xpath(".//p[@class='align-left bodytag pricing-quantity']//text()").get()
                item_price['min_qty'] = int(qty)
                item_price['currency'] = 'USD'
                price_s = abhi.xpath(
                    ".//p[@class='align-right bodytag special-pricing-price decimal-price-display']/text()").get()
                price_a = abhi.xpath(
                    ".//p[@class='align-right bodytag standard-pricing-price decimal-price-display']/text()").get()
                item_price['price'] = float(price_s[1:].replace(',', '')) if price_s else (
                    float(price_a[1:].replace(',', '')) if price_a else "call for price")
                price_list.append(item_price)
            item['price'] = price_list

            in_stock = response.xpath(
                "//div[@class='availability-value in-stock-message']/p[@class='align-right bodytag']/text()").get()
            item['in_stock'] = bool(in_stock)

            if discontinue and 'PRODUCT NOT AVAILABLE' in discontinue:
                item['available_to_checkout'] = False
            else:
                add_to_cart = response.xpath('//button[@class="submit-button-red text-center"]/span/text()').get()
                item['available_to_checkout'] = bool(add_to_cart)

            estimated_lead_time1 = response.xpath(
                "//p[@class='bodytag align-left'][contains(text(), 'Manufacturer Lead Time')]//following-sibling::p/text()").get()
            if estimated_lead_time1:
                estimated_lead_time2 = estimated_lead_time1.replace(':', '')
                item['lead_time'] = [{'min_qty': 1, 'time_to_stock': {"raw_value": estimated_lead_time2}}]
            else:
                item['lead_time'] = None

            return {"statusCode": 200, "data": item}

    except Exception as e:
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}

# if __name__ == '__main__':
#     # parse function call with products_url and sku :-
#     url_list = [
# "https://us.rs-online.com/product/mean-well-usa/sd-1000h-24/70069884/",
# "https://us.rs-online.com/product/mean-well-usa/sd-1000h-48/70069885/",
# "https://us.rs-online.com/product/mean-well-usa/sd-1000l-48/70069882/",
# "https://us.rs-online.com/product/eaton-cutler-hammer/10250tlp76stamp/72667274/",
# "https://us.rs-online.com/product/eaton-cutler-hammer/10250tr20stamp/72667383/",
# "https://us.rs-online.com/product/eaton-cutler-hammer/10250tr30stamp/72667387/"
# "https://us.rs-online.com/product/american-electrical-inc/c5a1p/70037586/",
# "https://us.rs-online.com/product/te-amp/1-178288-3/70086857/",
# "https://us.rs-online.com/product/c-k-components-llc/7105j16zqe22/70128173/",
# "https://us.rs-online.com/product/bussmann-electrical/non-5/70149298/"
# ]
#     for ii in url_list:
#         data = alliedelec(
#             url=f"{ii}",
#             sku=f"{ii.split('/')[-2]}")
#         # print json :-
#         print(data)
