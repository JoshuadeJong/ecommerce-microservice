from fastapi import APIRouter, HTTPException
from typing import Optional
import json
import redis


from ..config import ConfigRedis
from .utility import key, time, manager, newItem, newCart, items2list
from .model import Item

cursor = redis.Redis(host=ConfigRedis.HOST, port=ConfigRedis.PORT, db=1)

v1 = APIRouter(
    prefix="/v1"
)


# Carts
@v1.get('/cart', tags=["v1", 'Cart'])
async def get_all_carts(
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
        fields: Optional[str] = None
):
    '''
    Get all customer carts.
    '''

    carts = []
    for key in cursor.scan_iter('v1_*'):
        cart = cursor.get(key)
        cart = json.loads(cart)
        cart['items'] = items2list(cart['items'])
        carts.append(cart)

    args = {"limit": limit, "offset": offset, "fields": fields}
    return manager(carts, args)


@v1.get('/cart/{customer_id}', tags=["v1", 'Cart'])
async def get_customer_cart(
    customer_id: int,
    fields: Optional[str] = None
):
    '''
    Return a single customer's cart.
    '''

    cart = cursor.get(key(customer_id))

    if not cart:
        raise HTTPException(status_code=404, detail="Cart doesn't exists")

    cart = json.loads(cart)
    cart['items'] = items2list(cart['items'])

    return manager(cart, {"fields": fields})


@v1.post('/cart/{customer_id}', tags=['v1', 'Cart'])
async def create_customer_cart(
        customer_id: int
):
    '''
    Create a new customer cart.
    '''

    # Check if a cart exists
    if cursor.exists(key(customer_id)):
        raise HTTPException(status_code=401, detail="Cart already exists")

    # Create a new cart
    response = cursor.set(key(customer_id), json.dumps(newCart(customer_id)))

    if not response:
        raise HTTPException(status_code=500, detail="Cart creation failed")


@v1.post('/cart/{customer_id}/addItem', response_model=Item, tags=["v1", 'Item'])
async def add_item(
        customer_id: int,
        item: Item
):
    '''
    Add an item to a customer's cart. If the cart doesn't exists create a cart.
    '''

    # Get or build a new cart
    cart = cursor.get(key(customer_id))
    if cart:
        cart = json.loads(cart)
    else:
        cart = newCart(customer_id)

    # Add item to cart
    if item.id in cart['items']:
        cart['items'][item.id]['quantity'] += item.quantity
        cart['items'][item.id]['timestamp'] = time()
    else:
        cart['items'][item.id] = newItem(item)

    cart['total_price'] += item.price * item.quantity
    cart['total_count'] += item.quantity
    cart['timestamp'] = time()

    # Add cart to database
    response = cursor.set(key(customer_id), json.dumps(cart))

    if not response:
        raise HTTPException(status_code=500, detail="Failed to add an item.")


@v1.put('/cart/{customer_id}/quantity', tags=['v1', 'Item'])
async def change_quantity(
        customer_id: int,
        item_id: str,
        newQuantity: int
):
    '''
    Set the quantity for an item.
    '''

    # Check quantity
    if newQuantity < 0:
        raise HTTPException(status_code=406, detail="Quantity below zero")

    # Get and check if cart exists
    cart = cursor.get(key(customer_id))
    if not cart:
        raise HTTPException(status_code=404, detail="Cart does not exist")

    cart = json.loads(cart)

    # Check if item is in cart
    if item_id not in cart['items']:
        raise HTTPException(status_code=406, detail="Item does not exist in the cart.")

    # update price and quantity
    oldQuantity = cart['items'][item_id]['quantity']
    cart['items'][item_id]['quantity'] = newQuantity
    cart['total_price'] += cart['items'][item_id]['price'] * (newQuantity - oldQuantity)
    cart['total_count'] += newQuantity - oldQuantity

    # if item quantity is zero remove from cart
    if cart['items'][item_id]['quantity'] == 0:
        cart['items'].pop(item_id)

    # Add to database
    response = cursor.set(key(customer_id), json.dumps(cart))

    if not response:
        raise HTTPException(status_code=500)


@v1.put('/cart/{customer_id}/price', tags=['v1', 'Item'])
async def change_price(
        customer_id: int,
        item_id: str,
        newPrice: float
):
    '''
    Set a new price for an item.
    '''

    # Check quantity
    if newPrice < 0:
        raise HTTPException(status_code=406, detail="Price below zero")

    # Get and check if cart exists
    cart = cursor.get(key(customer_id))
    if not cart:
        raise HTTPException(status_code=404, detail="Cart does not exist")

    cart = json.loads(cart)

    # Check if item is in cart
    if item_id not in cart['items']:
        raise HTTPException(status_code=406, detail="Item does not exist in the cart.")

    # update prices and total price
    oldPrice = cart['items'][item_id]['price']
    cart['items'][item_id]['price'] = newPrice
    cart['total_price'] += cart['items'][item_id]['quantity'] * (newPrice - oldPrice)

    # Add to database
    response = cursor.set(key(customer_id), json.dumps(cart))

    if not response:
        raise HTTPException(status_code=500)


@v1.delete('/cart/{customer_id}/removeItem', response_model=Item, tags=["v1", 'Item'])
async def remove_item(customer_id: int, item_id: str):
    '''
    Remove an item from the cart.
    '''

    # Get and check if cart exists
    cart = cursor.get(key(customer_id))
    if not cart:
        raise HTTPException(status_code=404, detail="Cart does not exist")

    cart = json.loads(cart)

    # Check if item is in cart
    if item_id not in cart['items']:
        raise HTTPException(status_code=406, detail="Item does not exist in the cart.")

    # Remove item
    price = cart['items'][item_id]['price']
    quantity = cart['items'][item_id]['quantity']
    cart['items'].pop(item_id)

    # Update price and item count
    cart['total_price'] -= price * quantity
    cart['total_count'] -= quantity

    # Add to database
    response = cursor.set(key(customer_id), json.dumps(cart))

    if not response:
        raise HTTPException(status_code=500)


@v1.delete('/cart/{customer_id}/checkout', tags=["v1", 'Checkout'])
async def checkout(customer_id: int):
    '''
    Clear the cart.
    '''

    response = cursor.delete(key(customer_id))

    if not response:
        raise HTTPException(status_code=500, detail="Failed to checkout the cart.")
