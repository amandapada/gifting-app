import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('giftcurator.ui')
        self.Results_ui = uic.loadUi('main.ui')
        self.ui.pushButton.clicked.connect(self.select_gift)
        self.Results_ui.backButton.clicked.connect(self.back_to_main_window)
        self.initUI()

    def initUI(self):
        # Add a placeholder item to the interestsComboBox
        self.ui.interestsComboBox.addItem("Select an interest...")

        # Add items with icons to the interestsComboBox
        self.ui.interestsComboBox.addItem(QIcon("C:/Users/USER/Desktop/Gifting App/akatsuki.png"), "Anime")
        self.ui.interestsComboBox.addItem(QIcon("C:/Users/USER/Desktop/Gifting App/dumbbell.png"), "Sports")
        self.ui.interestsComboBox.addItem(QIcon("C:/Users/USER/Desktop/Gifting App/Sunglasses.png"), "Fashion")

        # Connect the currentTextChanged signal to the onInterestsChanged slot
        self.ui.interestsComboBox.currentTextChanged.connect(self.onInterestsChanged)

        # Add a placeholder item to the genderComboBox
        self.ui.genderComboBox.addItem("Select a Gender...")

        # Add items to the genderComboBox
        self.ui.genderComboBox.addItem("Male")
        self.ui.genderComboBox.addItem("Female")

        # Connect the currentTextChanged signal to the onGenderChanged slot
        self.ui.genderComboBox.currentTextChanged.connect(self.onGenderChanged)

        self.ui.budgetBox.setPlaceholderText("Enter Your Budget")

        self.ui.show()

    def select_gift(self):
        interest = self.ui.interestsComboBox.currentText()
        gender = self.ui.genderComboBox.currentText()
        budget = float(self.ui.budgetBox.text())

        if interest == "Select an interest..." or gender == "Select a Gender...":
            print("Please select valid options.")
            return

        # Connect to the SQLite database
        conn = sqlite3.connect('gifts.db')
        cursor = conn.cursor()

        # Prepare the SQL query
        query = f"""
        SELECT name, price 
        FROM gifts 
        WHERE interest = ? AND gender = ?
        """

        # Prepare the parameters for the query
        params = (interest, gender)

        # Execute the query with the correct number of parameters
        cursor.execute(query, params)

        gifts = cursor.fetchall()

        # Filter gifts based on budget and ensure a 0.25% profit margin
        selected_gifts = []
        total_cost = 0
        for gift in gifts:
            name, price = gift
            if total_cost + price <= budget / 1.0025:
                selected_gifts.append(name)
                total_cost += price
        print(selected_gifts)
        # Update the listWidget with the selected gifts
        self.Results_ui.listWidget.clear()
        self.Results_ui.listWidget.addItems(selected_gifts)

        conn.close()

        # Open the results window after the selection process
        self.open_result_window()

    def open_result_window(self):
        self.ui.hide()
        self.Results_ui.show()

    def back_to_main_window(self):
        self.Results_ui.hide()
        self.ui.show()

    @pyqtSlot(str)
    def onInterestsChanged(self, text):
        if text != "Select an interest...":
            print("Selected interest:", text)

    @pyqtSlot(str)
    def onGenderChanged(self, text):
        if text != "Select a Gender...":
            print("Selected gender:", text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
