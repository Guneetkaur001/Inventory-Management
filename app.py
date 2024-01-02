from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
import os

app.secret_key = os.urandom(24)  # Set a secure secret key for session security
# Define your products
products = [
    {"name": "Ladies Coat", "price": 250},
    {"name": "Geants Coat", "price": 250},
    {"name": "Hoodie", "price": 200},
    {"name": "Smart Phone", "price": 10000},
    {"name": "Tops", "price": 200},
    {"name": "Jackets", "price": 400}
]

@app.route("/shop", methods=['GET', 'POST'])
def shop():
    # Retrieve or initialize the cart_items list from the session
    cart_items = session.get('cart_items', [])

    subtotal = sum(item["subtotal"] for item in cart_items)  # Calculate subtotal
    tax_amount = subtotal * 0.05  # Example tax calculation
    net_bill = subtotal + tax_amount  # Example net bill calculation

    if request.method == 'POST':
        pname = request.form.get('productName')
        qty = int(request.form.get('quantity'))

        product = next((p for p in products if p["name"] == pname), None)

        if product:
            cart_item = {
                "name": product["name"],
                "price": product["price"],
                "quantity": qty,
                "subtotal": product["price"] * qty
            }

            cart_items.append(cart_item)  # Update the cart_items list

            # Save the updated cart_items list back to the session
            session['cart_items'] = cart_items

    return render_template('shop.html', products=products, cart_items=cart_items, subtotal=subtotal, tax_amount=tax_amount, net_bill=net_bill)

@app.route("/clear_cart", methods=['POST'])
def clear_cart():
    # Clear the cart by removing 'cart_items' from the session
    session.pop('cart_items', None)
    return redirect(url_for('shop'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
