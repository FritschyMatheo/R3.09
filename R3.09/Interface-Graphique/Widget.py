import sys
from PyQt6.QtWidgets import *
widgets = [
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLCDNumber,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit
]

app = QApplication(sys.argv)
root = QWidget()
grid = QHBoxLayout()
toolbar = QToolBar("My main toolbar")
for w in widgets:
    grid.addWidget(w())
root.setLayout(grid)
root.setWindowTitle("Hello world!")
root.show()
if __name__ == '__main__':
    sys.exit(app.exec())