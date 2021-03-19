from flask import Blueprint, render_template, url_for, abort, redirect, flash, session
import requests
import json

from ...config import ConfigCart, ConfigCatalog

cart = Blueprint('cart', __name__, template_folder='./templates')


@cart.route("/cart")
def view():
    user = session['user_id']
    res_cart = requests.get(f"http://{ConfigCart.HOST}:{ConfigCart.PORT}/v1/cart/{user}")

    if res_cart.status_code == 200:
        cart = json.loads(res_cart.text)
        return render_template('cart_view.html', cart=cart, title="My Cart")

    return render_template('cart_view.html', title="My Cart")


@cart.route("/cart/checkout")
def checkout():
    user = session['user_id']
    res_cart = requests.get(f"http://{ConfigCart.HOST}:{ConfigCart.PORT}/v1/cart/{user}")

    if res_cart.status_code == 200:
        cart = json.loads(res_cart.text)

        for item in cart['items']:
            requests.put(f"http://{ConfigCatalog.HOST}:{ConfigCatalog.PORT}/v1/item/{item['id']}/stock/{-item['quantity']}")

        requests.delete(f"http://{ConfigCart.HOST}:{ConfigCart.PORT}/v1/cart/{user}/checkout")

        flash("Processing Order", "info")
    else:
        flash("Error", "error")

    return redirect(url_for("base.home"))


@cart.route("/cart/delete/<item_id>", methods=["GET", "POST"])
def delete(item_id):
    user = session['user_id']
    item = {"item_id": item_id}
    response = requests.delete(f"http://{ConfigCart.HOST}:{ConfigCart.PORT}/v1/cart/{user}/removeItem", json=item)

    if response.status_code == 200:
        flash("Item removed", "info")
    else:
        flash("Error", "error")

    return redirect(url_for("cart.view"))
