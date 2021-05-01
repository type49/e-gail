
def txt_file(file):
    file = open(file, 'r', encoding='utf-8')
    dry_text = file.readlines()
    text = ''
    for i in range(len(dry_text)):
        text = text + dry_text[i]
    return text.split('\n')


def input_text(text_file):
    if text_file.endswith('txt'):
        return txt_file(text_file)
    else:
        return



hellows = ''.join(input_text(r'data/answers/hello.txt')).lower().split('%')[1:-1]
start_messages = ''.join(input_text(r'data/answers/start.txt')).lower().split('%')[1:-1]
ball42 = ''.join(input_text(r'data/answers/ball42.txt')).lower().split('%')[1:-1]
start_ask = ''.join(input_text(r'data/answers/asking_start.txt')).lower().split('%')[1:-1]
