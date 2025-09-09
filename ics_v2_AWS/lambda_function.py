import json
import datetime
import hashlib
import re
import api_funcs_list
import requests
import pymysql
import db_config


def get_current_datetime():
    return datetime.datetime.now(datetime.timezone.utc)


def lambda_handler(event, context):
    current_datetime = get_current_datetime()
    request_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    start_time = current_datetime.timestamp()
    api_key = event.get('headers', {}).get('x-api-key',None)
    db_con=db_config.ConfigMongo()

    client_ip = event.get('headers', {}).get('x-forwarded-for', 'internal')
    request_id = hashlib.sha256((api_key + str(start_time)).encode()).hexdigest()

    client = pymysql.connect(host='', database='ics_api_dashboard', user='', password='')
    cursor = client.cursor()

    body_data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    vendor_ = body_data.get('vendor', None)
    vendor_ = vendor_ if vendor_ and (vendor_ in api_funcs_list.aws_api_funcs.keys() or vendor_ in api_funcs_list.local_api_funcs.keys()) else None
    item = {'ip': client_ip, 'params': body_data, 'request_time': request_time, 'response_time':None,
            'request_id': request_id, 'status_code': 201,'key': api_key, 'vendor_name':vendor_, 'execution_time':30,
            'success':False, 'message':'Time Out', 'data':None,
            'response':{'query_params':body_data,'execution_time':None,'success':False,'message':'Time Out','data':None}}
    db_con.insert_storage_log(item)

    utctime = datetime.datetime.now(datetime.timezone.utc).timestamp()

    def update_table(status_code=201, error_message=None, body=None):
        # Dynamically create sql query based on existing variables
        temp_datetime = get_current_datetime()
        response_time = temp_datetime.strftime('%Y-%m-%d %H:%M:%S')

        resp_time = round(temp_datetime.timestamp() - start_time, 2)
        return_status_code = status_code
        success= True if status_code==200 else False
        error_message__ = 'Request Success' if status_code==200 else error_message
        update_dict={'response_time':response_time,'status_code':status_code, 'vendor_name':vendor_,'execution_time':resp_time,
                     'success':success,'message':error_message__,'data':body,
                     'response':{'query_params':body_data,'execution_time':resp_time,'success':success,'message':error_message__,'data':body}}
        if error_message:
            if status_code == 502 or status_code == 503 or status_code==500:
                return_status_code = 500
                error_message = 'Internal server error'
            return_dict = {'error_message': error_message}
        elif body and status_code == 200:
            db_con.add_apiKey_usage(api_key)
            return_dict = body
        else:
            return_dict = {'error_message': 'no conditions matched'}
        db_con.update_storage_log(update_dict,request_id)
        return {'statusCode': return_status_code, 'body': json.dumps({'statusCode': return_status_code, 'body': return_dict})}
    if not db_con.check_usage(event.get('headers', {}).get('x-api-key')):
        return update_table(status_code=401,error_message='API key usage limit exceeded')
    try:
        if not db_con.authenticate_apiKey(event.get('headers', {}).get('x-api-key')):
            pass
            # return update_table(status_code=401,error_message='Unauthorized, key is inactive')

        if event.get('headers', {}).get('x-api-key') not in ["act-gov-879365-789534", "87p6t2X5S33SsqQXbYIx64ENGGpdtj1g8ZwppQWK"]:
            return update_table(status_code=401,error_message='Unauthorized, x-api-key is invalid')

        error = ''
        dev_error = {}
        url = None
        # TODO: Optimise this part for input parameter validation
        try:
            if isinstance(body_data['pdp_url'], str) and body_data['pdp_url']:
                url = body_data['pdp_url']
            else:
                error = f"Type error in request param pdp_url, expected str"
        except:
            error = f"required parameter missing pdp_url"

        sku = None
        try:
            if isinstance(body_data['sku'], str) and body_data['sku']:
                if re.match('^(?=.*\S).+$', body_data['sku']):
                    sku = body_data['sku']
                else:
                    error = "Invalid SKU"
            else:
                error = f"Type error in request param sku, expected str"
        except Exception as e:
            error = f"required parameter missing sku"

        vendor = None
        try:
            if isinstance(body_data['vendor'], str) and body_data['vendor']:
                if re.match("^[a-zA-Z0-9-]*$", body_data['vendor']):
                    vendor = body_data['vendor']
                else:
                    error = "Invalid vendor"
            else:
                error = f"Type error in request param vendor, expected str"
        except:
            error = f"required parameter missing vendor"
        min_qty = zipcode = None
        if vendor == 'globalindustrial' or vendor == 'fixsupply':
            try:
                if isinstance(body_data['zipcode'], str) and body_data['zipcode']:
                    if re.match("^[a-zA-Z0-9-]*$", body_data['zipcode']):
                        zipcode = body_data['zipcode']
                    else:
                        error = "Invalid zipcode"
                else:
                    error = f"Type error in request param zipcode, expected str"
            except:
                pass
            try:
                if isinstance(body_data['min_qty'], int) and body_data['min_qty']:
                    min_qty = body_data['min_qty']
                else:
                    error = f"Type error in request param min_qty, expected Integer"
            except:
                pass

        if error:
            return update_table(status_code=400, error_message=error)

        else:
            if vendor in api_funcs_list.aws_api_funcs.keys():
                module_name = api_funcs_list.aws_api_funcs[vendor]
                module = __import__(module_name)
                if vendor == 'globalindustrial' or vendor == 'fixsupply':
                    if zipcode:
                        scraped_item = getattr(module, module_name)(url, sku, zipcode, min_qty)
                    else:
                        scraped_item = getattr(module, module_name)(url, sku)
                else:
                    # aws_scraped_item = requests.post(
                    #     'https://z62qxy8y63.execute-api.us-west-1.amazonaws.com/quick-scrapes', payload=body_data)
                    scraped_item = getattr(module, module_name)(url, sku)

            elif vendor in api_funcs_list.local_api_funcs.keys():
                try:
                    local_response = requests.post('http://148.113.1.104:8762/quick-scrapes', json=body_data)
                    scraped_item = json.loads(local_response.text)
                    if scraped_item is None:
                        dev_error['error'] = 'Scraped item is None'
                        query = """
                            INSERT INTO api_request_logs (response_error, request_id, request_time, request_data,
                                request_api_key ) VALUES (%s, %s, %s, %s, %s)"""
                        values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data), api_key)
                        cursor.execute(query, values)
                        client.commit()
                        return update_table(status_code=503, error_message='Scraped item is None')
                except Exception as e:
                    return update_table(status_code=500, error_message=str(e))
            else:
                return update_table(status_code=400, error_message='Vendor website not set yet')

            try:
                # TODO: Optimise this part for site response's validation
                if scraped_item.get('statusCode') == 200:
                    item = scraped_item['data']
                    result = {}
                    keys = ['vendor', 'pdp_url', 'sku', 'price', 'lead_time', 'available_to_checkout', 'in_stock',
                            'cart_summary']
                    for k in keys:
                        if k == 'vendor':
                            if isinstance(item[k], str):
                                result[k] = item[k]
                        if k == 'pdp_url':
                            if isinstance(item[k], str):
                                result[k] = item[k]
                        if k == 'sku':
                            if isinstance(item[k], str):
                                result[k] = item[k]
                            else:
                                dev_error['error'] = f'Type error in response key {k}, expected str'

                                query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                          api_key)
                                cursor.execute(query, values)
                                client.commit()
                                return update_table(status_code=502,error_message=f'Type error in response key {k}, expected str')

                        if k == 'price':
                            if isinstance(item[k], list) and item[k]:
                                for price_data in item[k]:
                                    if 'price' in price_data.keys():
                                        if not isinstance(price_data['currency'], str) and not price_data['currency']:
                                            dev_error['error'] = f"Type error in response key currency, expected str"
                                            query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                            values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                      api_key)
                                            cursor.execute(query, values)
                                            client.commit()

                                            return update_table(status_code=502,error_message='Type error in response key currency, expected str')

                                        if not isinstance(price_data['min_qty'], int) and not price_data['min_qty']:
                                            dev_error['error'] = f"Type error in response key price min_qty, expected int"
                                            query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                            values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                      api_key)
                                            cursor.execute(query, values)
                                            client.commit()
                                            return update_table(status_code=502,error_message='Type error in response key price min_qty, expected int')

                                        if not isinstance(price_data['price'], float):
                                            dev_error['error'] = f"Type error in response key price, expected float"
                                            query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                            values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                      api_key)
                                            cursor.execute(query, values)
                                            client.commit()
                                            return update_table(status_code=502,
                                                                error_message='Type error in response key price, expected float')

                                    elif 'price_string' in price_data.keys():
                                        if not isinstance(price_data['price_string'], str) and not price_data['price_string']:
                                            dev_error['error'] = f"Type error in response key price_string, expected str"
                                            query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                            values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                      api_key)
                                            cursor.execute(query, values)
                                            client.commit()
                                            return update_table(status_code=502,
                                                                error_message='Type error in response key price_string, expected str')

                                        if not isinstance(price_data['min_qty'], int) and not price_data['min_qty']:
                                            dev_error['error'] = f"Type error in response key price min_qty, expected int received"
                                            query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                            values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                      api_key)
                                            cursor.execute(query, values)
                                            client.commit()
                                            return update_table(status_code=502,error_message='Type error in response key price min_qty, expected int received')

                                    else:
                                        dev_error['error'] = "Missing price data"
                                        query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                        values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                  api_key)
                                        cursor.execute(query, values)
                                        client.commit()
                                        return update_table(status_code=502, error_message='Missing price data')
                                result[k] = item[k]
                            else:
                                if item[k] is None:
                                    result[k] = item[k]

                        if k == 'lead_time':
                            if isinstance(item[k], list) and item[k]:
                                for lead_time_data in item[k]:
                                    if not isinstance(lead_time_data['min_qty'], int) and not lead_time_data['min_qty']:
                                        dev_error['error'] = f"Type error in response key lead_time min_qty, expected int received"
                                        query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                        values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                  api_key)
                                        cursor.execute(query, values)
                                        client.commit()
                                        return update_table(status_code=502,error_message=f"Type error in response key lead_time min_qty, expected int received")

                                    if 'time_to_ship' in lead_time_data.keys():
                                        if not isinstance(lead_time_data['time_to_ship'], dict) and not lead_time_data[
                                            'time_to_ship']:
                                            dev_error['error'] = f"Type error in response key time_to_ship, expected dict received"
                                            query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                            values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                      api_key)
                                            cursor.execute(query, values)
                                            client.commit()
                                            return update_table(status_code=502,error_message=f"Type error in response key time_to_ship, expected dict received")

                                    elif 'time_to_stock' in lead_time_data.keys():
                                        if not isinstance(lead_time_data['time_to_stock'], dict) and not lead_time_data[
                                            'time_to_stock']:
                                            dev_error['error'] = f"Type error in response key time_to_stock, expected dict received"
                                            query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                            values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                      api_key)
                                            cursor.execute(query, values)
                                            client.commit()
                                            return update_table(status_code=502,error_message=f"Type error in response key time_to_stock, expected dict received")

                                    elif 'time_to_arrive' in lead_time_data.keys():
                                        if not isinstance(lead_time_data['time_to_arrive'], dict) and not lead_time_data['time_to_arrive']:
                                            dev_error['error'] = f"Type error in response key time_to_arrive, expected dict received"
                                            query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                            values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                      api_key)
                                            cursor.execute(query, values)
                                            client.commit()
                                            return update_table(status_code=502, error_message=f"Type error in response key time_to_arrive, expected dict received")

                                    else:
                                        dev_error['error'] = 'Missing lead time data'
                                        query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                        values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                                  api_key)
                                        cursor.execute(query, values)
                                        client.commit()
                                        return update_table(status_code=502, error_message='Missing lead time data')
                                result[k] = item[k]
                            else:
                                if item[k] is None or item[k] == []:
                                    result[k] = item[k]

                        if k == 'available_to_checkout':
                            if isinstance(item[k], bool):
                                result[k] = item[k]
                            else:
                                dev_error['error'] = f"Type errorType error in response key {k}, expected bool in response key {k}, expected bool"
                                query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data),
                                          api_key)
                                cursor.execute(query, values)
                                client.commit()
                                return update_table(status_code=502, error_message=f"Type error in response key {k}, expected bool")
                        if k == 'in_stock':
                            if isinstance(item[k], bool):
                                result[k] = item[k]
                            else:
                                dev_error['error'] = f"Type error in response key {k}, expected bool"
                                query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                                values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data), api_key)
                                cursor.execute(query, values)
                                client.commit()
                                return update_table(status_code=502,error_message=f"Type error in response key {k}, expected bool")

                        if k == 'cart_summary':
                            try:
                                if isinstance(item[k], list) and item[k]:
                                    result[k] = item[k]
                                else:
                                    if item[k] is None:
                                        result[k] = item[k]
                            except:
                                pass
                    db_result = result
                    db_result['sku'] = db_result['sku'].replace('"', '').replace("'", '')
                    db_event = body_data
                    db_event['sku'] = db_event['sku'].replace('"', '').replace("'", '')

                    query = """INSERT INTO api_request_logs (response_data, request_data, request_id, request_time, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                    values = (json.dumps(db_result), json.dumps(db_event), request_id, utctime, api_key)
                    cursor.execute(query, values)
                    client.commit()
                    return update_table(status_code=200, body=db_result)

                elif scraped_item['statusCode'] == 404:
                    scraped_item.pop('statusCode')
                    if 'response' in scraped_item:
                        payload = {'request_id': request_id + f'_{scraped_item["response_status"]}',
                                   'page': scraped_item['response'], 'vendor': body_data['vendor']}
                        requests.post('http://51.91.80.95:7896/pagesave', json=payload)
                        scraped_item.pop('response')
                    else:
                        pass

                    query = """INSERT INTO api_request_logs (response_error, request_data, request_id, request_time, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                    values = (json.dumps(scraped_item), json.dumps(body_data), request_id, utctime, api_key)
                    cursor.execute(query, values)
                    client.commit()

                    return update_table(status_code=410, error_message="Product not found")
                elif scraped_item['statusCode'] == 408:
                    query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                    values = (json.dumps(scraped_item), request_id, utctime, json.dumps(body_data), api_key)
                    cursor.execute(query, values)
                    client.commit()
                    return update_table(status_code=408, error_message="Request timeout, failed to reach the host")

                elif scraped_item['statusCode'] == 410:
                    scraped_item.pop('statusCode')
                    query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                    values = (json.dumps(scraped_item), request_id, utctime, json.dumps(body_data), api_key)
                    cursor.execute(query, values)
                    client.commit()
                    return update_table(status_code=410, error_message="Product is discontinued")

                elif scraped_item['statusCode'] == 500:
                    err_msg_temp = scraped_item.get('error_message', 'SCRIPT SIDE ISSUE')
                    scraped_item.pop('statusCode')
                    if 'response' in scraped_item:
                        scraped_item.pop('response')
                    dev_error['error'] = f'LAMBDA ERROR RESPONSE: {err_msg_temp}'
                    query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                    values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data), api_key)
                    cursor.execute(query, values)
                    client.commit()
                    return update_table(status_code=500, error_message=f'LAMBDA ERROR RESPONSE: {err_msg_temp}')
                else:
                    return update_table(status_code=503, error_message="Lambda error in response")
            except Exception as e:
                dev_error['error'] = f'LAMBDA ERROR VALIDATION: {e}'
                query = """INSERT INTO api_request_logs (response_error, request_id, request_time, request_data, request_api_key) VALUES (%s, %s, %s, %s, %s)"""
                values = (json.dumps(dev_error), request_id, utctime, json.dumps(body_data), api_key)
                cursor.execute(query, values)
                client.commit()
                return update_table(status_code=502,error_message=f'LAMBDA ERROR VALIDATION: {e}')
    except Exception as e:
        return update_table(status_code=503, error_message=str(e))


# if __name__ == '__main__':
#      import event
#      print(lambda_handler(event=event.event, context=''))
