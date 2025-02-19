from flask import Flask, render_template, request, redirect 

from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("/etc/secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


app = Flask("inventoryApp")


db = firestore.client()
items_ref = db.collection("Itmes")


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

    items = items_ref.get()

    item_list = []
    for item in items:
        item_list.append(item.to_dict())
        
    

    return render_template("dashboard.html", inventory=item_list)


@app.route("/update_inventory", methods=["POST"])
def update_inventory():
    

    item_name = request.form["item"]
    quantity_change = int(request.form["quantity"])

    current_item = items_ref.document(item_name).get().to_dict()
    new_quantity = int(current_item["quantity"]) + quantity_change
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    items_ref.document(item_name).update({"last_update": last_updated, "quantity":new_quantity})


    return redirect("/dashboard")


@app.route("/new_item", methods=["GET", "POST"])
def new_item():
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        unit = request.form["unit"]
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        items_ref.document(name).set({
            "name": name,
            "quantity": quantity,
            "unit": unit,
            "last_update": last_updated
        })

        return redirect("/dashboard")
    return render_template("new_item.html")




if __name__ == "__main__": 
    app.run(debug=True)
