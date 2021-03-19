from flask import Blueprint, render_template, url_for, abort, redirect, flash, session
import requests
import json

from ...config import ConfigCatalog, ConfigCart
from .forms import CreateItem, UpdateItem, BuyItem


item = Blueprint('item', __name__, template_folder='./templates')


@item.route('/create_item', methods=['GET', 'POST'])
def create():

    form = CreateItem()
    if form.validate_on_submit():
        item = {
            "name": form.data['name'],
            "description": form.data['description'],
            "price": form.data['price'],
            "stock": form.data['stock']
        }

        response = requests.post(f"http://{ConfigCatalog.HOST}:{ConfigCatalog.PORT}/v1/item/{form.data['id']}", json=item)

        if response.status_code == 200:
            flash("Item Created", "info")
            return redirect(url_for("shop.view"))

        flash("Error", "error")

    return render_template('create_item.html', form=form)


@item.route('/item/<item_id>/delete', methods=['GET', 'POST'])
def delete(item_id):

    response = requests.delete(f"http://{ConfigCatalog.HOST}:{ConfigCatalog.PORT}/v1/item/{item_id}")

    if response.status_code == 200:
        flash("Item deleted", "info")
    else:
        flash("Error", "error")

    return redirect(url_for("base.home"))


@item.route('/item/<item_id>/update', methods=['GET', 'POST'])
def update(item_id):
    pass


@item.route('/item/<item_id>', methods=["GET", "POST"])
def view(item_id):

    res_catalog = requests.get(f"http://{ConfigCatalog.HOST}:{ConfigCatalog.PORT}/v1/item/{item_id}")

    if res_catalog.status_code == 200:
        item = json.loads(res_catalog.text)

        form = BuyItem()
        if form.validate_on_submit():

            if item['stock'] - form.data['quantity'] < 0:
                flash("Item backorder", category="info")

            user = session["user_id"]
            order = {
                "id": item['id'],
                "name": item['name'],
                "description": item["description"],
                "price": item["price"],
                "quantity": form.data['quantity']
            }
            res_cart = requests.post(f"http://{ConfigCart.HOST}:{ConfigCart.PORT}/v1/cart/{user}/addItem", json=order)

            if res_cart.status_code == 200:
                return redirect(url_for("cart.view"))
            else:
                flash("Purchase Failed", category="error")

        return render_template('item.html', item=item, title=item['name'], form=form)

    elif res_catalog.status_code == 404:
        return abort(404)

    return abort(500)
