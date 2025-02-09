# python-developer
Inventory Management System (Blender + Flask + PySide)

📌 Overview

This project integrates Blender, Flask, and PySide to create an inventory management system. It allows users to:

Add, update, and remove items from an inventory.

Sync object transformations from Blender to a Flask server.

Interact via a PySide UI.

🛠 Tech Stack

Backend: Flask + SQLite

Frontend: PySide6 (Qt for Python)

3D Integration: Blender (Python API)

Database: SQLite

🔧 Installation

1️⃣ Clone the Repository

git clone https://github.com/your-username/inventory-management.git
cd inventory-management

2️⃣ Install Dependencies

pip install flask requests PySide6

🚀 Usage

1️⃣ Initialize Database

Run this once to create the inventory database:

python db.py

2️⃣ Start Flask Server

python app.py

Server runs at http://127.0.0.1:5000/

3️⃣ Run PySide UI

python pyside.py

4️⃣ Load Blender Plugin

Open Blender

Run transform_sync.py 2.blend inside Blender's Scripting panel

📌 API Endpoints

Method

Endpoint

Description

GET

/inventory

Fetch all inventory items

POST

/update-quantity

Update item quantity

POST

/add-item

Add a new item

POST

/remove-item

Remove an item

🛠 Troubleshooting

❌ Failed: { "error": "Item not found" }

Ensure the item exists in the database.

Run db.py to reset inventory.

❌ 404 Not Found

Check if Flask server is running (python app.py).

📜 License

MIT License

🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

📩 Contact

Author: Monesh

Email: Monesh18nov@gmail.com

