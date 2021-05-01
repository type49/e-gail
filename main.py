# -*- coding: utf-8 -*-
import configparser
import random
import re
import sys
from threading import Thread
import keyboard
import easygui as eg


from drag_and_drop_processing import drop_event
from text_processing import input_text

from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QEventLoop, QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QSystemTrayIcon, QAction, QMenu
from queenui import Ui_MainWindow

config = configparser.ConfigParser()
config.read(r'data\settings.ini')


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
        self.ui.queenBrowser.setText(random.choice(input_text('data/answers/start.txt')))
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
        hellows = ''.join(input_text(r'data/answers/hello.txt')).lower()
        print(answer)
        if answer[0] in hellows and len(answer) < 20:
            self.ui.queenBrowser.setText(random.choice(input_text('data/answers/hello.txt')) +
            random.choice(['', '!', ' ^-^', ' :з', ' (¬‿¬)', ' (✿◠‿◠)', ' (*・ω・)ﾉ ', '. Наверное.', ' <3']))
        if 'вопрос' in answer:
            self.ui.queenBrowser.setText(random.choice(input_text('data/answers/asking_start.txt')))
            self.asking_42()
        if ''.join(answer) == 'help':
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
            self.ui.queenBrowser.setText(random.choice(input_text('data/answers/ball42.txt')))
            if ask == 'хватит':
                self.ui.queenBrowser.setText(random.choice(input_text('data/answers/start.txt')))
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
        self.ui.queenBrowser.setText(random.choice(input_text('data/answers/exitApp.txt')))

        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)
        loop.exec()

        sys.exit()

    def tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(r'data\images\main_icon.png'))
        self.tray_icon.show()
        tray_exit_action = QAction("Выход", self)
        tray_exit_action.triggered.connect(QtWidgets.QApplication.quit)

        tray_menu = QMenu()
        tray_menu.setStyleSheet('''
                            font: 10pt "Montserrat Alternates";
                            background-color: #3a3d3e;
                            color: #efe2cd;
                            border: 1px solid #f09ea3;
                                ''')
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
