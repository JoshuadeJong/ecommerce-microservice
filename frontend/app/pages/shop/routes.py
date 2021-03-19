from flask import Blueprint, render_template, url_for, abort, redirect, flash, session
import requests
import json

from ...config import ConfigCatalog

shop = Blueprint('shop', __name__, template_folder='./templates')


@shop.route('/shop')
def view():

    response = requests.get(f"http://{ConfigCatalog.HOST}:{ConfigCatalog.PORT}/v1/search")

    if response.status_code == 200:
        items = json.loads(response.text)

        return render_template('shop.html', items=items, title='Shop')

    abort(500)

