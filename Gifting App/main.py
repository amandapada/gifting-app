import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit
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

        # Call the gift selection function
        recommended_gifts = self._select_gift(interest, gender, budget)

        # Clear the listWidget
        self.Results_ui.listWidget.clear()

        # Add the recommended gifts to the listWidget
        if recommended_gifts:
            print(recommended_gifts)
            for gift in recommended_gifts:
                item_text = f"{gift['name']} - {gift['description']} - ${gift['price']:.2f}"
                item = QListWidgetItem(item_text)
                self.Results_ui.listWidget.addItem(item)

        # Open the results window
        self.open_result_window()

    def open_result_window(self):
        self.ui.hide()
        self.Results_ui.show()

    def back_to_main_window(self):
        self.Results_ui.hide()
        self.ui.show()

    @pyqtSlot(str)
    def onInterestsChanged(self, text):
        if text != "Select an interest...":  # assuming "Select an interest..." is the placeholder text
            print("Selected interest:", text)

    @pyqtSlot(str)
    def onGenderChanged(self, text):
        if text != "Select a Gender...":  # assuming "Select a Gender..." is the placeholder text
            print("Selected gender:", text)

    def _select_gift(self, interest, gender, budget):
    
        print("Interest:", interest)
        print("Gender:", gender)
        print("Budget:", budget)
        # Establish a connection to the database
        db = sqlite3.connect('gifts.db')  # replace with your database file name
        cursor = db.cursor()

        # Filter by Interest
        cursor.execute("SELECT * FROM gifts WHERE interest = ?", (interest,))
        gifts = cursor.fetchall()
        print("Gifts:", gifts)
        
        # Filter by Gender
        gifts = [gift for gift in gifts if gift[2] == gender or gift[2] == 'Unisex']

        #the code isn't responding to this part
        # Filter by Budget
        min_price = budget * 0.5  # adjust the minimum price range based on the budget
        max_price = budget * 1.2 # adjust the maximum price range based on the budget
        gifts = [gift for gift in gifts if min_price <= gift[3] <= max_price]

        # Rank Gifts by Price
        gifts.sort(key=lambda x: x[3])

        # Select Gifts
        recommended_gifts = []
        for gift in gifts:
            recommended_gifts.append({'name': gift[0], 'description': gift[1], 'price': gift[3]})
        # Close the database connection
        db.close()
        return recommended_gifts

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())