import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

def set_main_window():
    window = QWidget()
    window.setWindowTitle('PyQt5 App')
    window.setGeometry(0, 0, 800, 400)
    window.move(0, 0)
    helloMsg = QLabel('<h1>Hello World!</h1>', parent=window)
    helloMsg.move(60, 15)
    return window

def main():
    app = QApplication(sys.argv)
    window = set_main_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
