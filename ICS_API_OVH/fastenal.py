import re
import json
import requests
from parsel import Selector

# 5 times retry for response if not get response in one time:-
max_retires = 5
# Scraper proxies for request :-
# proxies = {
#     "http": "http://scraperapi.country_code=de.keep_headers=true:de51e4aafe704395654a32ba0a14494d@proxy-server.scraperapi.com:8001"
# }
proxies = {
    "http": "http://4d6a0e0cab5d4b79811b69533059e6b1eccb3b7b628:@proxy.scrape.do:8080?country=US"
}


def fastenal(pdp_url, sku='sku', vendor='fastenal'):
    url = pdp_url
    try:
        skus = url.split('/')[-1]
        if skus != sku:
            return {"statusCode": 410,
                    "error_message": f"Scraped SKU:{skus} does not match input SKU:{sku}"}
        # cookies :-
        # cookies = {
        #     'mt.v': '2.46321644.1711102788875',
        #     '__mauuid': 'c0e5c2b5-8ac8-458f-a881-19945fce256a',
        #     'COOKIE_AGREEMENT': '"1"',
        #     '_hjSessionUser_302225': 'eyJpZCI6IjIyMmQ2N2M5LTQ5MzQtNWMwMy05YTQ5LTRlMDk2YmExZjEzNSIsImNyZWF0ZWQiOjE3MTExMDI3ODk2MTYsImV4aXN0aW5nIjp0cnVlfQ==',
        #     '_ga_X40YWNGS17': 'deleted',
        #     'NEW_SEARCH_EXPERIENCE': '0.14424062',
        #     '_ga_X40YWNGS17': 'deleted',
        #     'calltrk_referrer': 'direct',
        #     'calltrk_landing': 'https%3A//www.fastenal.com/product/details/03130676',
        #     'calltrk_session_id': 'e500d794-0010-48ca-917b-0e5a0da89a65',
        #     '_clck': 'jgq613%7C2%7Cfod%7C0%7C1689',
        #     'calltrk_fcid': '5735616c-9e63-49c8-9d5c-f4090a3de033',
        #     'brandcdn_uid': '47888a39-04e5-42b2-b619-3d15d3b4d418',
        #     'XSRF-TOKEN': '0381c5a6-7209-43eb-9406-2706154e82d8',
        #     'CJSESSIONID': 'YzY4ZDU4OGEtY2U3Zi00Nzk2LTk0MjQtOTJiNDk0NGE3YjY0',
        #     '_gid': 'GA1.2.1901591289.1728028019',
        #     '_hjSession_302225': 'eyJpZCI6ImU0MTI4YWI0LTUyZjAtNDY4Ni05ODM4LTcyMjE0Y2UxMTA0MyIsImMiOjE3MjgwMjgwMTg5OTgsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        #     'sa-user-id': 's%253A0-653066c7-02f8-511f-5388-fcc99ce90b06.BOq%252FbU%252BT%252Bv%252BEp4RtB%252F8xQnAixu2%252B7d3L8fMhuj5LdQI',
        #     'sa-user-id-v2': 's%253AZTBmxwL4UR9TiPzJnOkLBhttCmo.UeFz3WcWiGnRnIgNeAfH17mahtcszFcOGa2hpV7O0%252Fg',
        #     'sa-user-id-v3': 's%253AAQAKICGqCv4l4CSn837D3TfsvqBFhOrFMEWAp4azEkj_CcHSEAEYAyDP7OSvBjABOgRCSa5nQgT6cz1b.QBpIqKm4t77hD7fZmawqylXTCI0GJTK16T8H43cHZ1s',
        #     '_ga': 'GA1.2.1373299422.1711102789',
        #     '_dc_gtm_UA-2555468-6': '1',
        #     '_ga_X40YWNGS17': 'GS1.1.1728028019.43.1.1728028529.0.0.0',
        # }
        # headers = {
        #     'accept': 'application/json, text/plain, */*',
        #     'accept-language': 'en-US,en;q=0.9',
        #     'content-type': 'application/json',
        #     # 'cookie': 'mt.v=2.46321644.1711102788875; __mauuid=c0e5c2b5-8ac8-458f-a881-19945fce256a; COOKIE_AGREEMENT="1"; _hjSessionUser_302225=eyJpZCI6IjIyMmQ2N2M5LTQ5MzQtNWMwMy05YTQ5LTRlMDk2YmExZjEzNSIsImNyZWF0ZWQiOjE3MTExMDI3ODk2MTYsImV4aXN0aW5nIjp0cnVlfQ==; _ga_X40YWNGS17=deleted; NEW_SEARCH_EXPERIENCE=0.14424062; _ga_X40YWNGS17=deleted; calltrk_referrer=direct; calltrk_landing=https%3A//www.fastenal.com/product/details/03130676; calltrk_session_id=e500d794-0010-48ca-917b-0e5a0da89a65; _clck=jgq613%7C2%7Cfod%7C0%7C1689; calltrk_fcid=5735616c-9e63-49c8-9d5c-f4090a3de033; brandcdn_uid=47888a39-04e5-42b2-b619-3d15d3b4d418; XSRF-TOKEN=0381c5a6-7209-43eb-9406-2706154e82d8; CJSESSIONID=YzY4ZDU4OGEtY2U3Zi00Nzk2LTk0MjQtOTJiNDk0NGE3YjY0; _gid=GA1.2.1901591289.1728028019; _hjSession_302225=eyJpZCI6ImU0MTI4YWI0LTUyZjAtNDY4Ni05ODM4LTcyMjE0Y2UxMTA0MyIsImMiOjE3MjgwMjgwMTg5OTgsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; sa-user-id=s%253A0-653066c7-02f8-511f-5388-fcc99ce90b06.BOq%252FbU%252BT%252Bv%252BEp4RtB%252F8xQnAixu2%252B7d3L8fMhuj5LdQI; sa-user-id-v2=s%253AZTBmxwL4UR9TiPzJnOkLBhttCmo.UeFz3WcWiGnRnIgNeAfH17mahtcszFcOGa2hpV7O0%252Fg; sa-user-id-v3=s%253AAQAKICGqCv4l4CSn837D3TfsvqBFhOrFMEWAp4azEkj_CcHSEAEYAyDP7OSvBjABOgRCSa5nQgT6cz1b.QBpIqKm4t77hD7fZmawqylXTCI0GJTK16T8H43cHZ1s; _ga=GA1.2.1373299422.1711102789; _dc_gtm_UA-2555468-6=1; _ga_X40YWNGS17=GS1.1.1728028019.43.1.1728028529.0.0.0',
        #     'origin': 'https://www.fastenal.com',
        #     'pragma': 'no-cache',
        #     'priority': 'u=1, i',
        #     'referer': 'https://www.fastenal.com/product/details/0814625',
        #     'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'sec-fetch-dest': 'empty',
        #     'sec-fetch-mode': 'cors',
        #     'sec-fetch-site': 'same-origin',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        #     'x-xsrf-token': '0381c5a6-7209-43eb-9406-2706154e82d8',
        # }
        # json data :-
        cookies = {
            'XSRF-TOKEN': '80752d77-4423-41eb-a939-376a4334aa76',
            'CJSESSIONID': 'ZTdjZDRmMGYtZDlhNy00MDk1LTlkMjgtNjEwOGUxMmYwNDlk',
            'TSESSIONID': 'A9B87FE06BB3F79241820E1EF9DB508E',
            'mt.v': '2.2125303036.1751833920802',
            '_clck': '105qwcw%7C2%7Cfxd%7C0%7C2013',
            '_gid': 'GA1.2.206526560.1751833921',
            '_dc_gtm_UA-2555468-6': '1',
            '_hjSessionUser_302225': 'eyJpZCI6IjAxZWMzYmVjLTNlNzMtNTZiNS05N2IzLWMwNDFiMjNmODllOSIsImNyZWF0ZWQiOjE3NTE4MzM5MjEzODYsImV4aXN0aW5nIjpmYWxzZX0=',
            '_hjSession_302225': 'eyJpZCI6ImMyZDViZTRlLTMwZjctNGZkMi04ZGUyLWJiNjFjMzkyMzU2OSIsImMiOjE3NTE4MzM5MjEzODYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
            '_uetsid': '456836d05aa811f0bfcaa11199e057dd',
            '_uetvid': '456818105aa811f0980545a42ee624b1',
            '_ga': 'GA1.1.175102891.1751833921',
            'sa-user-id': 's%253A0-9b21c7ac-74db-5859-6a52-b94be2bf4951.MeFMhEKE2mGgTqQe1UD30cj%252FnjUYpaCbTCtEdIJpamA',
            'sa-user-id-v2': 's%253AmyHHrHTbWFlqUrlL4r9JUZRxAWg.gr0aWTeVnSuubNF1oZImWvxWWRilymVhegzsbe%252B8WWI',
            'sa-user-id-v3': 's%253AAQAKIMPWqcXH-_a7HgeCFLghDB3VZ0prg32tqp_-FwfAIM75EHwYBCCw_bXBBjABOgRURhDCQgTBkBr4.N1TVkH4aqb6u2Tyz%252BMOG5YtDz9v7g1Hw9OTcAz3LdVk',
            '__mauuid': '2f1e6905-f7dc-4e07-9d49-19945f430bf2',
            '_clsk': 'w2aos3%7C1751833922088%7C1%7C0%7Cj.clarity.ms%2Fcollect',
            'COOKIE_AGREEMENT': '"1"',
            '_ga_X40YWNGS17': 'GS2.1.s1751833921$o1$g1$t1751833949$j32$l0$h0',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.fastenal.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.fastenal.com/product/details/2180230',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'x-xsrf-token': '80752d77-4423-41eb-a939-376a4334aa76',
            # 'cookie': 'XSRF-TOKEN=80752d77-4423-41eb-a939-376a4334aa76; CJSESSIONID=ZTdjZDRmMGYtZDlhNy00MDk1LTlkMjgtNjEwOGUxMmYwNDlk; TSESSIONID=A9B87FE06BB3F79241820E1EF9DB508E; mt.v=2.2125303036.1751833920802; _clck=105qwcw%7C2%7Cfxd%7C0%7C2013; _gid=GA1.2.206526560.1751833921; _dc_gtm_UA-2555468-6=1; _hjSessionUser_302225=eyJpZCI6IjAxZWMzYmVjLTNlNzMtNTZiNS05N2IzLWMwNDFiMjNmODllOSIsImNyZWF0ZWQiOjE3NTE4MzM5MjEzODYsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_302225=eyJpZCI6ImMyZDViZTRlLTMwZjctNGZkMi04ZGUyLWJiNjFjMzkyMzU2OSIsImMiOjE3NTE4MzM5MjEzODYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _uetsid=456836d05aa811f0bfcaa11199e057dd; _uetvid=456818105aa811f0980545a42ee624b1; _ga=GA1.1.175102891.1751833921; sa-user-id=s%253A0-9b21c7ac-74db-5859-6a52-b94be2bf4951.MeFMhEKE2mGgTqQe1UD30cj%252FnjUYpaCbTCtEdIJpamA; sa-user-id-v2=s%253AmyHHrHTbWFlqUrlL4r9JUZRxAWg.gr0aWTeVnSuubNF1oZImWvxWWRilymVhegzsbe%252B8WWI; sa-user-id-v3=s%253AAQAKIMPWqcXH-_a7HgeCFLghDB3VZ0prg32tqp_-FwfAIM75EHwYBCCw_bXBBjABOgRURhDCQgTBkBr4.N1TVkH4aqb6u2Tyz%252BMOG5YtDz9v7g1Hw9OTcAz3LdVk; __mauuid=2f1e6905-f7dc-4e07-9d49-19945f430bf2; _clsk=w2aos3%7C1751833922088%7C1%7C0%7Cj.clarity.ms%2Fcollect; COOKIE_AGREEMENT="1"; _ga_X40YWNGS17=GS2.1.s1751833921$o1$g1$t1751833949$j32$l0$h0',
        }

        json_data = {
            'sku': [
                f'{sku}',
            ],
            'productDetails': True,
            'attributeFilters': {},
            'pageUrl': f'/product/details/{sku}',
        }

        # request to url using proxies :-
        url_request = str()
        try:
            for i in range(max_retires):
                try:
                    url_request = requests.post('https://www.fastenal.com/catalog/api/product-search',
                                                cookies=cookies,
                                                headers=headers,
                                                json=json_data,
                                                proxies=proxies
                                                )
                except Exception as e:
                    # The function should return a dictionary having statusCode: 500;
                    # If any internal error occurs. i.e If any Exception is caught inside try-except.
                    return {"statusCode": 500,
                            "error_message": "Internal server error" + str(e)}

                if url_request.status_code == 200:
                    break
            else:
                # The function must have logic for retries Max. 5
                # If request fails after 5 retries it should return following
                return {'statusCode': 408,
                        'error_message': 'Request timeout, failed to reach host'}
        except Exception as e:
            # The function should return a dictionary having statusCode: 500;
            # If any internal error occurs. i.e If any Exception is caught inside try-except.
            return {"statusCode": 500,
                    "error_message": "Internal server error" + str(e)}

        # main json loaded :-
        json_data = json.loads(url_request.text)

        # For Discontinued product :-
        try:
            if json_data['productDetail']['compliances'][0]['mp_Alt Text'].lower() == "Discontinued".lower():
                # The function should return a dictionary having statusCode: 410;
                # If product is discontinued
                return {"statusCode": 410,
                        "error_message": "Product is discontinued"}
        except Exception as e:
            print(e)

        # Product_details :-
        get_product_details = json_data.get('productDetail')

        # define dictionary for making data dictionary :-
        item = dict()

        # vendor Extracting :-
        item['vendor'] = vendor

        # sku :-
        try:
            item['sku'] = get_product_details.get('sku')
        except Exception as e:
            return {"statusCode": 410,
                    "error_message": "Product not found"}

        # pdp_url :-
        item['pdp_url'] = url

        # price Extracting :-
        # Price Extracting :-
        item_price = dict()
        item_price['currency'] = 'USD'
        item_price['min_qty'] = 1

        price_list = list()
        get_pricedisplaydata = get_product_details.get('pdd')
        if get_pricedisplaydata:
            o_price = ""
            w_price = ""
            for labeldata in get_pricedisplaydata:
                if labeldata['mp_label'] == 'Online Price:':
                    o_price = labeldata['pr']
                    price_list.append(labeldata['mp_label'])
                elif labeldata['mp_label'] == 'Wholesale:':
                    w_price = labeldata['pr']
                    price_list.append(labeldata['mp_label'])

            if "Online Price:" in price_list:
                item_price['price'] = float(o_price.replace(',', ''))

            if "Online Price:" not in price_list:
                item_price['price'] = float(w_price.replace(',', ''))
        else:
            item_price['price_string'] = "Call for Price"
            item_price.pop('currency')

        if 'price' in item_price:
            item_price['currency'] = 'USD'

        item['price'] = [item_price]

        # in_stock :-
        get_product_data = get_product_details.get('productEda')
        in_stock = get_product_data.get('mp_availabilityMessage')
        if in_stock.lower() == 'available inventory':
            in_stock = True
        else:
            in_stock = False

        item['in_stock'] = in_stock

        # available_to_checkout :-
        available_to_checkout = False
        pdpDeliveryMethodList = get_product_data.get('pdpDeliveryMethodList')
        if pdpDeliveryMethodList:
            for method in pdpDeliveryMethodList:
                mp_day = method.get('mp_day')
                if mp_day:
                    available_to_checkout = True
                else:
                    available_to_checkout = in_stock
        else:
            available_to_checkout = in_stock

        item['available_to_checkout'] = available_to_checkout

        estimated_lead_time = get_product_data.get('mp_message')
        # estimated_lead_time = ' '.join(estimated_lead_time)
        if 'day' not in estimated_lead_time:
            lead_time = get_product_data.get('mp_availabilityMessage')
            if 'ship' in lead_time:
                estimated_lead_time = lead_time
            else:
                estimated_lead_time = None
        estimate_list = []
        if estimated_lead_time:
            estimate_list.append({
                'min_qty': 1,
                'time_to_ship': {
                    'raw_value': estimated_lead_time
                }

            })
        if estimate_list:
            estimated_lead_time = estimate_list
        else:
            estimated_lead_time = None

        item['lead_time'] = estimated_lead_time

        # if no any key get
        key = ['lead_time', 'vendor', 'sku', 'pdp_url', 'price', 'available_to_checkout', 'in_stock']
        for i in key:
            if i not in item.keys():
                return None

        # return json output :-
        # The function should return a dictionary having statusCode: 200;
        # If all above given headers are scraped properly
        return {"statusCode": 200,
                "data": item}

    except Exception as e:
        # The function should return a dictionary having statusCode: 500;
        # If any internal error occurs. i.e If any Exception is caught inside try-except.
        return {"statusCode": 500,
                "error_message": "Internal server error" + str(e)}

# if __name__ == '__main__':
#     event ={"sku": "218027", "vendor": "fastenal", "pdp_url": "https://www.fastenal.com/product/details/2180272"}
#     print(json.dumps(fastenal(pdp_url=event['pdp_url'], sku=event['sku'])))