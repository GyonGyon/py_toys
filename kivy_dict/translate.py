import json
import urllib.request
import sys


log = print

key = '5ECCF2BFE29482607F1970245FD41519'


def openurl(url):
    s = urllib.request.urlopen(url).read()
    content = s.decode('utf-8')
    return content


def means(parts):
    s = ''
    for part in parts:
        t = part['part']
        s += t + '\n'
        means = part['means']
        for mean in means:
            s += mean + '\n'
        s += '\n'
    return s


def fetch_info(word):
    url = 'http://dict-co.iciba.com/api/dictionary.php?type=json&key={}&w={}'.format(
        key, word)
    string = openurl(url)
    info = json.loads(string)
    null = {'symbols': [
        {'ph_am_mp3': '', 'ph_en_mp3': '', 'ph_other': '', 'ph_tts_mp3': ''}]}
    if info == null:
        return None
    return info


def translate(info):
    if info == None:
        return
    parts = info['symbols'][0]['parts']
    s = means(parts)
    return s


def download(url, name):
    path = audio_path(name)
    s = urllib.request.urlopen(url).read()
    # 'w' 表示写入  'b' 表示二进制模式
    with open(path, 'wb') as f:
        f.write(s)
    return path


def audio_path(name):
    root = sys.path[0]
    path = '{}/audio/{}.mp3'.format(root, name)
    return path


def download_audio(info, name):
    if info == None:
        return
    ph_am_mp3 = info['symbols'][0]['ph_am_mp3']
    log(ph_am_mp3)
    if ph_am_mp3 == '':
        return None
    url = '{}?key={}'.format(ph_am_mp3, key)
    path = download(url, name)
    return path


def main():
    word = 'name'
    s = translate(word)
    log(s)


if __name__ == '__main__':
    main()
