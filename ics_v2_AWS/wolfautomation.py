import json# install json
from parsel import Selector# intsall parsel
import requests
# from curl_cffi import requests# intsall curl_cff
import html
max_retires=5
import api_key

token=api_key.scraperDo_key

headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'cookie': 'fornax_anonymousId=f2c250a1-caa1-4ffe-aa8d-e0ebf26a36a1; SHOP_SESSION_TOKEN=2f2dd955-dfff-4ef4-a36b-4164348495a4; _ga=GA1.1.1410795977.1718713163; _gcl_au=1.1.1569441600.1718713164; slaask-token-4942661a6129894e87c5d58535c280f5=ujkx4wgtde9rnet6d7cmdfn1kwn80u2e04299t4vj47l; XSRF-TOKEN=5d9075b03208b543854585218361fbf5abc5e631acff4fafcf4faf5addf9b2e2; _ga_MDXCZSCE0N=deleted; athena_short_visit_id=64e22dc8-fb21-4446-99da-14e54b55f132:1719321324; __kla_id=eyJjaWQiOiJZV0l6WldRM05EWXRZVE5pWXkwME0yTTNMV0UzWWpVdFltUXhaak5rTkRVeU9HSXoiLCIkcmVmZXJyZXIiOnsidHMiOjE3MTg3MTMxNjIsInZhbHVlIjoiaHR0cHM6Ly93d3cud29sZmF1dG9tYXRpb24uY29tL3NhZmV0eS1saWdodC1jdXJ0YWluLXJlY2VpdmVyLTIyNW1tLWhlaWdodC0xP19fY2ZfY2hsX3RrPWkxRlZWLjY0elQyOV80Tk1ZSGVmczd0dVNDaEx6TmVRbkkyVzU5bHNOakEtMTcxODcxMzE1My0wLjAuMS4xLTQxMTYiLCJmaXJzdF9wYWdlIjoiaHR0cHM6Ly93d3cud29sZmF1dG9tYXRpb24uY29tL3NhZmV0eS1saWdodC1jdXJ0YWluLXJlY2VpdmVyLTIyNW1tLWhlaWdodC0xIn0sIiRsYXN0X3JlZmVycmVyIjp7InRzIjoxNzE5MzIxMzI2LCJ2YWx1ZSI6Imh0dHBzOi8vd3d3LndvbGZhdXRvbWF0aW9uLmNvbS9tczY2bS1mZmYtYi1iZWFjb24tNjZtbS1kaWFtZXRlci1sZWQtc3RlYWR5LWY/X19jZl9jaGxfdGs9MjkuSU4uMXFTRGguVW5fcVBPRWRRRGcwYjJsTFlkUFU1ckxuNU01VmNMRS0xNzE5MzIxMzAzLTAuMC4xLjEtODM2MSIsImZpcnN0X3BhZ2UiOiJodHRwczovL3d3dy53b2xmYXV0b21hdGlvbi5jb20vbXM2Nm0tZmZmLWItYmVhY29uLTY2bW0tZGlhbWV0ZXItbGVkLXN0ZWFkeS1mIn19; STORE_VISITOR=1; cf_clearance=h3CGl3KzqkRlyHW3_ldzRYMUeQRRPo6s9GIwDS6w1GE-1719321326-1.0.1.1-is2m6KbcjEm5_vW9jGRJZVprtGKiHay6CvajLqUBMF6f2igP18dnh1KRundp_flu4Kt5KtUD3z0g3p05kNYCfg; _uetsid=e1edd910322811ef9180eb8bc961a2cd|1pifoar|2|fmx|0|1636; Shopper-Pref=889563AEF651736BA23CF39DE044B52F0E7E67CE-1719926132088-x%7B%22cur%22%3A%22USD%22%7D; _uetvid=11f436302d3411efa801099b5c482d19|enm6ow|1719321336157|1|1|bat.bing.com/p/insights/c/w; _ga_MDXCZSCE0N=GS1.1.1719321327.9.1.1719321377.10.0.0; SHOP_SESSION_TOKEN=2f2dd955-dfff-4ef4-a36b-4164348495a4; Shopper-Pref=21FC186CBA3041E55E893CA888B246A1F3922095-1719926283990-x%7B%22cur%22%3A%22USD%22%7D; athena_short_visit_id=64e22dc8-fb21-4446-99da-14e54b55f132:1719321324; fornax_anonymousId=f2c250a1-caa1-4ffe-aa8d-e0ebf26a36a1',
  # 'priority': 'u=0, i',
  # 'referer': 'https://www.wolfautomation.com/ms66m-fff-b-beacon-66mm-diameter-led-steady-f?__cf_chl_tk=29.IN.1qSDh.Un_qPOEdQDg0b2lLYdPU5rLn5M5VcLE-1719321303-0.0.1.1-8361',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
  'sec-ch-ua-arch': '"x86"',
  'sec-ch-ua-bitness': '"64"',
  'sec-ch-ua-full-version': '"126.0.6478.63"',
  'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.63", "Google Chrome";v="126.0.6478.63"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-model': '""',
  'sec-ch-ua-platform': '"Windows"',
  'sec-ch-ua-platform-version': '"10.0.0"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}


