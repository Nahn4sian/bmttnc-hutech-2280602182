import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_MainWindow # Import Ui_MainWindow from ui.ecc

import requests
import os # Import os for environment variable setting

# Set QT_QPA_PLATFORM_PLUGIN_PATH environment variable
# This is often needed when deploying PyQt applications to ensure platform plugins are found
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "../platforms"

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow() # Create an instance of the UI from ui.ecc
        self.ui.setupUi(self) # Set up the UI on this QMainWindow instance

        # Connect button signals to their respective slot functions
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            response = requests.get(url) # Use GET for key generation as shown in the image
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"]) # Assuming the message is in "message" key
                msg.exec_()
            else:
                print("Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: %s" % response.text)
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("Error while calling API")
            print("Error: %s" % e.message)

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setText(data["signature"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: %s" % response.text)
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("Error while calling API")
            print("Error: %s" % e.message)

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Fail")
                    msg.exec_()
            else:
                print("Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: %s" % response.text)
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("Error while calling API")
            print("Error: %s" % e.message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())