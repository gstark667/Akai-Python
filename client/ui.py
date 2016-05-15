import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QApplication
from PyQt5.QtGui import QFont

class UI():
   def __init__(self):
      self.app = QApplication(sys.argv)
      self.main_window = MainWindow()
      sys.exit(self.app.exec_())

class MainWindow(QWidget):
   def __init__(self):
      super().__init__()
      self.initUI()

   def initUI(self):
      QToolTip.setFont(QFont('SansSerif', 10))
      self.setToolTip('This is a <b>QWidget</b> widget')
      btn = QPushButton('Button', self)
      btn.setToolTip('This is a <b>QPushButton</b> widget')
      btn.resize(btn.sizeHint())
      btn.move(50, 50)       
      self.setGeometry(300, 300, 300, 200)
      self.setWindowTitle('Tooltips')    
      self.show()

class MainSplit(QSplitter):
   def __init__(self, parent):
      super().__init__(parent)

      btn = QPushButton("BUTTON")


UI()
sys.exit(app.exec_())
