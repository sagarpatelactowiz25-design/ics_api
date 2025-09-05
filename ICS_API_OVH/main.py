import hashlib
import json
import datetime
import pymysql
from galco import galco
from fastapi import FastAPI, Request
from pydantic import BaseModel
from api_key_list import local_api_funcs
from accugroup import accugroup
from biscoind import biscoind
from coleparmer import coleparmer
from edmundoptics import edmundoptics
from graybar import graybar
from iewc import iewc
from knightoptical import knightoptical
from lowes import lowes
from motionindustries import motionindustries
from mscdirect import mscdirect
from professionalplastics import professionalplastics
from supplyhouse import supplyhouse
from teconnectivity import teconnectivity
from tequipment import tequipment
from fastenal import fastenal
from northerntool import northerntool
from fastapi.responses import JSONResponse

app = FastAPI()

class Item(BaseModel):
    pdp_url: str
    sku: str
    vendor: str

@app.post("/quick-scrapes")
def create_item(item: Item, request: Request, jsons=None):
    event = dict(item)
    pdp_url = event['pdp_url']
    sku = event['sku']
    vendor = event['vendor']

    storename = ""

    for store in local_api_funcs:
        if vendor == store:
            storename = local_api_funcs[store]

    try:
        output = (eval(f'''{storename}(pdp_url="{pdp_url}", sku="{sku}", vendor="{vendor}")'''))
        return JSONResponse(status_code=output["statusCode"], content=output)
        # return output
    except Exception as e:
        return {'statusCode': 500,
                'error_message': 'Internal sever error_sql' + str(e)}
try:
    if __name__ == '__main__':
        import uvicorn
        uvicorn.run('main:app', host="148.113.1.104", port=8762, log_level="debug", reload=True)
except Exception as e:
    print(str(e))