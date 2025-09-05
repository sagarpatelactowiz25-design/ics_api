import requests
import urllib3
import json
from parsel import Selector
from urllib.parse import urlencode

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token = "f42a5b59aec3467e97a8794c611c436b91589634343"

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': 'visid_incap_2587862=KJSQuLESTVeVvAkKNbE0vIjaJmgAAAAAQUIPAAAAAAATgvPOkJMCAR1DeyYqdriQ; incap_ses_219_2587862=Zxs/AmU3kQ9x0CZ2qAsKA4jaJmgAAAAAcDzQnhrJTUBRBKaomqSGYg==; incap_ses_710_2587862=vCs3XbE4MV04TCp+jm3aCYnaJmgAAAAA1qI4cf+ykAYIbO98aVPocQ==; reese84=3:crSO5J/oB574NmL5ObSrOw==:9vkJnWonkWKQ42ClCcdJoMSLVdjxtUXSEBXkZNosM497dfBY5R0t9KzecK2Tbi+2bJl0NecfPVmJ3+Nws8iUSw4ZCKhO1k536WF9zK7oQBXE1ItJxpaU8kLCrFhb690t+uGqvG7AOHIrsVWYxBPM9JPdOmVfz6E4aYscWmHJlEyduLP7VqHW9ytWcH+0xe7hq48I0bjPFBvgEjzhqODE0Pq5tL9eCFxHGnpa84XnSXJKJLz0dZaXC6NAEbrq4qiUCu9K6Z5tTFtaowQIJaTedDbqpLm/kyvSgsuFevPh+q9hoM7XsLD7Cp2JCvEIOCnKYLKRY5xrGGVeQ/XgwvYpO7Ymr81aqvjeIf8NtLco6M8Dkps8sPOSWfOrUWT5qXgFharZeXtFsIz13NFVleMlbnObARDd35AHE+g7vTeQxPcA3yXsvBcv2jBWxxd6z/nVyIttyw6ztuXal1FbRlLBKGQoaLDi3bOM96KvFJLGahk=:bUmbHqHhE/bNtViZT8BBKxkWahJOxgiQ2l0zqNECKPE=; dtCookie=v_4_srv_25_sn_32C1DBDAE2AE0E826753336C215CCC7F_perc_100000_ol_0_mul_1_app-3A4933650768ea878a_1_rcs-3Acss_0; Mscdirect=3876067756.33588.0000; nlbi_2587862=UhRvWgXKLHNLSPyzG6JbxQAAAAAMlPyIpv86S3Nax527A05z; mbox=session%23ec0b1705cde8433f92f5302c22f1ee86%231747379137%7CPC%23ec0b1705cde8433f92f5302c22f1ee86.41_0%231810622077; mboxEdgeCluster=41; da1181=78562212; gpod363=eyIyMTA2MDY3IjoxfQ%3D%3D; incap_ses_242_2587862=PH7vKAcAuyacv5ecBMJbA3vcJmgAAAAAUyAA1p4W/bXenOmpCCg/Hw==; rxVisitor=1747377277468RMNQQIHSNPVNUN2I9LIM4LVV81L2Q42M; dtSa=-; at_check=true; AMCVS_99591C8B53306B560A490D4D%40AdobeOrg=1; AMCV_99591C8B53306B560A490D4D%40AdobeOrg=179643557%7CMCIDTS%7C20225%7CMCMID%7C86259093158298650052017161675435287218%7CMCAAMLH-1747982079%7C7%7CMCAAMB-1747982079%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1747384479s%7CNONE%7CvVersion%7C5.5.0; nlbi_2587862_2147483392=YuNpAJ1qNTsmAkEYG6JbxQAAAABGSbD/OB2JdMGs409a8RQa; utag_main=_sn:1$_se:4%3Bexp-session$_ss:0%3Bexp-session$_st:1747379080477%3Bexp-session$ses_id:1747377279937%3Bexp-session$_pn:1%3Bexp-session$vapi_domain:mscdirect.com; cross_sell_id=78562212; cj_channel=Direct_Navigation; c4=guest; c15=msc%3Aproducts%3Aaircraft%20extension%20drill%20bits%3A78562212; s_vnum=1748716200627%26vn%3D1; s_invisit=true; s_cc=true; mboxEdgeCluster=41; mbox=session#ec0b1705cde8433f92f5302c22f1ee86#1747379141|PC#ec0b1705cde8433f92f5302c22f1ee86.41_0#1810622077; WCDE_DA822=B; _rdt_uuid=1747377281450.43ba2d52-e0fb-4b3f-a722-f8e24111208f; _br_uid_2=uid%3D7193821705063%3Av%3D12.0%3Ats%3D1747377281463%3Ahc%3D1; cjConsent=MHxOfDB8Tnww; cjUser=dcd27f97-daf4-44e9-9d1e-118e891b2da9; _evga_34c0={%22uuid%22:%22bf49a3206ea77bd7%22}; _sfid_4952={%22anonymousId%22:%22bf49a3206ea77bd7%22%2C%22consents%22:[]}; _blkp_xps=%7B%22HJSHP%22%3A29%7D; gig_bootstrap_4_R0HZVTou0ajlxJ_Xco0l_w=identity_ver4; _uetsid=d95afbf0321f11f09e87bf171e927618; _uetvid=d95b48c0321f11f0a3a2edc691d7a48e; __blka_ts=1747379081948; _ga=GA1.1.1726591112.1747377282; _ga_CM5B4R0KX7=GS2.1.s1747377282$o1$g1$t1747377282$j60$l0$h0; sa-user-id=s%253A0-63c3c175-87bd-57fc-42f0-a85b3433e20a.6ia9nrU1m%252BdpkAsbxVicdpocE5xiWkZ%252FRhHh0uocj30; sa-user-id-v2=s%253AY8PBdYe9V_xC8KhbNDPiCqL5rBY.uQZUOtAZqCGZmJtC0lwVRWM0x%252FyEx6rILXo%252BT%252Fq4dlQ; sa-user-id-v3=s%253AAQAKIEgTMbGfSrjUUw8jJYQPyWC_vY8sIlT_1HsZep5IBOTaEAEYAyCk3NHABjABOgRURhDCQgTNt9s6.NUo%252F2OrJPCSxMx9pLCSwWI1DUojohj3UsSekeEcZ7H4; _fbp=fb.1.1747377282704.677500777217555624; _gcl_au=1.1.144428886.1747377283; fs_lua=1.1747377282332; fs_uid=#10Q6K5#a402cebf-8dc2-4346-9a06-6486aaf33f84:4459fef7-dff1-41e6-947b-190d4703dfea:1747377282332::1#/1778913283; rxvt=1747379085279|1747377277470; dtPC=25$177277466_941h-vECQVHCOVRHKMGQWPAHPKMUHUJEKKKNUF-0e0',
}


