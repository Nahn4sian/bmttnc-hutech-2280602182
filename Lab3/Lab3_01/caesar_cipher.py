import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui.caesar_ui import Ui_MainWindow 
import requests

# Cấu hình đường dẫn đến thư mục platforms
# Ensure this path is correct for your system
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "C:/Users/Administrator/AppData/Local/Programs/Python/Python312/Lib/site-packages/PyQt5/Qt5/plugins/platforms"

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow() # Use the corrected class name here as well
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        # NOTE: Your Flask app is configured for RSA/ECC, not Caesar.
        # This URL will likely return a 404 unless you add Caesar endpoints to your Flask app.
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            # It's better to convert key to integer if it's for Caesar cipher shift
            "key": self.ui.txt_key.text() 
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data.get("encrypted_message", "Error: No encrypted message in response"))
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                # Handle non-200 responses for better error reporting
                error_msg = f"API Error: {response.status_code} - {response.text}"
                QMessageBox.warning(self, "API Error", error_msg)
                print(error_msg)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Network Error", f"Could not connect to the API: {e}")
            print(f"Error while calling API: {e}")

    def call_api_decrypt(self):
        # NOTE: Your Flask app is configured for RSA/ECC, not Caesar.
        # This URL will likely return a 404 unless you add Caesar endpoints to your Flask app.
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            # It's better to convert key to integer if it's for Caesar cipher shift
            "key": self.ui.txt_key.text()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data.get("decrypted_message", "Error: No decrypted message in response"))
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                # Handle non-200 responses for better error reporting
                error_msg = f"API Error: {response.status_code} - {response.text}"
                QMessageBox.warning(self, "API Error", error_msg)
                print(error_msg)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Network Error", f"Could not connect to the API: {e}")
            print(f"Error while calling API: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())