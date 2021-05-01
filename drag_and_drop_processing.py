import configparser
import datetime
import json
import os
import time
import requests
import urllib
from urllib import request
import re
import easygui as eg

config = configparser.ConfigParser()
config.read(r'data\settings.ini')


def network_connection_check(link):
    try:
        from requests.utils import requote_uri
        quote_link = requote_uri(link)
        urllib.request.urlopen(quote_link, timeout=10)
        return True
    except Exception as ex:
        print(ex)
        return False


url_regex = re.compile(
    r'^(?:(?:http|ftp)s?://)?'  # http:// or https:// or None
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)  # Check text for url

PNG_SIGNS = (b'\x89PNG\r\n\x1a\n',)  # PNG signature
JPG_SIGNS = (b'\xff\xd8\xff',)  # JPG signature
GIF_SIGNS = (b'GIF87a', b'GIF89a')  # GIF signature


def write_data_to_json(data_line):
    try:
        data = json.load(open(r'data\data\saved_data.json', encoding='utf-8'))
    except Exception as ex:
        print(ex)
        data = []
    data.append(data_line)
    with open(r'data\data\saved_data.json', 'w', encoding='utf-8') as data_file:
        json.dump(data, data_file, indent=2, ensure_ascii=False)
    print(list(data_line)[0] + ' is added to json')


def image_downloader(image_url, file_signature):
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    img_name = os.getcwd() + r'\\Downloads\\images\\' + current_time + file_signature
    load = open(img_name, "wb")
    try:
        img_link = requests.get(image_url)
        load.write(img_link.content)
        load.close()
    except:
        print('Download error')
        con_er_msg = '''
                    Это окно такое некрасивое потому что это окно ошибки.
                    Тут почему то проблема с загрузкой файла. 
                    В общем, можешь проверить интернет и нажать "Повторить" - если хочешь повторить.
                    Ну или "Отмена" - если не так уж и хотелось.
                    Цмок:*
                    '''
        con_er_cho = ['Повторить', 'Отмена']
        if eg.ccbox(con_er_msg, 'Сбой загрузки.', con_er_cho):
            image_downloader(image_url, file_signature)
        else:
            return

    print(f'Download {file_signature} is done')
    if file_signature == '.gif':
        current_time = datetime.datetime.today().strftime("%Y-%m-%d | %H.%M")
        data_line = {'gif_item': [{'content': img_name, 'time': current_time}]}
        write_data_to_json(data_line)
    else:
        current_time = datetime.datetime.today().strftime("%Y-%m-%d | %H.%M")
        data_line = {'image_item': [{'content': img_name, 'time': current_time}]}
        write_data_to_json(data_line)


def drop_event(drop_data):
    if re.match(url_regex, drop_data):
        if not drop_data.startswith('http'):
            drop_data = 'http://' + drop_data
        if network_connection_check(drop_data) is True:

            try:
                resp = requests.get(drop_data, timeout=3)
                mime_content = resp.content

            except:
                con_er_msg = '''
                            Это окно такое некрасивое потому что это окно ошибки.
                            Проблемы с соедиением.
                            Если подключен прокси - скорее всего проблема в нём. Пока не научил её работать с ним.
                            В общем, можешь проверить интернет и нажать "Повторить" - если хочешь повторить.
                            Ну или "Отмена" - если не так уж и хотелось.
                            Цмок:*
                            '''
                con_er_cho = ['Повторить', 'Отмена']
                if eg.ccbox(con_er_msg, 'Интрынет нет.', con_er_cho):
                    drop_event(drop_data)
                else:
                    return
            if mime_content.startswith(PNG_SIGNS) or mime_content.startswith(GIF_SIGNS) or mime_content.startswith(
                    JPG_SIGNS):
                if mime_content.startswith(PNG_SIGNS):
                    image_downloader(drop_data, '.png')
                elif mime_content.startswith(JPG_SIGNS):
                    image_downloader(drop_data, '.jpg')
                elif mime_content.startswith(GIF_SIGNS):
                    image_downloader(drop_data, '.gif')
            else:
                current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
                data_line = {'url_item': [{'content': drop_data, 'time': current_time}]}
                write_data_to_json(data_line)
        else:
            print('Connection error')
            con_er_msg = '''
            Это окно такое некрасивое потому что это окно ошибки.
            Проблемы с соедиением. Ну, по крайней мере по этой ссылке.
            Если подключен прокси - скорее всего проблема в нём. Пока не научил её работать с ним.
            В общем, можешь проверить интернет и нажать "Повторить" - если хочешь повторить.
            Ну или "Отмена" - если не так уж и хотелось.
            Цмок:*
            '''
            con_er_cho = ['Повторить', 'Отмена']
            if eg.ccbox(con_er_msg, 'Интрынет нет.', con_er_cho):
                drop_event(drop_data)
            else:
                return

    else:
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        data_line = {'text_item': [{'content': drop_data, 'time': current_time}]}
        write_data_to_json(data_line)
