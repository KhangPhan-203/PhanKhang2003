import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QColor

class RGBController(QtWidgets.QWidget):
    def __init__(self):
        super(RGBController, self).__init__()
        uic.loadUi('Lab9.ui', self)

        # Connect the sliders and spinboxes
        self.verticalSlider.valueChanged.connect(self.update_color)
        self.spinBox.valueChanged.connect(self.verticalSlider.setValue)
        self.verticalSlider_2.valueChanged.connect(self.update_color)
        self.spinBox_2.valueChanged.connect(self.verticalSlider_2.setValue)
        self.verticalSlider_3.valueChanged.connect(self.update_color)
        self.spinBox_3.valueChanged.connect(self.verticalSlider_3.setValue)

        self.spinBox.valueChanged.connect(self.update_color)
        self.spinBox_2.valueChanged.connect(self.update_color)
        self.spinBox_3.valueChanged.connect(self.update_color)

        # Initialize the background color
        self.update_color()

    def update_color(self):
        red = self.verticalSlider.value()
        green = self.verticalSlider_2.value()
        blue = self.verticalSlider_3.value()
        color = QColor(red, green, blue)

        # Create a QPalette object
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)

        # Apply the palette to the widget
        self.setPalette(palette)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = RGBController()
    window.show()
    sys.exit(app.exec_())
