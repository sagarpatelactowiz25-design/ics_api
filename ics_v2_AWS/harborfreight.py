import json

import pymysql
import requests
from parsel import Selector

max_retries=5
def harborfreight(pdp_url,sku,vendor="harborfreight"):
    try:

        url=f'https://api.scrape.do/?token=f42a5b59aec3467e97a8794c611c436b91589634343&url={pdp_url}&render=true'
        for i in range(max_retries):
            url_request = requests.get(url=url)

            if url_request.status_code == 200:
                break
        else:
            return {'statusCode': 408,'error_message': 'Request timeout, failed to reach host'}

        resp_url=Selector(url_request.text)
        if url_request.status_code == 200 and resp_url.xpath('(//div[@class="product__title--DhrmCg"]/h1/text())[2]').get():
            response = Selector(text=url_request.text)

            j_data=response.xpath('//script[contains(text(), "__APOLLO_STATE__")]//text()').get()
            try:
                data = json.loads(j_data.split("=", 1)[-1][:-1])
            except Exception as ee:
                pass
            ld_json = json.loads(response.xpath('//script[@type="application/ld+json" and re:match(text(), \'"Product"\')]/text()').get('{}'))
            Vendor=vendor

            try:
                # sku=data["SimpleProduct:13377"]["agg_parent_product"]["sku"]
                # sku=data["SimpleProduct:15187.additional[0].value"]
                scraped_sku=resp_url.xpath('(//span[@class="product__sku--enhaMx"]/text())[2]').get().strip()
            except:
                scraped_sku=None

            if scraped_sku == sku:
                pass
            else:
                return {'statusCode': 410,
                        'error_message': f'Scraped SKU:{scraped_sku} does not match input SKU:{sku}'}

            min_qty=resp_url.xpath('//div[@data-testid="quantityWrap"]//input/@value').get()
            if min_qty:
                min_qty=int(min_qty)
            else:
                min_qty=1

            try:
                price_final=ld_json["offers"]["price"]
                if price_final:
                    price= [{'min_qty':min_qty,"price":float(price_final),"currency":"USD"}]
                else:
                    price = [{'min_qty': min_qty, 'price_string': "Call For Price",}]
            except:
                price=price = [{'min_qty': min_qty, 'price_string': "Call For Price",}]

            try:
                available=ld_json["offers"]["availability"]
                if not available.endswith('InStock'):
                    instock=False
                    available_to_checkout=False
                else:
                    instock = True
                    available_to_checkout = True
            except:
                instock = False
                available_to_checkout = False

            # data_json={"Vendor":vendor,"pdp_url":pdp_url,"name":Product_name,"sku":sku,"price":price,"breadcrumb":breadcrumb,"manufacturer":manufacturer,"description":description,"attributes":attributes,"available_to_checkout":available_to_checkout,"instock":instock,"main_image":main_image,"images":images}
            data_json={"vendor":vendor,"pdp_url":pdp_url,"sku":scraped_sku,"price":price,"available_to_checkout":available_to_checkout,"in_stock":instock,"lead_time":None}
            return {"statusCode":200,
                    'data': data_json
                    }
        else:
            return {'statusCode': 410,
                    'error_message': 'Product not found'}
    except Exception as e:
            return {"statusCode": 500,
                    "error_message": "Internal server error" + str(e)}

# if __name__ == '__main__':
#     event={"sku": "63739", "vendor": "harborfreight", "pdp_url": "https://www.harborfreight.com/collections/automotive-tools/locking-lug-nut-master-key-set-16-piece-63739.html"}
#     url='https://www.harborfreight.com/collections/woodworking/woodworking-accessories/8-inch-crimped-brass-wire-wheel-93467.html'
#     sku="9346"
#     print(json.dumps(harborfreight(event['pdp_url'],event['sku'])))
# if __name__ == '__main__':
#     event={"sku": "57194", "vendor": "harborfreight", "pdp_url": "https://www.harborfreight.com/collections/automotive-tools/cyclone-dust-separator-kit-for-5-gallon-buckets-57194.html"}

