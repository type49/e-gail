# -*- coding: utf-8 -*-
import configparser

from PIL import Image
import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea
import webbrowser
import clipboard
import json

config = configparser.ConfigParser()
config.read(r'data\settings.ini')
app_theme = config.get("Theme", "theme")
if app_theme == 'pink':
    app_theme = 'data/data_pink.qss'
if app_theme == 'blue':
    app_theme = 'data/data_blue.qss'


def html_open(url):
    webbrowser.open_new_tab(url)


def clipboard_copy(text):
    clipboard.copy(text)


class DataManagerWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.window_width = 450
        self.window_height = 730
        self.setObjectName('main_window')

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        with open(r'data\data\saved_data.json', encoding='utf-8') as data_file:
            self.data_text = json.load(data_file)

        self.vbox = QVBoxLayout(self)
        self.vbox.addStretch(1)
        self.vbox.setSpacing(15)

        self.button = QPushButton('restart')
        self.button.clicked.connect(self.reverse_data_foo)

        self.exit_button = QPushButton("х")
        self.exit_button.setObjectName('exit_button')
        self.exit_button.clicked.connect(self.close_app)

        self.reverse_button = QPushButton("↓↓")
        self.reverse_button.setObjectName('reverse_button')
        self.reverse_button.clicked.connect(self.reverse_data_foo)

        self.hide_button = QPushButton("-")
        self.hide_button.setObjectName('hide_button')
        self.hide_button.clicked.connect(self.showMinimized)

        self.vbox.addWidget(self.page_init())
        self.show()

    def page_init(self):
        page_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout(page_widget)
        self.main_box = QVBoxLayout()
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.area = QWidget()
        self.labels_box = QVBoxLayout()

        for data_line in self.data_text:
            if 'text_item' in data_line:
                data_item = data_line['text_item'][0]['content']
                data_time = data_line['text_item'][0]['time']

                text_label = QLabel(self)
                text_label.setWordWrap(True)
                text_label.adjustSize()
                text_label.setOpenExternalLinks(True)
                text_label.setContextMenuPolicy(Qt.ActionsContextMenu)
                text_label.setFixedWidth(self.window_width - 30)
                text_label.setObjectName('text_label')
                text_label.setText(f'''
                                    <p>{data_item}&nbsp;</p>
                                    <p style="text-align: right; font-size: 10px; color: #95a68b">{data_time}</p>
                                    ''')

                copy_action = QAction('Копировать текст', self)
                copy_action.triggered.connect(lambda ch, text=data_item: clipboard_copy(text))
                delete_text_action = QAction('Удалить текст', self)
                delete_text_action.triggered.connect(
                    lambda ch, x_data_line=data_line: self.delete_data_foo(x_data_line, None))

                text_label.addAction(copy_action)
                text_label.addAction(QAction('---', self))
                text_label.addAction(delete_text_action)
                text_label.addAction(QAction('---', self))

                self.labels_box.addWidget(text_label)

            if 'url_item' in data_line:
                data_item = data_line['url_item'][0]['content']
                data_time = data_line['url_item'][0]['time']

                html_label = QLabel('')
                html_label.setOpenExternalLinks(True)
                html_label.setWordWrap(True)
                html_label.setFixedWidth(self.window_width - 30)
                html_label.setObjectName('html_label')
                html_label.setText(f'''
                                    <p>{data_item}</p>
                                    <p style="text-align: right; font-size: 10px; color: #95a68b">{data_time}</p>
                                    ''')

                html_label.setContextMenuPolicy(Qt.ActionsContextMenu)
                html_open_action = QAction('Перейти по ссылке', self)
                html_open_action.triggered.connect(lambda ch, url=data_item: html_open(url))
                html_copy_action = QAction('Скопировать ссылку', self)
                html_copy_action.triggered.connect(lambda ch, text=data_item: clipboard_copy(text))
                delete_html_action = QAction('Удалить ссылку', self)
                delete_html_action.triggered.connect(
                    lambda ch, item=data_line: self.delete_data_foo(item, None))

                html_label.addAction(html_open_action)
                html_label.addAction(html_copy_action)
                html_label.addAction(QAction('---', self))
                html_label.addAction(delete_html_action)
                html_label.addAction(QAction('---', self))

                self.labels_box.addWidget(html_label)

            if 'image_item' in data_line:
                data_item = data_line['image_item'][0]['content']
                data_time = data_line['image_item'][0]['time']

                if os.path.exists(data_item):
                    image_label = QLabel()
                    image_label.setContextMenuPolicy(Qt.ActionsContextMenu)
                    image_label.setFixedWidth(self.window_width - 30)
                    image_label.setObjectName('image_label')
                    image_label.setText(f'''
                                        <p><img src="{data_item}" alt="" width="{self.window_width - 60}" /></p>
                                        <p style="text-align: right; font-size: 10px; color: #95a68b">{data_time}</p>
                                        ''')
                    delete_image_action = QAction('Удалить изображение.', self)
                    delete_image_action.triggered.connect(
                        lambda ch, x_data_line=data_line: self.delete_data_foo(x_data_line, None))
                    image_label.addAction(delete_image_action)
                    self.labels_box.addWidget(image_label)

                else:
                    self.delete_data_foo(data_line, 'x_flag')

            if 'gif_item' in data_line:
                data_item = data_line['gif_item'][0]['content']
                data_time = data_line['gif_item'][0]['time']

                gif_label = QLabel()
                gif_label.setContextMenuPolicy(Qt.ActionsContextMenu)
                gif_label.setFixedWidth(self.window_width - 30)
                gif_label.setObjectName('gif_label')

                if os.path.exists(data_item):
                    self.gif_item = QMovie(data_item)
                    gif_label.setMovie(self.gif_item)

                    im = Image.open(data_item)
                    w, h = im.size
                    w2, h2 = self.window_width - 50, self.window_height

                    if int(w2 / h2 * 100) < int(w / h * 100):
                        w_new = w2
                        h_new = int(w2 * h / w)
                        self.gif_item.setScaledSize(QtCore.QSize(w_new, h_new))
                        self.gif_item.start()
                        self.gif_item.stop()
                        self.labels_box.addWidget(gif_label)
                    else:
                        h_new = h2
                        w_new = int(h2 * w / h)
                        self.gif_item.setScaledSize(QtCore.QSize(w_new, h_new))
                        self.gif_item.start()
                        self.gif_item.stop()
                        self.labels_box.addWidget(gif_label)

                    gif_start_action = QAction('Запустить', self)
                    gif_start_action.triggered.connect(self.gif_item.start)
                    gif_label.addAction(gif_start_action)
                    gif_stop_action = QAction('Остановить', self)
                    gif_stop_action.triggered.connect(self.gif_item.stop)
                    gif_label.addAction(gif_stop_action)
                else:
                    self.delete_data_foo(data_line, 'x_flag')

        self.button_box = QHBoxLayout()
        self.button_box.addWidget(self.reverse_button)
        self.button_box.addWidget(self.hide_button)
        self.button_box.addWidget(self.exit_button)

        self.main_box.addLayout(self.button_box)

        self.area.setLayout(self.labels_box)

        self.scrollarea.setWidget(self.area)

        if self.scrollarea.viewportSizeHint().height() < self.window_height:
            self.scrollarea.setFixedHeight(self.scrollarea.viewportSizeHint().height())
        else:
            self.scrollarea.setFixedHeight(self.window_height)
        self.scrollarea.setObjectName('scrollarea')
        self.scrollarea.setFixedWidth(self.window_width + 10)
        self.main_box.addWidget(self.scrollarea)
        self.main_layout.addLayout(self.main_box)
        return page_widget

    def delete_data_foo(self, x_data_line, x_flag):
        if 'image_item' in x_data_line:
            try:
                os.remove(x_data_line['image_item'][0]['content'])
            except:
                print(f'Не получилось удалить изображение')

        new_data = []

        for i in self.data_text:
            if i != x_data_line:
                new_data.append(i)

        self.write_data_to_json(new_data)

        if not x_flag:
            self.update_page_foo()

    def write_data_to_json(self, data_line):
        with open(r'data\data\saved_data.json', 'w', encoding='utf-8') as data_file:
            json.dump(data_line, data_file, indent=2, ensure_ascii=False)
        self.data_text = data_line

    def reverse_data_foo(self):
        a = self.data_text
        a.reverse()
        self.write_data_to_json(a)
        self.update_page_foo()

    def update_page_foo(self):
        widget = self.vbox.takeAt(1).widget()
        widget.hide()
        w = self.page_init()
        self.vbox.insertWidget(1, w)
        w.show()

    def close_app(self):
        self.hide()


def move_right_bottom_corner(win):
    screen_geometry = QApplication.desktop().availableGeometry()
    screen_size = (screen_geometry.width(), screen_geometry.height())
    win_size = (win.frameSize().width(), win.frameSize().height())
    x = screen_size[0] - win_size[0]
    y = screen_size[1] - win_size[1]
    win.move(x, y)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    file = QtCore.QFile(app_theme)
    file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())
    w = DataManagerWindow()
    move_right_bottom_corner(w)
    w.show()
    sys.exit(app.exec_())
