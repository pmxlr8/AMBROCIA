import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Add a secret key for session management

# Replace the placeholders with your actual MySQL connection details
host = "localhost"
user = "root"
password = "pranjal@214022"
database = "ambrocia"

db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)


@app.route('/')
def login_page():
    return render_template('Login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    result = login_user(username, password)
    if result:
        session['username'] = username  # Store the username in the session
        return redirect(url_for('dashboard'))
    else:
        return "Invalid username or password"
@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        customer_name = session['username']
        items = []
        total_amount = 0
        
        # Get the quantities of each item from the form
        quantity_butter_chicken = int(request.form['quantity_butter_chicken'])
        quantity_paneer_tikka = int(request.form['quantity_paneer_tikka'])
        quantity_masala_dosa = int(request.form['quantity_masala_dosa'])
        quantity_chicken_biryani = int(request.form['quantity_chicken_biryani'])
        quantity_palak_paneer = int(request.form['quantity_palak_paneer'])
        quantity_gulab_jamun = int(request.form['quantity_gulab_jamun'])
        
        # Calculate the price for each item
        price_butter_chicken = 300
        price_paneer_tikka = 250
        price_masala_dosa = 150
        price_chicken_biryani = 250
        price_palak_paneer = 200
        price_gulab_jamun = 100
        
        # Calculate the total amount
        total_amount = (
            quantity_butter_chicken * price_butter_chicken +
            quantity_paneer_tikka * price_paneer_tikka +
            quantity_masala_dosa * price_masala_dosa +
            quantity_chicken_biryani * price_chicken_biryani +
            quantity_palak_paneer * price_palak_paneer +
            quantity_gulab_jamun * price_gulab_jamun
        )
        
        # Create item objects with their names, quantities, and prices
        if quantity_butter_chicken > 0:
            items.append({'name': 'Butter Chicken', 'quantity': quantity_butter_chicken, 'price': price_butter_chicken})
        if quantity_paneer_tikka > 0:
            items.append({'name': 'Paneer Tikka', 'quantity': quantity_paneer_tikka, 'price': price_paneer_tikka})
        if quantity_masala_dosa > 0:
            items.append({'name': 'Masala Dosa', 'quantity': quantity_masala_dosa, 'price': price_masala_dosa})
        if quantity_chicken_biryani > 0:
            items.append({'name': 'Chicken Biryani', 'quantity': quantity_chicken_biryani, 'price': price_chicken_biryani})
        if quantity_palak_paneer > 0:
            items.append({'name': 'Palak Paneer', 'quantity': quantity_palak_paneer, 'price': price_palak_paneer})
        if quantity_gulab_jamun > 0:
            items.append({'name': 'Gulab Jamun', 'quantity': quantity_gulab_jamun, 'price': price_gulab_jamun})
        
        # Store the order details in the database or perform any other necessary actions
        
        return render_template('generate_bill.html', customer_name=customer_name, items=items, total_amount=total_amount)
    
    return render_template('place_order.html')
@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    # Get the form data
    name = request.form['name']
    address = request.form['address']
    card_number = request.form['card_number']

    # Retrieve the items and total amount from the form data
    items = []
    total_amount = 0

    # Get the quantities of each item from the form
    quantity_butter_chicken = int(request.form['quantity_butter_chicken'])
    quantity_paneer_tikka = int(request.form['quantity_paneer_tikka'])
    quantity_masala_dosa = int(request.form['quantity_masala_dosa'])
    quantity_chicken_biryani = int(request.form['quantity_chicken_biryani'])
    quantity_palak_paneer = int(request.form['quantity_palak_paneer'])
    quantity_gulab_jamun = int(request.form['quantity_gulab_jamun'])

    # Calculate the price for each item
    price_butter_chicken = 300
    price_paneer_tikka = 250
    price_masala_dosa = 150
    price_chicken_biryani = 250
    price_palak_paneer = 200
    price_gulab_jamun = 100

    # Calculate the total amount
    total_amount = (
        quantity_butter_chicken * price_butter_chicken +
        quantity_paneer_tikka * price_paneer_tikka +
        quantity_masala_dosa * price_masala_dosa +
        quantity_chicken_biryani * price_chicken_biryani +
        quantity_palak_paneer * price_palak_paneer +
        quantity_gulab_jamun * price_gulab_jamun
    )

    # Create item objects with their names, quantities, and prices
    if quantity_butter_chicken > 0:
        items.append({'name': 'Butter Chicken', 'quantity': quantity_butter_chicken, 'price': price_butter_chicken})
    if quantity_paneer_tikka > 0:
        items.append({'name': 'Paneer Tikka', 'quantity': quantity_paneer_tikka, 'price': price_paneer_tikka})
    if quantity_masala_dosa > 0:
        items.append({'name': 'Masala Dosa', 'quantity': quantity_masala_dosa, 'price': price_masala_dosa})
    if quantity_chicken_biryani > 0:
        items.append({'name': 'Chicken Biryani', 'quantity': quantity_chicken_biryani, 'price': price_chicken_biryani})
    if quantity_palak_paneer > 0:
        items.append({'name': 'Palak Paneer', 'quantity': quantity_palak_paneer, 'price': price_palak_paneer})
    if quantity_gulab_jamun > 0:
        items.append({'name': 'Gulab Jamun', 'quantity': quantity_gulab_jamun, 'price': price_gulab_jamun})

    # Perform the database insertion
    cursor = db.cursor()
    query = "INSERT INTO orders (name, address, card_number, total_amount) VALUES (%s, %s, %s, %s)"
    values = (name, address, card_number, total_amount)
    cursor.execute(query, values)
    order_id = cursor.lastrowid

    # Insert the items into the order_items table
    for item in items:
        item_name = item['name']
        quantity = item['quantity']
        price = item['price']

        query = "INSERT INTO order_items (order_id, item_name, quantity, price) VALUES (%s, %s, %s, %s)"
        values = (order_id, item_name, quantity, price)
        cursor.execute(query, values)

    db.commit()
    cursor.close()

    return redirect(url_for('thank_you'))


@app.route('/register', methods=['POST'])
def register():
    full_name = request.form['full_name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return "Passwords do not match"

    register_user(username, full_name, email, password)
    return "Registration successful"


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        card_number = request.form['card_number']
        
        # Save the billing details to the database or perform any other necessary actions
        
        return redirect(url_for('thank_you'))
    
    return render_template('billing.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:  # Check if the username is stored in the session
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login_page'))



@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the stored username from the session
    return redirect(url_for('login_page'))


@app.route('/New_account.html')
def new_account():
    return render_template('New_account.html')


def register_user(username, full_name, email, password):
    cursor = db.cursor()
    query = "INSERT INTO customers (username, full_name, email, password) VALUES (%s, %s, %s, %s)"
    values = (username, full_name, email, password)
    cursor.execute(query, values)
    db.commit()
    cursor.close()


def login_user(username, password):
    cursor = db.cursor()
    query = "SELECT * FROM customers WHERE username = %s AND password = %s"
    values = (username, password)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    return result
def register_user(username, full_name, email, password, name, address, card_number):
    cursor = db.cursor()
    query = "INSERT INTO customers (username, full_name, email, password) VALUES (%s, %s, %s, %s)"
    values = (username, full_name, email, password)
    cursor.execute(query, values)
    db.commit()
    
    # Get the inserted customer's ID
    customer_id = cursor.lastrowid
    
    # Insert billing details into the billing table
    query = "INSERT INTO billing (customer_id, name, address, card_number) VALUES (%s, %s, %s, %s)"
    values = (customer_id, name, address, card_number)
    cursor.execute(query, values)
    db.commit()
    
    cursor.close()


if __name__ == '__main__':
    app.run()