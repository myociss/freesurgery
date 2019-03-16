import sys
#from PyQt5.QtWidgets import QApplication, QWidget
'''
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon


class AppWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        
        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.3)
        self.setWindowTitle('FreeSurgery')    
        self.show()

def app():
    
    app = QApplication([])
    application = AppWindow()
    application.show()
    sys.exit(app.exec())
'''
