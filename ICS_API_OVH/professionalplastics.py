import json# install json
from curl_cffi import requests
from parsel import Selector
max_retires = 5

def professionalplastics(pdp_url,sku,vendor):

    for i in range(max_retires):
        response_data = requests.get(pdp_url.replace(' ', '%20'), impersonate='chrome110')
        if response_data.status_code == 200:
            break

    else:
        return {'statusCode': 408,
                'error_message': 'Request timeout, failed to reach host'}
    error_dict ={}

    if response_data.status_code==200 and "Cut Tolerance" not in response_data.text and '<script language="JavaScript">' in response_data.text:
        response = Selector(text=response_data.text)
        sku=''
        sku_list = []
        slug1_list = []
        slug0_list = []
        slug2_list = []
        if not (response.xpath('//div[@class="tabcalc"]/button/text()').getall())[0]=='REQUEST A QUOTE':
            # if int(float(response.xpath("count(//div[@class='tabcalc']/button)").get()))<3 and int(float(response.xpath('count(//span[@class="calcflex"]//thead//td)').get()))==5:
            if 1:

                variations = ((" ".join(response_data.text.split("new Array();")[1:]).split("</script>"))[0]).split(";")
                for variation in variations[:-1]:
                    slug1 = ((response_data.text.split("prrfnbr=")[1]).split("&"))[0]
                    slug2 = ((variation.split('"')[1]).split(":"))[0]

                    #print(variation)
                    slug0 = ((variation.split("c")[1]).split("c"))[0]
                    sku=''
                    try:
                        sku=((variation.split("jpg:--:")[1]).split('"'))[0]
                    except:
                        pass
                    try:
                        sku=((variation.split("png:--:")[1]).split('"'))[0]
                    except:
                        pass
                    try:
                        sku=((variation.split("gif:--:")[1]).split('"'))[0]
                    except:
                        pass
                    try:
                        sku=((variation.split("jpeg:--:")[1]).split('"'))[0]
                    except:
                        pass
                    sku_list.append(sku)
                    if sku== sku:
                        slug0_list.append(slug0)
                        slug1_list.append(slug1)
                        slug2_list.append(slug2)


        # slug2 = ((variation.split('"')[1]).split(":"))[0]

        params = {
            'prrfnbr': f'{slug1_list[0]}',
            'child': f'{slug2_list[0]}',
            'qty': '1',
            'calc': 'calc' + f'{slug0_list[0]}',
        }

        res_price = requests.get(pdp_url, params=params, impersonate='chrome110')

        res_price = Selector(text=res_price.text)

        price_list = []

        min_qty_data = res_price.xpath('//td[@data-label="QTY"]/input/@value').get()
        price_data = res_price.xpath("//meta[@itemprop='price']/@content").get()

        add_to_cart = res_price.xpath("//img[@alt='Add To Cart']/parent::a/@href")
        if add_to_cart:
            in_stock = True
            available_to_checkout = True
        else:
            in_stock = False
            available_to_checkout = False

        if not price_data  is None and price_data:
            if not min_qty_data:
                min_qty_data =1

            price_list.append({"min_qty":int(min_qty_data),"price":float(price_data),"currency":"USD"})
        elif response.xpath('//span[@class="calcflex"]'):
            main_property_headers = response.xpath('//span[@class="calcflex"]')
            attr_first_dict = {}
            for main_property_header in main_property_headers:
                sub_property_headers = main_property_header.xpath(".//tr/td/text()").getall()
                sub_property_headers = [i.replace("\n", "").replace("\t", "").strip() for i in sub_property_headers]
                sub_property_headers = [i for i in sub_property_headers if i != '']
                calc_value = main_property_header.xpath(".//input/@name").get()
                if calc_value:
                    calc_value = "c" + (((calc_value.split("_"))[0]).split("lc"))[1] + "c"
                    attr_first_dict[calc_value] = sub_property_headers

            variations = ((response_data.text.split('<script language="JavaScript">')[1]).split(" = new Array();"))[1:]
            attributes_all_headers = []

            tolerance_values = ''
            if response.xpath('//td[@data-label="Cut Tolerance"]'):
                tolerance_values = response.xpath('//td[@data-label="Cut Tolerance"]//option/text()').getall()

            cut_tol_checker = 0
            for variation in variations:
                products = variation.split(";")
                c_slug = 0
                for product in products:
                    product_statement_list = ((product.strip().lstrip()).split(":--:")[1:])

                    try:
                        c_slug = product_statement_list[0]
                        attributes_all_headers = attr_first_dict[c_slug]
                        attributes_all_headers = [i for i in attributes_all_headers if
                                                  "price" not in i and "Price" not in i]
                        if "Cut Tolerance" in attributes_all_headers:
                            cut_tolerance_index = attributes_all_headers.index("Cut Tolerance")
                            attributes_all_headers = attributes_all_headers[:cut_tolerance_index]
                            cut_tol_checker = 1
                    except:
                        pass

                    attributes_listt = []
                    try:
                        for ii in range(1, len(attributes_all_headers)):

                            attri_keyy = attributes_all_headers[ii]
                            attri_valuee = product_statement_list[ii]
                            attributes_listt.append(
                                {
                                    'name': attri_keyy,
                                    'value': attri_valuee,
                                    'group': 'Specification'
                                }
                            )
                        product_sku_1 = (product_statement_list[-1]).replace('"', '')


                        cut_value = ''
                        for jj in attributes_listt:
                            if "Cut Size (inches)" in jj.get("name"):
                                cut_value = jj.get("value")

                            if "Feet" in jj.get("name") and "Cut Size (inches)" not in jj.get("name"):
                                cut_value = jj.get("value")

                        slug1 = ((response_data.text.split("prrfnbr=")[1]).split("&"))[0]
                        slug2 = (((product.split('] = "'))[1]).split(":--:"))[0]
                        calc_slug = "calc" + c_slug.split("c")[1].split("c")[0]
                        if cut_value:
                            params = {
                                'prrfnbr': f'{slug1}',
                                'child': f'{slug2}',
                                'qty': '1',
                                'calc': f'{calc_slug}',
                                'dimension': f'{cut_value}',
                            }
                            if product_sku_1==sku:
                                sku_list.append(product_sku_1)

                                ress = requests.get(pdp_url, params=params, impersonate='chrome110')

                                ress = Selector(text=ress.text)
                                min_qty_data = ress.xpath('//td[@data-label="QTY"]/input/@value').get()
                                price_data = ress.xpath("//meta[@itemprop='price']/@content").get()
                                if price_data:
                                    if not min_qty_data:
                                        min_qty_data=1
                                    price_list.append({"min_qty": int(min_qty_data), "price": float(price_data), "currency": "USD"})
                                else:
                                    price_list = [{"min_qty": 1, "price_string": "Call for price"}]

                    except:
                        pass
        else:
            price_list = [{"min_qty": 1, "price_string": "Call for price"}]

        try:
            if sku not in sku_list:
                error_dict['statusCode'] = 404
                error_dict['error_message'] = f"Scraped SKU:{sku} does not match input SKU:{sku}"
                return error_dict
        except Exception as e:
            error_dict['statusCode'] = 500
            error_dict['error_message'] = str(e)
            return error_dict

        item = {}
        item['vendor'] = 'professionalplastics'
        item['sku'] = sku
        item['pdp_url'] = pdp_url
        item['price'] = price_list
        item['available_to_checkout'] = available_to_checkout
        item['in_stock'] = in_stock
        item['lead_time'] = None
        return {'statusCode': 200,
                'data': item}
    else:
        error_dict['statusCode'] = 404
        error_dict['error_message'] = str("404 Page not found")
        return error_dict
