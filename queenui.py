from PyQt5 import QtCore, QtWidgets
import configparser

config = configparser.ConfigParser()
config.read(r'data\settings.ini')
backgroundImage = config.get("Theme", "theme")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('Эгель UI')
        MainWindow.setMinimumSize(QtCore.QSize(424, 424))
        MainWindow.setMaximumSize(QtCore.QSize(424, 424))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')

        self.textBrowser = QtWidgets.QLineEdit(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(170, 383, 251, 41))
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setObjectName('textBrowser')

        self.queenBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.queenBrowser.setGeometry(QtCore.QRect(200, 190, 222, 71))
        self.queenBrowser.setReadOnly(True)
        self.queenBrowser.setObjectName('queenBrowser')

        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.resize(424, 433)

        if backgroundImage == 'pink':
            self.background.setStyleSheet("image: url(data/images/pink.png);")
            self.textBrowser.setStyleSheet('''
                                    font: 10pt "Montserrat Alternates";
                                    background-color: #414547;
                                    color: #efe2cd;
                                    padding: 5;
                                    border: 1px solid #f09ea3;
                                    border-radius: 10px;
                                        ''')
            self.queenBrowser.setStyleSheet('''
                                    font: 10pt "Montserrat Alternates";
                                    background-color: #414547;
                                    color: #efe2cd;
                                    padding: 5;
                                    border: 1px solid #f09ea3;
                                    border-radius: 10px;
                                        ''')
            self.textBrowser.setGeometry(10, 390, 410, 33)
            self.queenBrowser.setGeometry(160, 300, 250, 60)

        elif backgroundImage == 'blue':
            self.background.setStyleSheet("image: url(data/images/blue.png);")
            self.textBrowser.setStyleSheet('''
                                                font: 10pt "Montserrat Alternates";
                                                background-color: #414547;
                                                color: #efe2cd;
                                                padding: 5;
                                                border: 1px solid #3f81a1;
                                                border-radius: 10px;
                                                    ''')
            self.queenBrowser.setStyleSheet('''
                                                font: 10pt "Montserrat Alternates";
                                                background-color: #414547;
                                                color: #efe2cd;
                                                padding: 5;
                                                border: 1px solid #3f81a1;
                                                border-radius: 10px;
                                                    ''')
            self.textBrowser.setGeometry(100, 390, 310, 33)
            self.queenBrowser.setGeometry(160, 320, 250, 60)


        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




