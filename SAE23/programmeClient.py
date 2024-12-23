from Client import *
import sys
from PyQt6.QtWidgets import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        app.exec()
    except Exception as e:
        QMessageBox.critical(None, "Erreur", f"Erreur dans le programme client :\n{e}")