# -*- coding: utf-8 -*-
import configparser
import random
import re
import sys
from threading import Thread
import keyboard
import easygui as eg

from drag_and_drop_processing import drop_event
import text_processing as tp

from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QEventLoop, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QSystemTrayIcon, QAction, QMenu
from queenui import Ui_MainWindow
from settingsui import Ui_SettingsWindow

config = configparser.ConfigParser()
config.read(r'data\settings.ini')


class SettingsWin(QtWidgets.QMainWindow, QWidget):

    def __init__(self):
        with open(r'data\settings.ini', 'r') as config_file:
            self.old_config = config_file.read()
        QtWidgets.QWidget.__init__(self, parent=None)

        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.8)
        self.show()
        self.ui.saveButton.clicked.connect(self.save_button)
        self.ui.cancelButton.clicked.connect(self.cancel_button)

        self.ui.themeComboBox.setCurrentText(config.get("Theme", "background"))
        self.ui.themeComboBox.activated.connect(self.set_theme_cb)
        self.ui.themeComboBox.activated.connect(self.set_theme_cb)
        self._old_pos = None

    on_theme_changed = pyqtSignal(str)

    def set_theme_cb(self):
        background_image = config.get("Theme", "background")
        self.on_theme_changed.emit(background_image)
        a = self.ui.themeComboBox.currentIndex()
        if a == 0:
            config.set("Theme", "background", "blue")
            with open(r'data\settings.ini', "w") as config_file:
                config.write(config_file)
        elif a == 1:
            config.set("Theme", "background", "pink")
            with open(r'data\settings.ini', "w") as config_file:
                config.write(config_file)

    def save_button(self):
        with open(r'data\settings.ini', "w") as config_file:
            config.write(config_file)
        self.close()

    def cancel_button(self):
        with open(r'data\settings.ini', 'w') as config_file:
            config_file.write(self.old_config)
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return
        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)


