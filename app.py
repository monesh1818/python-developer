from flask import Flask, request, jsonify

app = Flask(__name__)

inventory = [
    {"name": "Widget", "quantity": 10}
]

@app.route('/inventory', methods=['GET'])
def get_inventory():
    """Fetch the current inventory list."""
    return jsonify({"inventory": inventory}), 200

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    """Update the quantity of an existing item."""
    data = request.json
    name = data.get("name")
    change = data.get("quantity")

    if not isinstance(change, int):  # Ensure quantity is a number
        return jsonify({"error": "Invalid quantity value"}), 400

    for item in inventory:
        if item["name"].lower() == name.lower():
            item["quantity"] = max(0, item["quantity"] + change)  # Prevent negative stock
            return jsonify({"message": f"Updated {name} to {item['quantity']}"}), 200

    return jsonify({"error": "Item not found"}), 404

@app.route('/add-item', methods=['POST'])
def add_item():
    """Add a new item to the inventory."""
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity")

    if not name or not isinstance(quantity, int) or quantity < 0:
        return jsonify({"error": "Invalid item name or quantity"}), 400

    for item in inventory:
        if item["name"].lower() == name.lower():
            return jsonify({"error": "Item already exists"}), 400

    inventory.append({"name": name, "quantity": quantity})
    return jsonify({"message": f"Added {name} with quantity {quantity}"}), 200

@app.route('/remove-item', methods=['POST'])
def remove_item():
    """Remove an item from the inventory."""
    data = request.json
    name = data.get("name")

    global inventory
    new_inventory = [item for item in inventory if item["name"].lower() != name.lower()]

    if len(new_inventory) == len(inventory):  # If no item was removed
        return jsonify({"error": "Item not found"}), 404

    inventory = new_inventory  # Update the inventory list
    return jsonify({"message": f"Removed {name}"}), 200

if __name__ == '__main__':
    app.run(debug=True)