def wolfautomation(pdp_url, sku, vendor='wolfautomation'):
    try:
        if 'https://www.wolfautomation.com/' not in pdp_url:
            return {"statusCode": 410,
                    "error_message": "Product not found"}
        item = {}
        error={}
        pdp_urls =  f"http://api.scrape.do?token={token}&url={pdp_url}"
        for i in range(max_retires):
            url_request = requests.get(pdp_urls)
            if url_request.status_code == 404:
                error['statusCode'] = 410
                error['error_message'] = 'Product not found'
                return error
            if url_request.status_code == 200:
                break
        if url_request.status_code == 200:
            pass
        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}
        response = Selector(text=url_request.text)
        # ------------------------------------ product_sku and Pdp_url below -------------------------------------------
        product_sku = response.xpath('//div[@class="ob-product-name-row ob-full-name-row"]//h1/text()').get()
        if product_sku:
            product_sku=product_sku.strip()
            # if product_sku.startswith('.'):
            #     product_sku = product_sku.replace('.', '')
            # else:
            #     product_sku = product_sku

        if product_sku != sku:
            return {"statusCode": 410,
                    "error_message": f"Scraped SKU:{product_sku} does not match input SKU:{sku}"}

        # -------------------------------------- product_sku and Pdp_url above -----------------------------------------

        # ------------------------------------------ price code below --------------------------------------------------
        price_element = response.xpath('//div[@class="price-section price-section--withoutTax"]/span/text()').get()
        final_price = []
        if price_element != 0:
            if "," in str(price_element):
                price = price_element.replace(',', '').replace('$', '')
                price = float(price)
            else:
                price = price_element.replace('$', '')
                price = float(price)
        else:
            price = None

        min_qty = response.xpath('//div[@class="form-increment"]//input[@class="form-input form-input--incrementTotal"]/@value').get('').strip()
        if min_qty.isdigit():
            min_qty = int(min_qty)
        else:
            min_qty = 1
        if price:
            final_price.append(
                {"min_qty": min_qty, "price": price, "currency": "USD"})
        else:
            final_price.append(
                {"min_qty": 1, "price_string": 'Call For Price'})

            # else:
            #     return {'statusCode': 410,
            #                 "error_message": "Product is discontinued" }
        # ----------------------------------------- price code above  --------------------------------------------------

        # ----------------------------------- Add in_stock and available_to_checkout -----------------------------------

        in_stock1 = response.xpath('//div[@class="ob-availability-row ob-desktop"]/span[2]/text()').get()
        if in_stock1:
            if 'in stock' in in_stock1 and in_stock1 != None and in_stock1 != '':
                in_stock = True
            else:
                in_stock = False
        else:
            in_stock = False
        available_to_checkout1 = response.xpath('//div[@class="ob-cart-actions-row"]/button/text()').get('').strip()
        if available_to_checkout1:
            available_to_checkout = True
        else:
            available_to_checkout = False
        item['vendor']=vendor
        item['sku'] = product_sku
        item['pdp_url'] = pdp_url
        if  final_price!= []:
            item['price'] = final_price
        else:
            item['price_string'] = final_price
        item['available_to_checkout'] = available_to_checkout
        item['in_stock'] = in_stock
        item['lead_time'] = None
        return {'statusCode': 200,
                'data': item}
    except Exception as e:
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}


#Input Params
# vendor = "wolfautomation"
# sku = 'MS66M-FFF-B'
# pdp_url = 'https://www.wolfautomation.com/ms66m-fff-b-beacon-66mm-diameter-led-steady-f'
# print(json.dumps(wolfautomation(pdp_url,sku,vendor)))

