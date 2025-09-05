import requests
import json
from parsel import Selector
import re

max_retires = 5


def tacuna(pdp_url, product_sku, vendor="tacuna"):
    cookies = {
        '_gcl_au': '1.1.304045719.1713255128',
        '_ga': 'GA1.1.1278170049.1713255129',
        'mc_landing_site': 'https%3A%2F%2Ftacunasystems.com%2Fproduct-category%2Fload-cells%2F',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2024-04-17%2006%3A38%3A33%7C%7C%7Cep%3Dhttps%3A%2F%2Ftacunasystems.com%2Fproducts%2Fload-cells%2Fs-type%2Fanyload-101bs-stainless-steel-s-beam-load-cell%2F%3Fattribute_pa_capacity%3D10000lb%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2024-04-17%2006%3A38%3A33%7C%7C%7Cep%3Dhttps%3A%2F%2Ftacunasystems.com%2Fproducts%2Fload-cells%2Fs-type%2Fanyload-101bs-stainless-steel-s-beam-load-cell%2F%3Fattribute_pa_capacity%3D10000lb%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29',
        '_clck': '1ij6oj2%7C2%7Cfl0%7C0%7C1567',
        'sbjs_udata': 'vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F123.0.0.0%20Safari%2F537.36',
        'woocommerce_items_in_cart': '1',
        'wp_woocommerce_session_bc8483c9f1234e106280eb3c284ff12f': 't_10a374d3cd7a08e3a4f3f0c7400f32%7C%7C1713517129%7C%7C1713513529%7C%7Cc64f8a7e089c68a29da7c0a313d2622f',
        'woocommerce_cart_hash': '2cae099a3c2ed3261fdf60bc1524bb42',
        'sbjs_session': 'pgs%3D7%7C%7C%7Ccpg%3Dhttps%3A%2F%2Ftacunasystems.com%2Fproducts%2Fload-cells%2Fs-type%2Fanyload-101bs-stainless-steel-s-beam-load-cell%2F%3Fattribute_pa_capacity%3D1000lb',
        '_uetsid': '05664360fbc911eeb3596f26738c65a8',
        '_uetvid': '0566faf0fbc911eeb9f5357b77c93341',
        '_clsk': '16xjgnw%7C1713345411576%7C29%7C1%7Cb.clarity.ms%2Fcollect',
        '_ga_6ENNVYB8WH': 'GS1.1.1713342808.6.1.1713345416.57.0.761036333',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': '_gcl_au=1.1.304045719.1713255128; _ga=GA1.1.1278170049.1713255129; mc_landing_site=https%3A%2F%2Ftacunasystems.com%2Fproduct-category%2Fload-cells%2F; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2024-04-17%2006%3A38%3A33%7C%7C%7Cep%3Dhttps%3A%2F%2Ftacunasystems.com%2Fproducts%2Fload-cells%2Fs-type%2Fanyload-101bs-stainless-steel-s-beam-load-cell%2F%3Fattribute_pa_capacity%3D10000lb%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2024-04-17%2006%3A38%3A33%7C%7C%7Cep%3Dhttps%3A%2F%2Ftacunasystems.com%2Fproducts%2Fload-cells%2Fs-type%2Fanyload-101bs-stainless-steel-s-beam-load-cell%2F%3Fattribute_pa_capacity%3D10000lb%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29; _clck=1ij6oj2%7C2%7Cfl0%7C0%7C1567; sbjs_udata=vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F123.0.0.0%20Safari%2F537.36; woocommerce_items_in_cart=1; wp_woocommerce_session_bc8483c9f1234e106280eb3c284ff12f=t_10a374d3cd7a08e3a4f3f0c7400f32%7C%7C1713517129%7C%7C1713513529%7C%7Cc64f8a7e089c68a29da7c0a313d2622f; woocommerce_cart_hash=2cae099a3c2ed3261fdf60bc1524bb42; sbjs_session=pgs%3D7%7C%7C%7Ccpg%3Dhttps%3A%2F%2Ftacunasystems.com%2Fproducts%2Fload-cells%2Fs-type%2Fanyload-101bs-stainless-steel-s-beam-load-cell%2F%3Fattribute_pa_capacity%3D1000lb; _uetsid=05664360fbc911eeb3596f26738c65a8; _uetvid=0566faf0fbc911eeb9f5357b77c93341; _clsk=16xjgnw%7C1713345411576%7C29%7C1%7Cb.clarity.ms%2Fcollect; _ga_6ENNVYB8WH=GS1.1.1713342808.6.1.1713345416.57.0.761036333',
        'if-modified-since': 'Sat, 13 Apr 2024 18:27:39 GMT',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    try:
        # Maximum retries for urls and checking the status code is 200 or not.
        for i in range(max_retires):
            request = requests.get(pdp_url, cookies=cookies, headers=headers)
            if request.status_code == 200:
                response = Selector(text=request.text)
                break
            elif request.status_code == 404:
                return {"statusCode": 404,
                        "error_message": "Product not found"}
        else:
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}

        sku_list = []
        # Checking if status code and the product name  is also in the response text
        if request.status_code == 200 and response.xpath('//h1[@class="product_title entry-title"]'):
            sku = response.xpath('//span[@class="sku_wrapper"]/span/text()').get()

            try:
                sku_json = response.xpath(
                    '//script[@type="application/ld+json" and @class="yoast-schema-graph yoast-schema-graph--woo yoast-schema-graph--footer"]/text()').get()
                json_all = json.loads(sku_json)
                json1 = json_all["@graph"][0]["hasVariant"]
                sku_list.append(sku)
                for sku_ in json1:
                    if sku_["sku"] == product_sku:
                        text_data = sku_["offers"]["url"]
                        try:
                            attribute_pa_capacity = re.search("attribute_pa_capacity=([\w\d-]+)", text_data).group(1)
                            attribute_pa_option = re.search("attribute_pa_options=([\w\d-]+)", text_data).group(1)
                        except:
                            pass
                    sku_list.append(sku_["sku"])
            except:
                sku_list = [sku]
            # Checking product_sku is equal to sku
            if product_sku in sku_list:
                # Executing a add to cart using xpath
                add_to_cart = response.xpath(
                    '//button[@type="submit"and @class="single_add_to_cart_button button alt"]')
                available_to_checkout = True if add_to_cart else False
                # Executing in_stock using json which derive from xpath.
                try:
                    in_stock_json_xpath = json.loads(
                        response.xpath('//form[@class="variations_form cart"]/@data-product_variations').get())
                    in_stock_json_xpath = in_stock_json_xpath
                    if in_stock_json_xpath:
                        for in_stock in in_stock_json_xpath:
                            if in_stock["sku"] == product_sku:
                                variation_id = in_stock["variation_id"]
                                if in_stock["availability_html"] != "":
                                    in_stock = True
                                    break
                                else:
                                    in_stock = False
                            else:
                                in_stock = False
                    else:
                        variation_id = re.search(r'([\d]+)', response.xpath("//article/@id").get()).group()
                        params = {
                            'wc-ajax': 'get_variation',
                        }

                        data = {
                            'attribute_pa_capacity': attribute_pa_capacity,
                            'attribute_pa_options': attribute_pa_option,
                            'product_id': int(variation_id),
                        }

                        in_stock_request = requests.post('https://tacunasystems.com/?wc-ajax=get_variation',
                                                         params=params, cookies=cookies,
                                                         headers=headers, data=data)
                        in_stock_json = json.loads(in_stock_request.text)
                        if in_stock_json["sku"] == product_sku:
                            variation_id = in_stock_json["variation_id"]
                            if in_stock_json["availability_html"] != "":
                                in_stock = True
                            else:
                                in_stock = False
                        else:
                            in_stock = False



                except:
                    in_stock_xpath = response.xpath('//p[@class="stock in-stock" and text()="In stock"]')
                    in_stock = True if in_stock_xpath else False

                # Executing Price using json or xpath

                try:
                    try:
                        awdr_nonce_text = response.xpath('//script[@id="awdr-main-js-extra"]/text()').get().replace(
                            "var awdr_params = ",
                            "").replace(";", "")
                        awdr_nonce_json = json.loads(awdr_nonce_text)
                        awdr_nonce = awdr_nonce_json["nonce"]

                        data = {
                            'action': 'wdr_ajax',
                            'method': 'get_variable_product_bulk_table',
                            'product_id': str(variation_id),
                            'awdr_nonce': awdr_nonce,
                        }

                        for i in range(max_retires):
                            price_response = requests.post('https://tacunasystems.com/wp-admin/admin-ajax.php',
                                                           cookies=cookies,
                                                           headers=headers, data=data)
                            price_text = price_response.text
                            if price_text != "Invalid token" and price_text != '{"success":false}':
                                price_in_json = True
                                break
                            else:
                                if i == max_retires - 1:
                                    price_in_json = False
                        if price_in_json:
                            price_json = json.loads(price_text)
                            price_data = Selector(text=price_json["bulk_table"])

                            table_price = price_data.xpath('//table[@id="sort_customizable_table"]/tbody/tr')
                            price = []
                            for data in table_price:
                                value = data.xpath(
                                    './/td[@class="wdr_bulk_table_td wdr_bulk_range  col_index_2"]/text()').get()
                                price_value = data.xpath('.//bdi/text()').get()
                                minimum_quantity = re.search(r'\d+', value).group()
                                price.append(
                                    {'min_qty': int(minimum_quantity), 'price': float(price_value.replace(",", "")),
                                     'currency': 'USD'})
                        else:
                            table_price = response.xpath('//table[@id="sort_customizable_table"]/tbody/tr')
                            price = []

                            for data in table_price:
                                value = data.xpath(
                                    './/td[@class="wdr_bulk_table_td wdr_bulk_range  col_index_2"]/text()').get()
                                price_value = data.xpath('.//bdi/text()').get()
                                minimum_quantity = re.search(r'\d+', value).group()
                                if value and price_value:
                                    price.append(
                                        {'min_qty': int(minimum_quantity), 'price': float(price_value.replace(",", "")),
                                         'currency': 'USD'})
                                else:
                                    price = [{'min_qty': 1, 'price_string': "Call for price"}]
                                    break


                    except:
                        table_price = response.xpath('//table[@id="sort_customizable_table"]/tbody/tr')
                        price = []

                        for data in table_price:
                            value = data.xpath(
                                './/td[@class="wdr_bulk_table_td wdr_bulk_range  col_index_2"]/text()').get()
                            price_value = data.xpath('.//bdi/text()').get()
                            minimum_quantity = re.search(r'\d+', value).group()
                            if value and price_value:

                                price.append(
                                    {'min_qty': int(minimum_quantity), 'price': float(price_value.replace(",", "")),
                                     'currency': 'USD'})

                            else:
                                price = [{'min_qty': 1, 'price_string': "Call for price"}]
                except:
                    price = [{'min_qty': 1, 'price_string': "Call for price"}]

                data = {'vendor': vendor, 'pdp_url': pdp_url, 'sku': product_sku, 'price': price,
                        'lead_time': None, 'available_to_checkout': available_to_checkout,
                        'in_stock': in_stock}

                return {"statusCode": 200,
                        "data": data}

            else:
                return {"statusCode": 404,
                        "error_message": f"Scraped SKU:{product_sku} does not match input SKU:{sku}"}
        else:
            return {"statusCode": 404,
                    "error_message": "Product not found"}
    except Exception as e:
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}

