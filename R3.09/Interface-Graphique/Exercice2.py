import sys
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Conversion de Température")

        labeltemp = QLabel("Température")
        self.label1 = QLabel("°C")
        self.data = QLineEdit("")
        convert = QPushButton("Convertir")
        self.choix =  QComboBox()
        self.choix.addItems(["°C -> K", "K -> °C"])
        labelConversion = QLabel("Conversion")
        self.resultat = QLineEdit("")
        self.resultat.setEnabled(False)
        self.label2 = QLabel("K")
        aide = QPushButton("?")

        # Ajouter les composants au grid ayout
        grid.addWidget(labeltemp, 0, 0)
        grid.addWidget(self.data, 0, 1)
        grid.addWidget(self.label1, 0, 2)
        grid.addWidget(convert, 1, 1)
        grid.addWidget(self.choix, 1, 2)
        grid.addWidget(labelConversion, 2, 0)
        grid.addWidget(self.resultat, 2, 1)
        grid.addWidget(self.label2, 2, 2)
        grid.addWidget(aide, 3, 4)

        convert.clicked.connect(self.__actionConvert)
        aide.clicked.connect(self.__actionAide)
        self.choix.currentIndexChanged.connect(self.__changementUnite)
        
    def __actionConvert(self):
        try:
            data = float(self.data.text())
            if self.choix.currentText() == "°C -> K":
                if data < -273.15:
                    raise ValueError("La température est trop basse")
                else:
                    resultat = data + 273.15
            else:
                if data < 0:
                    raise ValueError("La température est trop basse")
                else:
                    resultat = data - 273.15
            
            self.resultat.setText(f"{resultat:.2f}")
        

        except ValueError as e:
            if "could nopt convert string to float" in str(e):
                QMessageBox.warning(self, "Erreur", "Veuillez entrer une nouvelle valeure valide !")
            else:
                QMessageBox.warning(self, "Erreur", str(e))
    
    def __changementUnite(self):
        if self.choix.currentText() == "°C -> K":
            self.label1.setText("°C")
            self.label2.setText("K")
        else:
            self.label1.setText("K")
            self.label2.setText("°C")

    def __actionAide(self):
        QMessageBox.information(self, "Aide", "Permet de convertir un nombre soit de Kelvin vers Celcius, soit de Celcius vers Kelvin")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(350,225)
    window.show()
    app.exec()