def make_request(url, token, max_retries=5, timeout=30):
    # proxy_url = "https://api.scrape.do/?"
    # params = {
    #     'token': token,
    #     'super': 'true',
    #     'url': url
    # }
    # final_url = proxy_url + urlencode(params)
    final_url=f'https://api.scrape.do/?token={token}&url={url}&super=true'

    for attempt in range(max_retries):
        try:
            response = requests.get(final_url, timeout=timeout, headers=headers)
            if response.status_code == 200:
                return response
        except (requests.RequestException, requests.Timeout):
            continue
    return None


def extract_product_data(response, sku, url, vendor):
    try:
        selector = Selector(text=response.text)
        raw_data = selector.xpath('//script[contains(text(),\'"@type": "Product"\')]/text()').get()

        if not raw_data:
            return {'statusCode': 404, 'error_message': 'Product Not Found'}

        json_data = json.loads(raw_data)
        scraped_sku = json_data.get('sku')

        if scraped_sku != sku:
            return {
                'statusCode': 404,
                'error_message': f"Scraped sku:{scraped_sku} does not match input sku:{sku}"
            }

        return build_product_response(json_data, selector, url, vendor)
    except Exception as e:
        return {'statusCode': 500, 'error_message': f"Data extraction error: {str(e)}"}


def build_product_response(json_data, selector, url, vendor):
    offers = json_data.get('offers', {})
    instock = offers.get('availability', '').lower() == 'in stock'

    price_data = get_price_data(selector, offers)

    data = {
        'vendor': vendor,
        'sku': json_data.get('sku'),
        'pdp_url': url,
        'price': [price_data],
        'available_to_checkout': instock,
        'in_stock': instock,
        'lead_time': None
    }

    return {'statusCode': 200, 'data': data}


def get_price_data(selector, offers):
    quantity = selector.xpath('//input[@id="pdp-input-quantity"]/@value').get()
    return {
        'min_qty': int(quantity.strip()) if quantity else 1,
        'price': float(offers.get('price').replace(',','')) if offers.get('price') else None,
        'currency': 'USD'
    }


def mscdirect(url, sku, vendor='mscdirect'):
    try:
        response = make_request(url, token)

        if not response:
            return {
                'statusCode': 408,
                'error_message': "Request timeout, failed to reach host"
            }
        return extract_product_data(response, sku, url, vendor)

    except Exception as e:
        return {
            'statusCode': 500,
            'error_message': f"Internal server error: {str(e)}"
        }


# if __name__ == '__main__':
#     event={"pdp_url": "https://www.mscdirect.com/product/details/67635474", "sku": "67635474", "vendor": "mscdirect"}
#     print(json.dumps(mscdirect(event['pdp_url'],event['sku'])))

