from fastapi import APIRouter, HTTPException
from elasticsearch import Elasticsearch

from ..config import ConfigElastic
from .utility import item2dict
from .model import Item

es = Elasticsearch([ConfigElastic.HOST], maxsize=12)

v1 = APIRouter(
    prefix="/v1"
)


# Items
@v1.get('/item/{item_id}', tags=["v1", "Item"])
async def get_item(
        item_id: str,
):
    '''
    Return a single item.
    '''
    response = es.get(index="inventory", id=item_id, ignore=404)

    if response['found']:
        return response['_source']

    raise HTTPException(status_code=404, detail="Item doesn't exists")


@v1.post('/item/{item_id}', tags=["v1", "Item"])
async def create_item(
        item_id: str,
        item: Item
):
    '''
    Create an item.
    '''
    response = es.index(index="inventory", id=item_id, body=item2dict(item_id, item))

    return response

    if response['result'] != 'created':
        raise HTTPException(status_code=500, detail="Server Error")


@v1.put('/item/{item_id}', tags=["v1", "Item"])
async def update_item(
    item_id: str,
    item: Item
):
    '''
    Update an item.
    '''
    response = es.update(index="inventory", id=item_id, body={"doc": item2dict(item_id, item)}, ignore=404)

    if response['status'] == 404:
        raise HTTPException(status_code=404, detail="Item doesn't exists")


@v1.delete('/item/{item_id}', tags=['v1', 'Item'])
async def delete_item(
    item_id: str
):
    '''
    Remove an item from the store
    '''
    response = es.delete(index="inventory", id=item_id, ignore=404)

    if response['result'] == 'not_found':
        raise HTTPException(status_code=404, detail="Item doesn't exists")
    elif response['result'] != 'deleted':
        raise HTTPException(status_code=500, detail="Server Error")


@v1.put('/item/{item_id}/stock/{change}', tags=["v1", "Item"])
async def update_item_stock(
    item_id: str,
    change: int
):
    '''
    Add or remove stock of an item.
    '''
    response = es.get(index="inventory", id=item_id, ignore=404)

    if response['found']:
        newStock = response['_source']['stock'] + change
        es.update(index="inventory", id=item_id, body={"doc": {"stock": newStock}})

    raise HTTPException(status_code=404, detail="Item doesn't exists")


# Search
@v1.get('/search', tags=["v1", "Search"])
async def search_all():
    '''
    Search for an item with basic parameters
    '''
    query = {
        "query": {
            "match_all": {
            }
        }
    }

    response = es.search(index="inventory", body=query)

    return [x['_source'] for x in response['hits']['hits']]