class MyWin(QtWidgets.QMainWindow, QWidget):
    keySwitcher = 0

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self._old_pos = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.ui.queenBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.ui.queenBrowser.setText(random.choice(tp.start_messages))
        self.tray_icon()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return and len(self.ui.textBrowser.text()) > 2:
            if self.keySwitcher == 0:
                self.start_dialogue()
            if self.keySwitcher == 1:
                self.asking_42()

    def start_dialogue(self):
        answer = re.split('[-.?!)(,: ]', self.ui.textBrowser.text().lower())
        self.ui.textBrowser.clear()
        print(answer)
        if answer[0] in tp.hellows and len(answer) < 20:
            self.ui.queenBrowser.setText(random.choice(tp.hellows) +
            random.choice(['', '!', ' ^-^', ' :з', ' (¬‿¬)', ' (✿◠‿◠)', ' (*・ω・)ﾉ ', '. Наверное.', ' <3']))
        elif 'вопрос' in answer:
            self.ui.queenBrowser.setText(random.choice(tp.start_ask))
            self.asking_42()
        elif ''.join(answer) == 'help':
            eg.msgbox('''
            Я - Эгель. Милый асистент в просирании времени в интернете. 
            Можешь поздороваться. Да. Можешь задать любой вопрос. Только сначала скажи - хочу, мол, 
            вопрос задать, или "у меня вопрос". В общем вот. Так же можешь кидать в меня текстом,
            картинками, ссылками. Всё это добро я сохраню. В последующих версиях мне ещё и обещали 
            добавить удобный менеджер для этого. 
            Можешь скрыть меня кнопкой 'Pause', и так же "раскрыть". Выключить меня можно из контекстного меню в трее. 
            ''')
        else:
            self.ui.queenBrowser.setText('''Увы, не поняла. Можешь воспользоваться командой help
            ''')

    def asking_42(self):
        self.keySwitcher = 1
        ask = self.ui.textBrowser.text().lower()
        self.ui.textBrowser.clear()
        if ask:
            self.ui.queenBrowser.setText(random.choice(tp.ball42))
            if ask == 'хватит':
                self.ui.queenBrowser.setText(random.choice(tp.start_messages))
                self.keySwitcher = 0

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            mime = str(event.mimeData().text())
            print(f'{mime} is dropped')
            Thread(target=drop_event, args=(mime, )).start()

    def close_app_foo(self):
        self.ui.textBrowser.clear()
        sys.exit()

    def tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(r'data\images\main_icon.png'))
        self.tray_icon.show()
        tray_exit_action = QAction("Выход", self)
        tray_exit_action.triggered.connect(QtWidgets.QApplication.quit)
        tray_settings_action = QAction("Настройки", self)
        tray_settings_action.triggered.connect(self.settings_foo)

        tray_menu = QMenu()
        tray_menu.setStyleSheet('''
                            font: 10pt "Montserrat Alternates";
                            background-color: #3a3d3e;
                            color: #efe2cd;
                            border: 1px solid #f09ea3;
                                ''')
        tray_menu.addAction(tray_settings_action)
        tray_menu.addAction(tray_exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return
        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def settings_foo(self):
        self.sw = SettingsWin()
        self.sw.show()
        self.sw.on_theme_changed.connect(self.set_theme_foo)


    @pyqtSlot(str)
    def set_theme_foo(self, backgroundImage):
        """
        Change theme from settings.
        """
        if backgroundImage == 'blue':
            self.ui.background.setStyleSheet("image: url(data/images/blue.png);")
            self.ui.textBrowser.setStyleSheet('''
                                                            font: 10pt "Montserrat Alternates";
                                                            background-color: #414547;
                                                            color: #efe2cd;
                                                            padding: 5;
                                                            border: 1px solid #3f81a1;
                                                            border-radius: 10px;
                                                                ''')
            self.ui.queenBrowser.setStyleSheet('''
                                                            font: 10pt "Montserrat Alternates";
                                                            background-color: #414547;
                                                            color: #efe2cd;
                                                            padding: 5;
                                                            border: 1px solid #3f81a1;
                                                            border-radius: 10px;
                                                                ''')
            self.ui.textBrowser.setGeometry(100, 390, 310, 33)
            self.ui.queenBrowser.setGeometry(160, 320, 250, 60)
        if backgroundImage == 'pink':
            self.ui.background.setStyleSheet("image: url(data/images/pink.png);")
            self.ui.textBrowser.setStyleSheet('''
                                                font: 10pt "Montserrat Alternates";
                                                background-color: #414547;
                                                color: #efe2cd;
                                                padding: 5;
                                                border: 1px solid #f09ea3;
                                                border-radius: 10px;
                                                    ''')
            self.ui.queenBrowser.setStyleSheet('''
                                                font: 10pt "Montserrat Alternates";
                                                background-color: #414547;
                                                color: #efe2cd;
                                                padding: 5;
                                                border: 1px solid #f09ea3;
                                                border-radius: 10px;
                                                    ''')
            self.ui.textBrowser.setGeometry(10, 390, 410, 33)
            self.ui.queenBrowser.setGeometry(160, 300, 250, 60)


class InactiveHotKey(Thread):
    def key_listener(key):
        if key.name == 'pause' and key.event_type == 'down':
            if w.windowOpacity() == 1:
                __var = 1
                while w.windowOpacity() > 0:
                    w.setWindowOpacity(__var)
                    __var -= 0.2
                    loop = QEventLoop()
                    QTimer.singleShot(30, loop.quit)
                    loop.exec()
            else:
                __va = 0
                while w.windowOpacity() < 1:
                    w.setWindowOpacity(__va)
                    __va += 0.2
                    loop = QEventLoop()
                    QTimer.singleShot(30, loop.quit)
                    loop.exec()
    keyboard.hook(key_listener)


def move_right_bottom_corner(win):
    screen_geometry = QApplication.desktop().availableGeometry()
    screen_size = (screen_geometry.width(), screen_geometry.height())
    win_size = (win.frameSize().width(), win.frameSize().height())
    x = screen_size[0] - win_size[0]
    y = screen_size[1] - win_size[1]
    win.move(x, y)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWin()
    move_right_bottom_corner(w)
    w.show()
    sys.exit(app.exec_())
