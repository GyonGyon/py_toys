import json
import urllib.request


log = print


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


def translate(word):
    key = '5ECCF2BFE29482607F1970245FD41519'
    url = 'http://dict-co.iciba.com/api/dictionary.php?type=json&key={}&w={}'.format(
        key, word)
    string = openurl(url)
    parts = json.loads(string)['symbols'][0]['parts']
    s = means(parts)
    return s


def main():
    word = 'name'
    s = translate(word)
    log(s)


if __name__ == '__main__':
    main()
