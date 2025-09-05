import re
import json
from parsel import Selector
from curl_cffi import requests


def edmundoptics(pdp_url, sku, vendor='edmunds'):

    # request to url :-
    url_request = str()
    try:
        max_retires = 5
        for i in range(max_retires):
            url_request = requests.get(url=pdp_url, impersonate='chrome110')
            if url_request.status_code == 200:
                break
        else:
            # The function must have logic for retries Max. 5
            # If request fails after 5 retries it should return following
            return {'statusCode': 408,
                    'error_message': 'Request timeout, failed to reach host'}
    except Exception as e:
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}

    if 'class="snpn"' not in url_request.text:
        error = dict()
        error['statusCode'] = 410
        error['error_message'] = 'Product not found '
        return error

    if "No longer available at Edmund Optics" not in url_request.text:

        # make Selector :-
        response = Selector(url_request.text)

        # define dictionary for making data dictionary :-
        item = dict()

        # vendor Extracting :-
        item['vendor'] = vendor

        # sku :-
        ld_json_data = None
        sku_site = str()
        if response.xpath("//div[@id='snpn-div']"):
            for ld_json in response.xpath('//script[@type="application/ld+json"]//text()').getall():
                ld_json = ld_json.replace("<sub>", "").replace("</sub>", "")
                try:
                    tmp = json.loads(ld_json)
                except:
                    ld_json = "".join([i.strip() for i in ld_json.split() if i.strip()])
                    tmp = json.loads(ld_json)
                if tmp['@type'] == "Product":
                    ld_json_data = tmp

            sku_site = ld_json_data['sku']

        item['sku'] = sku_site

        if not sku_site:
            # The function should return a dictionary having statusCode: 500;
            # If scraped sku does not match sku passed in input parameter
            return {"statusCode": 410,
                    "error_message": f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"}

        if item['sku'] != sku:
            error = dict()
            error['statusCode'] = 410
            error['error_message'] = f"Scraped SKU:{item['sku']} does not match input SKU:{sku}"
            return error

        # url :-
        item['pdp_url'] = pdp_url

        # price Extracting :-
        in_stock = False
        estimated_lead_time = list()
        in_stock_text = response.xpath("//div[@id='snpn-div']//span[@class='instock']//text()").getall()
        in_stock_text = [j.replace('\n', '').strip() for j in in_stock_text
                         if j.replace('\n', '')]
        if 'In Stock' in in_stock_text and in_stock_text:
            in_stock = True

        elif response.xpath("//div[@id='snpn-div']//span[contains(@class,'days')]//text()"):
            estimated_text = response.xpath("//div[@id='snpn-div']//span[contains(@class,'days')]//text()").getall()
            estimated_text = [k.replace('\n', '').strip() for k in estimated_text
                              if k.replace('\n', '')]
            if estimated_text:
                estimated_lead_time.append({"min_qty": 1, "time_to_ship":
                    {"raw_value": f"{' '.join(estimated_text).strip()}"}})
            in_stock = False

        if not estimated_lead_time:

            cookies = {
                'UMB_SESSION': 'CfDJ8KAWG3M62XpDvSL5Y%2BfhBSUlNEARpmuAsvC4zt8Zq1M26IkS7qx6sbfCGcEH5%2FcD%2BvA%2B%2FHxXgRfJWYV5URpLbRwRKX3BKPXVK7NR0J9qzptQQde5iSoS85y8TGJt7o%2Fi2CH6V%2FzhUAbsSy57ySaF2fz%2FFAIAhhLF30vCqFiTw4mR',
                'CookieConsent': '{stamp:%27GgC/4YFFDB1GZTbhCbzWWWz12IS+B5eWgN/lVgiLkF6nzspJOlWOUg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1712290855103%2Cregion:%27de%27}',
                '_gcl_au': '1.1.1479579246.1712290856',
                '_mkto_trk': 'id:951-WXW-844&token:_mch-edmundoptics.com-1712290857451-50897',
                '_fbp': 'fb.1.1712290857474.1505308148',
                '_clck': 'rfjncj%7C2%7Cfko%7C0%7C1556',
                '_ga': 'GA1.2.1495210508.1712290856',
                '_gid': 'GA1.2.561455109.1712290858',
                'mf_user': 'ab3e4f6232ed2dbb54243f540901def4|',
                'wisepops': '%7B%22popups%22%3A%7B%7D%2C%22sub%22%3A0%2C%22ucrn%22%3A99%2C%22cid%22%3A%2250951%22%2C%22v%22%3A4%2C%22bandit%22%3A%7B%22recos%22%3A%7B%7D%7D%7D',
                'wisepops_visitor': '%7B%22EJXiYx9y4t%22%3A%229c6f532d-d6aa-46e6-bce4-51c1264b64b6%22%7D',
                'wisepops_props': '%7B%22cookie1%22%3A%22%22%7D',
                'wisepops_visits': '%5B%222024-04-05T04%3A20%3A56.125Z%22%5D',
                'wisepops_session': '%7B%22arrivalOnSite%22%3A%222024-04-05T04%3A20%3A56.125Z%22%2C%22mtime%22%3A1712290859222%2C%22pageviews%22%3A1%2C%22popups%22%3A%7B%7D%2C%22bars%22%3A%7B%7D%2C%22sticky%22%3A%7B%7D%2C%22countdowns%22%3A%7B%7D%2C%22src%22%3Anull%2C%22utm%22%3A%7B%7D%2C%22testIp%22%3Anull%7D',
                '_conv_v': 'vi%3A1*sc%3A1*cs%3A1712290856*fs%3A1712290856*pv%3A1*exp%3A%7B100339720.%7Bv.1003155091-g.%7B100317229.1%7D%7D-100340517.%7Bv.1003159301-g.%7B100317229.1%7D%7D%7D',
                'mf_0d213a1c-a791-4ba8-a4c8-444333d6e012': '3480e1debf9b5bcb9d2fe3d17b7ab494|04055722fda621ca5188c24e33e29d50a10bf2bc.595443985.1712290858151|1712291201653||1||||0|18.01|59.77153',
                '_clsk': 'vkz3so%7C1712293015667%7C1%7C1%7Ck.clarity.ms%2Fcollect',
                '_ga_K0MTNSK7JJ': 'GS1.1.1712293015.2.0.1712293015.60.0.0',
                'AWSALB': '2Gbi8u6YtfREcCkzdiUaJiTozHqo6Vrf+UfMAhR3oIFNOxKYs1M7QopRdiZxo/nvUGR4A8MugWmlXrO80+8L5lyHl7slO244uk3h/JmlbyjIIBylhDsSftz3qW4/',
                'AWSALBCORS': '2Gbi8u6YtfREcCkzdiUaJiTozHqo6Vrf+UfMAhR3oIFNOxKYs1M7QopRdiZxo/nvUGR4A8MugWmlXrO80+8L5lyHl7slO244uk3h/JmlbyjIIBylhDsSftz3qW4/',
                'EOLang': '1',
                'EOCurr': '1',
                'EO_EU_Inv': '',
                '__cf_bm': 'rPOjC68blhcCD4h_bnbB2kOAhaPnnU1mRtt9AefYbIk-1712293016-1.0.1.1-eMC9bwCtnTlLnpkQRpvlFHykQMilJswVFu3PSRaHbp9PND.eqjOkacjUDqG7FdDbFgRnRXMLY4qUvv1eXNykQA',
            }

            headers = {
                'accept': 'text/html, */*; q=0.01',
                'accept-language': 'en-US,en;q=0.9',
                # 'cookie': 'UMB_SESSION=CfDJ8KAWG3M62XpDvSL5Y%2BfhBSUlNEARpmuAsvC4zt8Zq1M26IkS7qx6sbfCGcEH5%2FcD%2BvA%2B%2FHxXgRfJWYV5URpLbRwRKX3BKPXVK7NR0J9qzptQQde5iSoS85y8TGJt7o%2Fi2CH6V%2FzhUAbsSy57ySaF2fz%2FFAIAhhLF30vCqFiTw4mR; CookieConsent={stamp:%27GgC/4YFFDB1GZTbhCbzWWWz12IS+B5eWgN/lVgiLkF6nzspJOlWOUg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1712290855103%2Cregion:%27de%27}; _gcl_au=1.1.1479579246.1712290856; _mkto_trk=id:951-WXW-844&token:_mch-edmundoptics.com-1712290857451-50897; _fbp=fb.1.1712290857474.1505308148; _clck=rfjncj%7C2%7Cfko%7C0%7C1556; _ga=GA1.2.1495210508.1712290856; _gid=GA1.2.561455109.1712290858; mf_user=ab3e4f6232ed2dbb54243f540901def4|; wisepops=%7B%22popups%22%3A%7B%7D%2C%22sub%22%3A0%2C%22ucrn%22%3A99%2C%22cid%22%3A%2250951%22%2C%22v%22%3A4%2C%22bandit%22%3A%7B%22recos%22%3A%7B%7D%7D%7D; wisepops_visitor=%7B%22EJXiYx9y4t%22%3A%229c6f532d-d6aa-46e6-bce4-51c1264b64b6%22%7D; wisepops_props=%7B%22cookie1%22%3A%22%22%7D; wisepops_visits=%5B%222024-04-05T04%3A20%3A56.125Z%22%5D; wisepops_session=%7B%22arrivalOnSite%22%3A%222024-04-05T04%3A20%3A56.125Z%22%2C%22mtime%22%3A1712290859222%2C%22pageviews%22%3A1%2C%22popups%22%3A%7B%7D%2C%22bars%22%3A%7B%7D%2C%22sticky%22%3A%7B%7D%2C%22countdowns%22%3A%7B%7D%2C%22src%22%3Anull%2C%22utm%22%3A%7B%7D%2C%22testIp%22%3Anull%7D; _conv_v=vi%3A1*sc%3A1*cs%3A1712290856*fs%3A1712290856*pv%3A1*exp%3A%7B100339720.%7Bv.1003155091-g.%7B100317229.1%7D%7D-100340517.%7Bv.1003159301-g.%7B100317229.1%7D%7D%7D; mf_0d213a1c-a791-4ba8-a4c8-444333d6e012=3480e1debf9b5bcb9d2fe3d17b7ab494|04055722fda621ca5188c24e33e29d50a10bf2bc.595443985.1712290858151|1712291201653||1||||0|18.01|59.77153; _clsk=vkz3so%7C1712293015667%7C1%7C1%7Ck.clarity.ms%2Fcollect; _ga_K0MTNSK7JJ=GS1.1.1712293015.2.0.1712293015.60.0.0; AWSALB=2Gbi8u6YtfREcCkzdiUaJiTozHqo6Vrf+UfMAhR3oIFNOxKYs1M7QopRdiZxo/nvUGR4A8MugWmlXrO80+8L5lyHl7slO244uk3h/JmlbyjIIBylhDsSftz3qW4/; AWSALBCORS=2Gbi8u6YtfREcCkzdiUaJiTozHqo6Vrf+UfMAhR3oIFNOxKYs1M7QopRdiZxo/nvUGR4A8MugWmlXrO80+8L5lyHl7slO244uk3h/JmlbyjIIBylhDsSftz3qW4/; EOLang=1; EOCurr=1; EO_EU_Inv=; __cf_bm=rPOjC68blhcCD4h_bnbB2kOAhaPnnU1mRtt9AefYbIk-1712293016-1.0.1.1-eMC9bwCtnTlLnpkQRpvlFHykQMilJswVFu3PSRaHbp9PND.eqjOkacjUDqG7FdDbFgRnRXMLY4qUvv1eXNykQA',
                'referer': 'https://www.edmundoptics.com/p/38348ink/39100/',
                'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }


            part_number_id = [m for m in pdp_url.split("/") if m]

            params = {
                'partNumberID': f'{part_number_id[-1]}',
                'stockNumber': f'{sku}'
                #     'displayIconFlag': 'false',
                #     '_': '1689345642410',
            }

            in_stock_validator = requests.get(
                'https://www.edmundoptics.com/modal-windows/inventorystatus-in-stock/',
                params=params,
                cookies=cookies,
                headers=headers,
                impersonate='chrome110'
            )

            response_lead_time = Selector(text=in_stock_validator.text)

            instock = False
            estimated_lead_time = list()
            for index, i in enumerate(response_lead_time.xpath('//div//p')):
                if not index:
                    instock_text = "".join(i.xpath(".//text()").getall())
                    if 'In Stock' in instock_text:
                        instock = True
                    continue
                if instock:
                    estimated_lead_time_html = "".join(i.xpath(".//text()").getall()[0])
                    estimted_text = " ".join(re.findall('within.*?days', estimated_lead_time_html))
                    estimted_text = re.sub(" - ", "-", estimted_text.replace('within', '').strip())
                    if estimted_text:
                        estimated_lead_time.append(
                            {"min_qty": 1, "time_to_ship": {"raw_value": f"{estimted_text}"}}
                        )

            if in_stock_validator.status_code == 200:
                in_stock = False if 'Contact Us' in in_stock_validator.text else True

        item['in_stock'] = in_stock

        item['lead_time'] = json.dumps(estimated_lead_time)

        if response.xpath("//div[@id='AddToCartBox']//input[@value='Add to Cart']"):
            item['available_to_checkout'] = True
        else:
            item['available_to_checkout'] = False

        
        checking = re.sub('\s+', ' ', response.xpath('//span[@class="snpn"]/following-sibling::span//text()').get('')).strip().lower()

        if estimated_lead_time:
            if 'in stock' in checking:
                item['lead_time'] = estimated_lead_time
            elif 'contact us' not in checking and 'in stock' not in checking:
                item['lead_time'] = estimated_lead_time
            else:
                item['lead_time'] = None
                item['in_stock'] = False
        else:
            item['lead_time'] = None
            item['in_stock'] = False

        checking_in_stock = response.xpath('//a[@class="clearance"]//text()').get('').lower()
        if 'clearance' in checking_in_stock:
            item['in_stock'] = True
        # EXTRACTING PRICES :-
        price_list = list()
        for tr in response.xpath('//div[contains(@class, "volPrice")]'):
            if tr.xpath('./strong/text()').getall() != []:
                if "-" not in tr.xpath('.//text()').getall()[0]:
                    min_qty = re.findall("\\d+\\+", tr.xpath('.//text()').getall()[0])[0].replace("+", "")
                else:
                    min_qty = re.findall("\\d+-", tr.xpath('.//text()').getall()[0])[0].replace("-", "")
                price = "".join(tr.xpath('./strong/text()').getall()).strip().replace("$", "")
                item_price = dict()
                if not price:
                    item_price['price_string'] = "Call for price"
                else:
                    item_price['price'] = float(price.replace(',', ''))
                    item_price['currency'] = "USD"
                item_price['min_qty'] = int(min_qty)
                price_list.append(item_price)

        item['price'] = price_list

        # return json output :-
        # The function should return a dictionary having statusCode: 200;
        # If all above given headers are scraped properly
        return {"statusCode": 200,
                "data": item}


if __name__ == '__main__':
    # parse function call with products_url and sku :-

    data = edmundoptics(pdp_url="https://www.edmundoptics.com/p/allied-vision-guppy-pro-f-031ccd-monochrome-camera/23178/", sku="68-563")
#     # print json :-
    print(data)
