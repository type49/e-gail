

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



