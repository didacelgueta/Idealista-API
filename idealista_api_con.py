from httplib2 import Http
import pandas as pd
import base64
import json
import urllib
import os



class CallApi:

    API_PUBLIC = os.environ.get("PUBLIC_KEY")
    API_SECRET = os.environ.get("SECRET_KEY")

    def __init__(self):
        self.token = self.get_oauth_token()

    # Function to get token
    @staticmethod
    def get_oauth_token():
        http_obj = Http()
        url = "https://api.idealista.com/oauth/token"
        key = API_PUBLIC + ":" + API_SECRET
        # Encode key to base64
        key_bytes = key.encode('ascii')
        key_base64 = base64.b64b64encode(key_bytes)
        auth = key_base64.decode('ascii')
        body = {'grant_type':'client_credentials','scope':'read'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8','Authorization' : auth}
        resp, content = http_obj.request(url,method='POST', headers=headers, body=urllib.parse.urlencode(body))
        content = json.loads(content)
        return content["access_token"]

    # Function to request api and save data in json
    def search_api(self):
        http_obj = Http()
        country = 'es'
        operation = 'sale'
        propertyType = 'homes'
        center = '41.3887901,2.1589899'
        locale = 'es'
        distance = '10000'
        maxItems = '50'
        #numPage = '2'
        maxPrice = '2000000'
        minPrice = '100000'
        sinceDate = 'M'
        pages = 101
        df = pd.DataFrame()
        for page in range(1, pages):
            url = ("http://api.idealista.com/3.5/"+country+"/search?operation="+operation+
                "&propertyType="+propertyType+
                "&center="+center+
                "&locale="+locale+
                "&distance="+distance+
                "&maxItems="+maxItems+
                "&numPage=%s"+
                "&maxPrice"+maxPrice+
                "&minPrice"+minPrice+
                "&sinceDate"+sinceDate) %(page)
            headers = {'Authorization' : 'Bearer ' + self.token}
            print(headers)
            resp, content = http_obj.request(url, method='POST', headers=headers)
            print(content)
            response = json.loads(content)
            df_aux = pd.DataFrame(response['elementList'])
            df = df.append(df_aux, ignore_index=True, sort=False)
        print(df)
        df.to_csv('./data.csv')
        return None


call = CallApi()
call.search_api()
