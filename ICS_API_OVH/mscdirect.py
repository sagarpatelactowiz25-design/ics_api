from parsel import Selector
import json
import requests



def mscdirect(pdp_url, sku, vendor='mscdirect'):
    error = {}

    cookies = {
        'visid_incap_2587862': 'nNa/7LKGQQyjfoL7w37iTqR+LWgAAAAAQUIPAAAAAABFd/Y1ZhdVX9CEx9nXmXrN',
        'gig_bootstrap_4_R0HZVTou0ajlxJ_Xco0l_w': 'identity_ver4',
        '_evga_34c0': '{%22uuid%22:%2235ff5d24f9ad832c%22}',
        '_sfid_4952': '{%22anonymousId%22:%2235ff5d24f9ad832c%22%2C%22consents%22:[]}',
        'cjConsent': 'MHxZfDB8Tnww',
        '_blkp_xps': '%7B%22HJSHP%22%3A61%7D',
        '_ga': 'GA1.1.1884211103.1747811995',
        '_fbp': 'fb.1.1747811995512.639518355933353791',
        '_gcl_au': '1.1.1459020816.1747811996',
        'sa-user-id': 's%253A0-9b21c7ac-74db-5859-6a52-b94be2bf4951.MeFMhEKE2mGgTqQe1UD30cj%252FnjUYpaCbTCtEdIJpamA',
        'sa-user-id-v2': 's%253AmyHHrHTbWFlqUrlL4r9JUamW2gk.cHTrKqlxVjgnox8eUORHvWrdk4kyNbYG1T%252FxsAg2rrM',
        'sa-user-id-v3': 's%253AAQAKIMPWqcXH-_a7HgeCFLghDB3VZ0prg32tqp_-FwfAIM75EHwYBCCw_bXBBjABOgRURhDCQgTBkBr4.N1TVkH4aqb6u2Tyz%252BMOG5YtDz9v7g1Hw9OTcAz3LdVk',
        'visid_incap_2619917': 'C5ntu75sSRm3KcNvtqI4rG6LPmgAAAAAQUIPAAAAAADw3t+VwfQr7g7EBcyZqKp0',
        'incap_ses_33_2587862': 'V1IsaIx+C1MLD04Orj11AGHXa2gAAAAAIJY0KEYpBYb28J7M9o35fQ==',
        'Mscdirect': '3842513324.33588.0000',
        'mbox': 'session%23b91fa7a981724775afc2c2f5d28ad30d%231751899816%7CPC%23207733d3bc8a41de93df0362b1811750.41_0%231815142756',
        'da1181': '00000836',
        'gpod363': 'eyIyMTA3NTYzIjoxfQ%3D%3D',
        'dtCookie': 'v_4_srv_24_sn_FE845548B55ACC24463D51668BE9C937_perc_100000_ol_0_mul_1_app-3A4933650768ea878a_1',
        'nlbi_2587862': 'zzxxc/tS23cOLwaQG6JbxQAAAADp9hA1CsJEb5N2V/MpmHtk',
        'rxVisitor': '1751897955883GMS1G6FIGMBT9QCTM3TQC1KOL0RN6NI2',
        'dtSa': '-',
        'at_check': 'true',
        'AMCVS_99591C8B53306B560A490D4D%40AdobeOrg': '1',
        'AMCV_99591C8B53306B560A490D4D%40AdobeOrg': '179643557%7CMCIDTS%7C20277%7CMCMID%7C12516411731854364501552594196988412881%7CMCAAMLH-1752502756%7C12%7CMCAAMB-1752502756%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1751905156s%7CNONE%7CMCSYNCSOP%7C411-20237%7CvVersion%7C5.5.0',
        'mbox': 'session#b91fa7a981724775afc2c2f5d28ad30d#1751899817|PC#207733d3bc8a41de93df0362b1811750.41_0#1815142756',
        'WCDE_DA822': 'B',
        'cj_channel': 'Direct_Navigation',
        '__blka_ts': '1751899756703',
        's_vnum': '1754031600739%26vn%3D1',
        's_cc': 'true',
        '_uetsid': '5d87c9a05b3d11f0ad7319625db11ef7',
        '_uetvid': 'fecc4150361311f099e31f9d8cf8b6f8',
        '_ga_CM5B4R0KX7': 'GS2.1.s1751897956$o5$g0$t1751897956$j60$l0$h0',
        '__pr.10to': 'SADswMbwvu',
        '_rdt_uuid': '1747811994751.efc3bffa-4639-4032-a552-ff21bd4fab2e',
        'targetIO': 'B',
        'targetFS': 'C',
        '_br_uid_2': 'uid%3D8273018131472%3Av%3D12.0%3Ats%3D1747811995333%3Ahc%3D4',
        'dtPC': '24$497955882_908h-vUCCHOFBMFVJUADMUAKPAGLADNMUSKMOP-0e0',
        'WCDE_GUESTPROMO_VISIT': 'true',
        'utag_main': '_sn:3$_se:5%3Bexp-session$_ss:0%3Bexp-session$_st:1751899765272%3Bexp-session$ses_id:1751897956400%3Bexp-session$_pn:1%3Bexp-session$vapi_domain:mscdirect.com',
        's_sq': '%5B%5BB%5D%5D',
        'nlbi_2587862_2147483392': 'geIbac1t+VbhWrbCG6JbxQAAAABc1bFvZR2uppNXShL9/s+J',
        'reese84': '3:i4y4xStXSiZWhntIsq/irg==:cE4ianh9i/vpCAiflvopbtgl8NiRsV6VqhnA9vvYQgJeAdItxkbC5q5dUMgKX/wP3H0LM86rz5jZ/NNsI/pTjm/mTFm7nlHb6OMmta9khsKMbxn0pKClQdNcbLzYXBsXpoJjrGs2lmaObZNxqT1/HmummjO906Wt1PAFrAKH5xV7Y/f0Ow9OrUBmtMBmU5cQ2MVSdR438qTfVcWuWIocPd3ozfyb9w0StlkoD9U5IUNKzuSeTFOxB8/4Br5SKe7E/+ecHoL67zZVtLV6SfymOjqXWm3fNeRkTSXN3UH5TpQev188UjT7kiLGMexYstEraN7I2zea74ngQhekFGg5qyrHTs2nqfpQO+5T/JlZCl3z5MnZ886pEMutvAHNRo5VC5hAWl84M4sisPKiOfD2mVgscKewJ2y+1PdGfdPyAb16DBxa+jNG1OOjWJSFlqf0A3B96CTxeUmsT3bFQhe7crH5pUyoRnPRme+bfi14t/RtJbvYZNwCYxn9mB10LkaN:B6s2jt841JWboSwemRM4P8oGgImkuileoEJ5vZ0z7rY=',
        'fs_lua': '1.1751900563480',
        'fs_uid': '#10Q6K5#c619335b-d489-4b0e-b4d2-a40e246022d2:59049223-18b6-42d5-9ea1-2aafc317f1ec:1751900563480::1#/1779348027',
        'rxvt': '1751902379031|1751897955884',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://www.mscdirect.com/product/details/00000836',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        # 'cookie': 'visid_incap_2587862=nNa/7LKGQQyjfoL7w37iTqR+LWgAAAAAQUIPAAAAAABFd/Y1ZhdVX9CEx9nXmXrN; gig_bootstrap_4_R0HZVTou0ajlxJ_Xco0l_w=identity_ver4; _evga_34c0={%22uuid%22:%2235ff5d24f9ad832c%22}; _sfid_4952={%22anonymousId%22:%2235ff5d24f9ad832c%22%2C%22consents%22:[]}; cjConsent=MHxZfDB8Tnww; _blkp_xps=%7B%22HJSHP%22%3A61%7D; _ga=GA1.1.1884211103.1747811995; _fbp=fb.1.1747811995512.639518355933353791; _gcl_au=1.1.1459020816.1747811996; sa-user-id=s%253A0-9b21c7ac-74db-5859-6a52-b94be2bf4951.MeFMhEKE2mGgTqQe1UD30cj%252FnjUYpaCbTCtEdIJpamA; sa-user-id-v2=s%253AmyHHrHTbWFlqUrlL4r9JUamW2gk.cHTrKqlxVjgnox8eUORHvWrdk4kyNbYG1T%252FxsAg2rrM; sa-user-id-v3=s%253AAQAKIMPWqcXH-_a7HgeCFLghDB3VZ0prg32tqp_-FwfAIM75EHwYBCCw_bXBBjABOgRURhDCQgTBkBr4.N1TVkH4aqb6u2Tyz%252BMOG5YtDz9v7g1Hw9OTcAz3LdVk; visid_incap_2619917=C5ntu75sSRm3KcNvtqI4rG6LPmgAAAAAQUIPAAAAAADw3t+VwfQr7g7EBcyZqKp0; incap_ses_33_2587862=V1IsaIx+C1MLD04Orj11AGHXa2gAAAAAIJY0KEYpBYb28J7M9o35fQ==; Mscdirect=3842513324.33588.0000; mbox=session%23b91fa7a981724775afc2c2f5d28ad30d%231751899816%7CPC%23207733d3bc8a41de93df0362b1811750.41_0%231815142756; da1181=00000836; gpod363=eyIyMTA3NTYzIjoxfQ%3D%3D; dtCookie=v_4_srv_24_sn_FE845548B55ACC24463D51668BE9C937_perc_100000_ol_0_mul_1_app-3A4933650768ea878a_1; nlbi_2587862=zzxxc/tS23cOLwaQG6JbxQAAAADp9hA1CsJEb5N2V/MpmHtk; rxVisitor=1751897955883GMS1G6FIGMBT9QCTM3TQC1KOL0RN6NI2; dtSa=-; at_check=true; AMCVS_99591C8B53306B560A490D4D%40AdobeOrg=1; AMCV_99591C8B53306B560A490D4D%40AdobeOrg=179643557%7CMCIDTS%7C20277%7CMCMID%7C12516411731854364501552594196988412881%7CMCAAMLH-1752502756%7C12%7CMCAAMB-1752502756%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1751905156s%7CNONE%7CMCSYNCSOP%7C411-20237%7CvVersion%7C5.5.0; mbox=session#b91fa7a981724775afc2c2f5d28ad30d#1751899817|PC#207733d3bc8a41de93df0362b1811750.41_0#1815142756; WCDE_DA822=B; cj_channel=Direct_Navigation; __blka_ts=1751899756703; s_vnum=1754031600739%26vn%3D1; s_cc=true; _uetsid=5d87c9a05b3d11f0ad7319625db11ef7; _uetvid=fecc4150361311f099e31f9d8cf8b6f8; _ga_CM5B4R0KX7=GS2.1.s1751897956$o5$g0$t1751897956$j60$l0$h0; __pr.10to=SADswMbwvu; _rdt_uuid=1747811994751.efc3bffa-4639-4032-a552-ff21bd4fab2e; targetIO=B; targetFS=C; _br_uid_2=uid%3D8273018131472%3Av%3D12.0%3Ats%3D1747811995333%3Ahc%3D4; dtPC=24$497955882_908h-vUCCHOFBMFVJUADMUAKPAGLADNMUSKMOP-0e0; WCDE_GUESTPROMO_VISIT=true; utag_main=_sn:3$_se:5%3Bexp-session$_ss:0%3Bexp-session$_st:1751899765272%3Bexp-session$ses_id:1751897956400%3Bexp-session$_pn:1%3Bexp-session$vapi_domain:mscdirect.com; s_sq=%5B%5BB%5D%5D; nlbi_2587862_2147483392=geIbac1t+VbhWrbCG6JbxQAAAABc1bFvZR2uppNXShL9/s+J; reese84=3:i4y4xStXSiZWhntIsq/irg==:cE4ianh9i/vpCAiflvopbtgl8NiRsV6VqhnA9vvYQgJeAdItxkbC5q5dUMgKX/wP3H0LM86rz5jZ/NNsI/pTjm/mTFm7nlHb6OMmta9khsKMbxn0pKClQdNcbLzYXBsXpoJjrGs2lmaObZNxqT1/HmummjO906Wt1PAFrAKH5xV7Y/f0Ow9OrUBmtMBmU5cQ2MVSdR438qTfVcWuWIocPd3ozfyb9w0StlkoD9U5IUNKzuSeTFOxB8/4Br5SKe7E/+ecHoL67zZVtLV6SfymOjqXWm3fNeRkTSXN3UH5TpQev188UjT7kiLGMexYstEraN7I2zea74ngQhekFGg5qyrHTs2nqfpQO+5T/JlZCl3z5MnZ886pEMutvAHNRo5VC5hAWl84M4sisPKiOfD2mVgscKewJ2y+1PdGfdPyAb16DBxa+jNG1OOjWJSFlqf0A3B96CTxeUmsT3bFQhe7crH5pUyoRnPRme+bfi14t/RtJbvYZNwCYxn9mB10LkaN:B6s2jt841JWboSwemRM4P8oGgImkuileoEJ5vZ0z7rY=; fs_lua=1.1751900563480; fs_uid=#10Q6K5#c619335b-d489-4b0e-b4d2-a40e246022d2:59049223-18b6-42d5-9ea1-2aafc317f1ec:1751900563480::1#/1779348027; rxvt=1751902379031|1751897955884',
    }

    try:
        response = requests.get(pdp_url, cookies=cookies, headers=headers)  # proxies=proxy,verify=False,timeout=40)
    except:
        response = requests.get(pdp_url, cookies=cookies, headers=headers)  # proxies=proxy,verify=False,timeout=40)
    if response.status_code != 200:
        for k_ in range(0, 5):
            response = requests.get(pdp_url, cookies=cookies,
                                    headers=headers)  # proxies=proxy, verify=False,timeout=40)
            if response.status_code == 200:
                break

    if response.status_code==200:
        # response = Selector(text=response.text)

        try:
            result = {}
            try:
                url_parts =pdp_url.split("/")
                sku1 = url_parts[-1]
            except:
                sku1 = ''

            if sku1 == sku:
                html_content = response.text
                data1 = Selector(text=html_content)
                basic_json = data1.xpath('//script[@type="application/ld+json"]//text()').get()
                # print(basic_json)
                try:
                    json_ = json.loads(basic_json)
                except:
                    error['statusCode'] = 408
                    error['error_message'] = "Request timeout, failed to reach host"
                    return error
                vendor = vendor

                pdp_url = pdp_url

                price_list = []
                pricing_loaders = {}
                pricing_loaders['currency'] = "USD"
                if 'let priceObject =' in data1.xpath('.').get(''):
                    price_json = data1.xpath(
                        '//div[@id="lightbox-loader-content"]/script[contains(text(),"let priceObject")]/text()').get()
                    start_index = price_json.find('{')  # Find the starting index of the JSON string
                    end_index = price_json.rfind('}')
                    if start_index != -1 and end_index != -1:
                        try:
                            json_str = price_json[start_index:end_index + 1]
                            prices = json.loads(json_str)
                            min_qty = prices['minimumOrderQuantity']
                            price = prices['totalPriceText']
                            pricing_loaders['min_qty'] = min_qty
                            pricing_loaders['price'] = price

                        except:
                            min_qty = 1
                            pricing_loaders['min_qty'] = int(min_qty)
                            pricing_loaders['price_string'] = "Call For Price"

                    else:
                        pricing_loaders['min_qty'] = 1
                        pricing_loaders['price_string'] = "Call For Price"

                    price_list.append(pricing_loaders)

                    price = price_list

                    add_to_cart = data1.xpath('//div[@id="atc"]//button[@id="btn-pdp-add-to-cart"]').get()
                    if add_to_cart:
                        available = True
                    else:
                        available = False

                    available_to_checkout = available

                    stock = json_['offers']['availability']
                    if "Ships from Supplier" in stock:
                        instock = False
                    else:
                        instock = True

                    in_stock = instock

                    estimated_lead_time = []
                    try:
                        if 'Ships from Supplier' not in json_['offers']['availability']:
                            estimated_lead_time = [{
                                "min_qty": int(prices['minimumOrderQuantity']),
                                "time_to_arrive": {"raw_value": "Next Business Day*"}
                            }]

                        elif "Ships from Supplier" in json_['offers']['availability']:
                            estimated_lead_time = ('estimated_lead_time', [])
                        else:
                            estimated_lead_time = ('estimated_lead_time', [])
                    except:
                        pass

                    if estimated_lead_time:
                        lead_time = estimated_lead_time

                    result['vendor'] = vendor
                    result['sku'] = sku
                    result['pdp_url'] = pdp_url
                    result['price'] = price_list
                    result['available_to_checkout'] = available_to_checkout
                    result['in_stock'] = instock
                    result['lead_time'] = estimated_lead_time
                    return {'statusCode': 200, 'data': result}

                # return data



        except Exception as e:
            error['statusCode'] = 500
            error['error_message'] = "Internal server error" + str(e)
            return error
    elif response.status_code==404:
        error['statusCode'] = 410
        error['error_message'] = "Product Not Found"

        return error
    else:
            error['statusCode'] = 408

            error['error_message'] = "Request timeout, failed to reach host"
            return error


# if __name__ == '__main__':
# #     # keyword = 'https://www.mscdirect.com/product/details/06941017'
# #     # keyword = 'https://www.mscdirect.com/product/details/50075548'
# #     # a = process(keyword)
# #     # print(json.dumps(a))
# #
# #
#     event = {"pdp_url": "https://www.mscdirect.com/product/details/96341706",
#              "sku": "96341706",
#              "vendor": "mscdirect"}
#     print(json.dumps(mscdirect(pdp_url=event['pdp_url'], sku=event['sku'])))
