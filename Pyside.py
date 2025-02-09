import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog

API_URL = "http://127.0.0.1:5000"

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Item Name", "Quantity"])
        self.layout.addWidget(self.table)

        self.refresh_button = QPushButton("Refresh Inventory")
        self.refresh_button.clicked.connect(self.refresh_inventory)
        self.layout.addWidget(self.refresh_button)

        self.buy_button = QPushButton("Buy Item")
        self.buy_button.clicked.connect(self.buy_item)
        self.layout.addWidget(self.buy_button)

        self.return_button = QPushButton("Return Item")
        self.return_button.clicked.connect(self.return_item)
        self.layout.addWidget(self.return_button)

        self.add_button = QPushButton("Add New Item")
        self.add_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Item")
        self.remove_button.clicked.connect(self.remove_item)
        self.layout.addWidget(self.remove_button)

        self.setLayout(self.layout)
        self.refresh_inventory()

    def refresh_inventory(self):
        try:
            response = requests.get(f"{API_URL}/inventory")
            data = response.json()["inventory"]
            self.table.setRowCount(len(data))
            
            for row, item in enumerate(data):
                self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
                self.table.setItem(row, 1, QTableWidgetItem(str(item["quantity"])))

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Error", "Cannot connect to server.")

    def buy_item(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Select Item", "Please select an item to buy.")
            return

        item_name = self.table.item(row, 0).text()
        quantity, ok = QInputDialog.getInt(self, "Buy Item", f"Enter quantity to buy for {item_name}:", 1, 1, 100)

        if ok:
            try:
                response = requests.post(f"{API_URL}/update-quantity", json={"name": item_name, "quantity": -quantity})
                if response.status_code == 200:
                    QMessageBox.information(self, "Success", f"Bought {quantity} of {item_name}.")
                    self.refresh_inventory()
                else:
                    QMessageBox.warning(self, "Error", response.json().get("error", "Failed to buy item."))
            except requests.exceptions.ConnectionError:
                QMessageBox.critical(self, "Server Error", "Cannot connect to the Flask server.")

    def return_item(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Select Item", "Please select an item to return.")
            return

        item_name = self.table.item(row, 0).text()
        quantity, ok = QInputDialog.getInt(self, "Return Item", f"Enter quantity to return for {item_name}:", 1, 1, 100)

        if ok:
            try:
                response = requests.post(f"{API_URL}/update-quantity", json={"name": item_name, "quantity": quantity})
                if response.status_code == 200:
                    QMessageBox.information(self, "Success", f"Returned {quantity} of {item_name}.")
                    self.refresh_inventory()
                else:
                    QMessageBox.warning(self, "Error", response.json().get("error", "Failed to return item."))
            except requests.exceptions.ConnectionError:
                QMessageBox.critical(self, "Server Error", "Cannot connect to the Flask server.")

    def add_item(self):
        name, ok = QInputDialog.getText(self, "Add Item", "Enter item name:")
        if not ok or not name:
            return

        quantity, ok = QInputDialog.getInt(self, "Add Item", "Enter quantity:", 1, 1, 1000)
        if ok:
            try:
                response = requests.post(f"{API_URL}/add-item", json={"name": name, "quantity": quantity})
                if response.status_code == 200:
                    QMessageBox.information(self, "Success", f"Added {name} with quantity {quantity}.")
                    self.refresh_inventory()
                else:
                    QMessageBox.warning(self, "Error", response.json().get("error", "Failed to add item."))
            except requests.exceptions.ConnectionError:
                QMessageBox.critical(self, "Server Error", "Cannot connect to the Flask server.")

    def remove_item(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Select Item", "Please select an item to remove.")
            return

        item_name = self.table.item(row, 0).text()
        confirm = QMessageBox.question(self, "Remove Item", f"Are you sure you want to remove {item_name}?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            try:
                response = requests.post(f"{API_URL}/remove-item", json={"name": item_name})
                if response.status_code == 200:
                    QMessageBox.information(self, "Success", f"Removed {item_name}.")
                    self.refresh_inventory()
                else:
                    QMessageBox.warning(self, "Error", response.json().get("error", "Failed to remove item."))
            except requests.exceptions.ConnectionError:
                QMessageBox.critical(self, "Server Error", "Cannot connect to the Flask server.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
