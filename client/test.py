from PyQt4 import QtCore, QtGui

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction('Action')
        widget = QtGui.QWidget(self)
        layout = QtGui.QVBoxLayout(widget)
        self.canvas = Canvas(widget)
        layout.addWidget(self.canvas)
        self.setCentralWidget(widget)

class Canvas(QtGui.QGraphicsView):
    def __init__(self, parent):
        super(Canvas, self).__init__(parent)
        self.widget = QtGui.QComboBox(self)

    def resizeEvent(self, event):
        self.widget.move(self.width() - self.widget.width() - 2, self.height() - self.widget.height() - 2)
        super(Canvas, self).resizeEvent(event)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    window.setGeometry(500, 300, 200, 200)
    sys.exit(app.exec_())
