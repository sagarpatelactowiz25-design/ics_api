import json# install json
import re
import time

# import requests# intall requests
from parsel import Selector# intsall parsel
from curl_cffi import requests# intsall curl_cffi
# import requests# intsall curl_cffi
# import requests
import  html

import api_token

token_api=api_token.scraperDo_key
proxy = {
    "http": f"http://{token_api}:geoCode=us@proxy.scrape.do:8080",
    "https": f"http://{token_api}:geoCode=us@proxy.scrape.do:8080"
}
# proxy ={
#     'http': 'https://scraperapi:3143fc2135b9c865bd90505c2f017f83@proxy-server.scraperapi.com:8001',
#     'https': 'https://scraperapi:3143fc2135b9c865bd90505c2f017f83@proxy-server.scraperapi.com:8001',
# }
max_retires=15
def supplyhouse(pdp_url, sku, vendor='supplyhouse'):
    try:
        error = {}
        item = {}
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.supplyhouse.com',
            'priority': 'u=0, i',
            'referer': 'https://www.supplyhouse.com/Watts-0009280-3-4-25AUB-LP-Z3-Low-Pressure-Reducing-Valve-Threaded-F-Union-Inlet-x-NPT-Threaded-F-Outlet?__cf_chl_tk=8XXUu6h3Hb7FJXSMbp3igCzC8nMQuGtUTUR7GWDeYK8-1750167172-1.0.1.1-fUPwrpcB0NI0mQOcuv1gfT7VWqTBu9d4ZaxFPinJ9yc',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"137.0.7151.104"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="137.0.7151.104", "Chromium";v="137.0.7151.104", "Not/A)Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            # 'cookie': '_gcl_au=1.1.605541392.1749815449; _pin_unauth=dWlkPU4ySTNaV05sTmpJdE1tWXhOQzAwWmpSa0xUZzNPVE10TVRkaE1HSXlPREEwTVdKaQ; _tt_enable_cookie=1; _ttp=01JXMJ1NXNFQSWYFFZG5E5WZNQ_.tt.1; ajs_anonymous_id=c00fe93c-3fa9-48b4-b2fc-f4c18c2af38d; GUEST_CHECKOUT_EXPERIMENT_GROUP=6; STICKY_CART_EXPERIMENT_GROUP=2; GLOBAL_INVENTORY_CHANGES_EXPERIMENT_GROUP=9; LOCAL_DELIVERY_REBRANDING_EXPERIMENT_GROUP=4; _fbp=fb.1.1749815451261.276564020789936558; __ssid=1e61635d3f77de2383a3631c4774b74; LPVID=MxMjI3OTkzNDcxMWRmZWFi; shScreenWidth=1280; __pr.a04=qXmRjLYpc0; __cf_bm=hvmlLqcfaDStVLOlVc2o52GZl66R1x.qketqkMe9V_E-1750167172-1.0.1.1-7vSUBWs9GLJfI7.0XQtuz9vXYZLASe9ASOdUggBeVGWOMsR_6DaPJQbDI5cjSKEgGMYI0dnLF9WWzaCzKmdTwBMSjgQTtfggd0fyKBErCrE; cf_clearance=MkiYS.ohajuwA1NTaMbNdJQQWJyDNUnLi_Q1BW5Or0c-1750167180-1.2.1.1-bL28sTUJFKK_taN_91_G740c9Idz7_3b7HGifj.jI83crbpSapfcLQ.w8Txgqq5UHS9F0PdPlXB8O0G26KXDmRDUPHaaUy3hBro_kjnXaIxMT_ukHkB_g_R2Gvb_4xBLFNjSGroVFh4sG_Q1n4b1SqR5cNLcPKBtJyUqC0nIN8V3XXT6saea._4yaHb4p9Iz3hWCzYg0vilqj2OJsq0zMckTH7CWGhF.sx4ZRJ5yrG9Usf.BwZOPk0MOLqFUsnDtHPN2CYCSAzHD7Uyl0rCbS9JXiHftjmp9ZwonhSKa4EgHN9GqPdntzRGpaKTShDop4jN3powrYFAkUGH0wzUBf0PcSzZNeubN7Wr3VziQ5bf1FlbsP.Aa9bqdPCQXZ3AX; JSESSIONID=F69D4CD48D00327D66A7D05F15D3CEB4.jvm11; _gid=GA1.2.786416335.1750167182; analytics_session_id=1750167183142; analytics_session_id.last_access=1750167183142; _uetsid=97aa83704b7f11f0b64dbdf430eeac0d|piulia|2|fwu|0|1994; ttcsid_C1UULH9LRI5O97LIN2UG=1750167182714::nz8mrI4xeP_fylfpVZ6Y.4.1750167183887; ttcsid=1750167182715::1a-k7l0-IKw9AS1OySMM.4.1750167183887; _ga=GA1.1.1603698184.1749815449; _ga_4Y14Y6B4C8=GS2.1.s1750167184$o5$g0$t1750167184$j60$l0$h0; _uetvid=a64ff3b0484c11f08cb25d28685971a4|bpq4gc|1750167184372|1|1|bat.bing-int.com/p/insights/c/l; _br_uid_2=uid%3D6847928744711%3Av%3D15.0%3Ats%3D1749815449883%3Ahc%3D8; cto_bundle=U24a319VMHl5WDNsdDhJcDhFVWpuUXRvbHFsVm1qdGFWam5HR1h0MzA3R084OVJnV1QxaElydlp6VDllb2F5Nml3cGdhc1lTbldpRkRxcDhQU3U2VzBDZFhjb2lDNTRzUWxlcW1peDFLTWhQQW5IT3pPQmkzdDBoZkdtN2lrMnFlcjQ0MXN4bVEzcEpyemJtTjA2dG9OcWFoTiUyQjMlMkZ6SWZBSCUyRnNRMVolMkY3JTJGSWsyRG9nJTNE; LPSID-7347571=vKMCzvBQQaCQHXXfOU3z1Q',
        }
        for i in range(max_retires):
            # token = "f42a5b59aec3467e97a8794c611c436b91589634343"
            # pdp_url = "http://api.scrape.do/?token={}&url={}&geoCode={}".format(token, pdp_url,"us")
            url_request = requests.get(url=pdp_url,
                                       headers=headers,
                                       impersonate = "chrome110",
                                       proxies=proxy,
                                       verify=False

                                       )
            if url_request.status_code == 200:
                break

        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}

        # if 'class="Box-sc-1z9git-0 cOgTzu"' not in url_request.text:
        #     error['statusCode'] = 404
        #     error['error_message'] = 'Product not found'
        #     return error

        item['vendor'] = vendor
        item['pdp_url'] = pdp_url
        response = Selector(text=url_request.text)
        try:
            item['sku'] =response.xpath('//div[@class="Box-sc-1z9git-0 iXetAF ProductPageHeaderDetailsValue-sc-1sia5h6-0 csKMgc"]/text()').get().strip()
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

        in_stock = response.xpath('//div[@class="Box-sc-1z9git-0 dGwTrH ProductInventoryStatusAndPromiseMessageText-sc-p14sra-0 llIxJF"]/text() | //div[@class="Box-sc-1z9git-0 jLinpV ProductInventoryStatusAndPromiseMessageText-sc-p14sra-0 llIxJF"]/text() |//div[@class="Box-sc-1z9git-0 Flex-sc-1qhr4qe-0 bXnbTp dNxDHg"]/div/text() | //div[@class="Box-sc-1z9git-0 kOSGwv ProductInventoryStatusAndPromiseMessageText-sc-p14sra-0 llIxJF"]//strong/text()').getall()
        discontinued = response.xpath('//div[@class="Box-sc-1z9git-0 bobsfl"]//text()').get()
        In_Stock=''
        if discontinued:
            if 'has been discontinued' in discontinued:
                In_Stock = False

            else:
                pass
        else:
            time_to = ''
            if in_stock:
                in_stock = ''.join(in_stock).strip()
                if 'In Stock' in in_stock:
                    In_Stock = True
                    time_to = 'time_to_arrive'
                elif 'Backorder' in in_stock:
                    In_Stock = False
                    time_to = 'time_to_stock'
                else:
                    In_Stock = False
                    time_to = None
            else:
                In_Stock = False
                time_to = None


        available_to_checkout=''
        # EXTRACTING THE PRICE USING XPATH
        price_list=[]
        # price = response.xpath('//span[@class="ProductPriceText__ProductPriceTextAmount-sc-1r9ap75-0 bPHChY"]/text()').get()
        price = response.xpath('(//span[@class="ProductPriceText__ProductPriceTextAmount-sc-1r9ap75-0 kmXLqM"]/strong/text())[2] | //span[@class="ProductPriceText__ProductPriceTextAmount-sc-1r9ap75-0 bPHChY"]/text()').get()
        if price:
            price = price.strip().lstrip().replace('\n', '').replace('$', '').replace(',', '')
        min_qty = response.xpath('//div[@class="qty-input"]/input/@data-validate').get()
        price_2 = response.xpath('//div[@class="Box-sc-1z9git-0 lahHzg ProductQuantityAdjustorsPriceTextBoxPrice-sc-13phdru-0 wyzOY"]/text()').get()
        if price:
            if min_qty:
                min_qty = int(min_qty)
            else:
                min_qty = 1
            if price:
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

        if price_2:
            price2 = price_2.split('box')[0].strip().replace('$', '').replace(',', '')
            min_qty2 = price_2.split('of')[1].strip()
            min_qty2 = int(min_qty2)
            if price2:
                price_list.append({
                    "currency": "USD",
                    'min_qty': min_qty2,
                    'price': float(price2)
                })


        price_3 = response.xpath('//div[@class="Box-sc-1z9git-0 gELBwG"]//span[1]/text()').get()
        if price_3:
            price_3 = price_3.replace('$', '').replace('each', '').replace(',', '')
            min_qty = 1
            price_list.append({
                "currency": "USD",
                'min_qty': min_qty,
                'price': float(price_3)
            })

        price_4 = response.xpath(
            '//span[@class="ProductPriceText__ProductPriceTextAmount-sc-1r9ap75-0 bOFa-DN"]/text()').get()
        if price_4:
            price_4 = price_4.replace('$', '').replace('each', '').replace(',', '')
            min_qty = 1
            price_list.append({
                "currency": "USD",
                'min_qty': min_qty,
                'price': float(price_4)
            })

        # EXTRACTING THE LEAD TIME AND CHECK PRODUCUT IS AVAILABLE USING XPATH
        estimated_lead_time = []
        min_qty_lead_time = " ".join(response.xpath('//div[contains(@class,"ProductInventoryStatusAndPromiseMessageText")]/text()').getall())
        if min_qty_lead_time:
            try:
                result = re.search(r'Get.*?(\d+)', min_qty_lead_time)
                if result:
                    digit_value = int(result.group(1))
                else:
                    digit_value= None
            except:
                digit_value=None
        else:
            digit_value= None

        if time_to is not None:
            lead_time = response.xpath('//span[@class="Box-sc-1z9git-0 iXetAF"]/text() | //span[@class="Box-sc-1z9git-0 gUKiTB"]/strong/text()').get()
            if discontinued:
                if 'has been discontinued' in discontinued:
                    estimated_lead_time = None
            else:
                if lead_time:
                    lead_time_1 = lead_time.replace('\n', '').strip()
                    lead_time = {'raw_value': lead_time_1}
                    if digit_value:
                        estimated_lead_time.append(
                            {
                                'min_qty': digit_value,
                                time_to: lead_time
                            }
                        )
                    else:

                        estimated_lead_time.append(
                            {
                                'min_qty': 1,
                                time_to: lead_time
                            }
                        )
            estimated_lead_time = estimated_lead_time

        if price_list:
            item['price'] = price_list
            available_to_checkout = True
        else:
            item['price'] = ({"min_qty": 1, "price_string": 'Call for price'})
            available_to_checkout = False
        item['lead_time'] = estimated_lead_time
        item['available_to_checkout'] = available_to_checkout
        item['in_stock'] = In_Stock

        # body = {"body": item}
        if item['lead_time'] == []:
            item['lead_time'] = None
        return {'statusCode': 200,
                'data': item}
    except Exception as e:
        return {'statusCode': 500,
        'error_message': str(e)}


# # Input Params
# if __name__ == '__main__':
#     vendor = "supplyhouse"
#     sku = 'S6310EPBN'
#     pdp_url = 'https://www.supplyhouse.com/Moen-S6310EPBN-Brushed-Nickel-1-Function-7-Diameter-Spray-Head-Eco-performance-Rainshower'
#     s = time.time()
#     print(json.dumps(supplyhouse(pdp_url,sku,vendor)))
#     e = time.time()
#     print(e-s)

