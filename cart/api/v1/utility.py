from datetime import datetime
from .model import Item


# Data Functions
def newItem(item: Item) -> dict:
    '''
    Return a json form of a new item
    '''
    return {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "quantity": item.quantity,
        "timestamp": time()
    }


def newCart(customer_id):
    '''
    Create a new customer cart
    '''
    return {
        "customer_id": customer_id,
        "total_price": 0,
        "total_count": 0,
        "timestamp": time(),
        "items": {}
    }


# Helper Methods
def key(customer_id) -> str:
    '''
    Create the lookup key for redis
    '''
    return f"v1_{customer_id}"


def time() -> str:
    '''
    Create a timestamp
    '''
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def items2list(items: dict) -> list:
    output = []
    for key, value in items.items():
        value['id'] = key
        output.append(value)

    return output


# Output Formatter
def manager(data, args: dict):
    '''
    Applies utilities functions to mutate the data.
    :param data: a list or dict of json data
    :param args: a dictionary of arguments
    :return: a list or dict of mutated json data
    '''

    if "fields" in args:
        data = fields(data, args["fields"])

    if type(data) == list:

        if "offset" in args:
            data = offset(data, args["offset"])

        if "limit" in args:
            data = limit(data, args["limit"])

    return data


def limit(data: list, num: int) -> list:
    '''
    Returns all elements before num
    :param data: a list of json data
    :param num: an index integer
    :return:
    '''
    if num is None or type(num) != int:
        return data

    return data[:num]


def offset(data: list, num: int) -> list:
    '''
    Returns all elements after nums
    :param data: a list of json data
    :param num: an index integer
    :return:
    '''
    if num is None or type(num) != int:
        return data

    return data[num:]


def fields(data, keys: str):
    '''
    Return only requested fields from a list of dicts or a dict.
    :param data: A list or a dict of json data
    :param keys: a comma delimited string of fields
    :return: A list or dict of json data
    '''
    if keys is None or type(keys) != str:
        return data

    keys = set(keys.split(','))

    if type(data) == list:
        return _fieldsList(data, keys)
    elif type(data) == dict:
        return _fieldsDict(data, keys)


def _fieldsList(data: list, keys: set) -> list:
    '''
    Return a list of dictionaries which only contain the requested fields.
    :param data: The requested data
    :param keys: The requested fields from the data
    :return: A list of dicts only containing the requested fields
    '''

    remove = []
    for index in range(len(data)):
        if type(data[index]) == dict:
            data[index] = _fieldsDict(data[index], keys)

            # record if the entry is empty
            if data[index] == {}:
                remove.append(index)

    # Pop out all empty entries
    for index in remove[::-1]:
        data.pop(index)

    return data


def _fieldsDict(data: dict, keys: set) -> dict:
    '''
    Return only requested fields from a dict.
    :param data: The requested data
    :param keys: The requested fields from the data
    :return: A dict only containing the requested fields
    '''

    remove = set(data.keys()) - keys
    for key in remove:
        data.pop(key)

    return data

