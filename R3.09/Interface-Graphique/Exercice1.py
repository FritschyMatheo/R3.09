import sys
from PyQt6.QtWidgets import QApplication, QWidget
app = QApplication(sys.argv)
root = QWidget()
root.resize(250, 250)
root.setWindowTitle("Une première fenêtre")
root.show()
if __name__ == '__main__':
    sys.exit(app.exec())