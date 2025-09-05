import pymongo
import datetime


class ConfigMongo:
    def __init__(self):
        """
        Define database collection and all the required database here
        """
        try:
            current_datetime = datetime.datetime.now(datetime.timezone.utc)
            current_month = current_datetime.strftime('%Y_%m')
            self.con = pymongo.MongoClient("mongodb://actowiz:tvvL4n%3D33%3D*_@51.222.244.92:27017/admin?authSource=admin")
            self.db = self.con['ics_api']
            self.log_master = self.db[f'logs_table_{current_month}']
            self.project_master_api = self.db["key_tables"]
            self.proxy_keys = self.db["proxy_keys"]
        except:
            pass

    def get_assign_proxy(self, proxy_name='scrap_do'):
        """
        Get proxy.
        Can be expanded to consider multiple proxies for multiple endpoints by adding a database with the assign proxy name to the endpoint
        :return: proxy key/string or {}
        """
        try:
            return self.proxy_keys.find_one({'proxy_name':proxy_name}, {'_id': 0, 'proxy_key': 1}).get('proxy_key', None)
        except Exception as e:
            return None

    def insert_storage_log(self, log):
        """
        Register the incoming request to the database with status 201.
        :param log: Required log details
        :return: None
        """
        try:
            self.log_master.insert_one(log)
        except Exception as er:
            print(f"Error in db log insert: {er}")

    def update_storage_log(self, query, request_id):
        """
        Update registered request with new status and its details
        :param query: update query dictionary
        :param request_id: Unique request log id
        :return: None
        """
        try:
            self.log_master.update_one({'request_id': request_id}, {'$set': query})
        except Exception as er:
            pass

    def add_apiKey_usage(self, apiKey):
        """
        Update key usage by 1 based on the condition
        :param apiKey: api key to be updated
        :return: None
        """
        try:
            self.project_master_api.update_one({"key": apiKey}, {"$inc": {"usage": 1}})
        except Exception as er:
            print(f"Error in db usage increment: {er}")

    def check_usage(self,apiKey):
        res = self.project_master_api.find_one({"key": f'{apiKey}'}, {'_id': 0, 'limit': 1, 'usage': 1})
        return True if res.get('usage', 0) <= res.get('limit', 0) else False

    def authenticate_apiKey(self, apiKey):
        """
        Authenticate the api key and provide its current status
        :param apiKey: api key to be checked
        :return: True - if the key is valid and active, and its usage limit is less then allocated limit
                 False - for all the other states
        """
        try:
            res = self.project_master_api.find_one({"key": f'{apiKey}', "status": True}, {'_id': 0, 'limit': 1, 'usage': 1})
            return True if res and res.get('total_usage', 0) <= res.get('usage_limit', 0) else False
        except Exception as er:
            print(f"Error in db authentication token: {er}")
            return False