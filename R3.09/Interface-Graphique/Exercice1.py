import sys
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Une première fenêtre")

        lab = QLabel("Saisir votre nom")
        self.text = QLineEdit("")
        self.retour = QLabel("")
        ok = QPushButton("Ok")
        quit = QPushButton("Quitter")

        # Ajouter les composants au grid ayout
        grid.addWidget(lab, 0, 0) 
        grid.addWidget(self.text, 1, 0)
        grid.addWidget(ok, 2, 0)
        grid.addWidget(self.retour, 3, 0)
        grid.addWidget(quit, 4, 0)

        ok.clicked.connect(self.__actionOk)
        quit.clicked.connect(self.__actionQuitter)

    def __actionOk(self):
        nom = self.text.text()
        if nom == "":
            self.retour.setText("Veuillez entrer un nom :)")
        else:
            self.retour.setText(f"Bonjour {nom} !")
    def __actionQuitter(self):
        QApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300,150)
    window.show()
    app.exec()