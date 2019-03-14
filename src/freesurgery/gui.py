import sys
#from PyQt5.QtWidgets import QApplication, QWidget

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon

'''
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("FreeSurgery")
        MainWindow.resize(2000, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("FreeSurgery", "FreeSurgery"))

class AppWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(AppWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
'''

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

if __name__=='__main__':
    app()