from flask import Flask, render_template, request, redirect 
import sqlite3 as sql
from datetime import datetime

app = Flask("inventoryApp")

conn = sql.connect("inventory.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, quantity INTEGER, unit TEXT, last_updated TEXT)")
conn.commit()
@app.route("/", methods=["GET", "POST"])

def main_login_page():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "admin@gmail.com" and password == "admin":
            return redirect("/dashboard")
    return render_template("login.html")



@app.route("/dashboard")
def dashboard():
    inventory = cursor.execute("SELECT * FROM inventory")
    inventory = inventory.fetchall()
    print(inventory)

    return render_template("dashboard.html", inventory=inventory)


@app.route("/update_inventory", methods=["POST"])
def update_inventory():
    

    item_name = request.form["item"]
    quantity_change = int(request.form["quantity"])

    current_item = cursor.execute("SELECT quantity FROM inventory WHERE name = ?", (item_name,)).fetchone()
    new_quantity = current_item[0] + quantity_change
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE inventory SET quantity = ?, last_updated = ? WHERE name = ?", 
                  (new_quantity, last_updated, item_name))
    conn.commit()
    return redirect("/dashboard")


@app.route("/new_item", methods=["GET", "POST"])
def new_item():
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        unit = request.form["unit"]
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO inventory (name, quantity, unit, last_updated) VALUES (?, ?, ?, ?)", (name, quantity, unit, last_updated))
        conn.commit()
        return redirect("/dashboard")
    return render_template("new_item.html")




if __name__ == "__main__": 
    app.run(debug=True)
