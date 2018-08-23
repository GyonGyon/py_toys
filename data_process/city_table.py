import os
import sys
import json
import enum
import urllib.request


log = print


class PathTable(str, enum.Enum):
    test = 'test'
    root = sys.path[0]
    citys = '{}/citys.json'.format(root)
    provinces = '{}/provinces.json'.format(sys.path[0])
    post = '{}/post'.format(sys.path[0])
    origin = '{}/info.csv'.format(sys.path[0])
    out = '{}/out.csv'.format(sys.path[0])
    excelin = '{}/info.xlsx'.format(d)
    excelout = '{}/out.xlsx'.format(d)


# Path_table = dict(
#     root=sys.path[0],
#     citys='{}/citys.json'.format(sys.path[0]),
#     provinces='{}/provinces.json'.format(sys.path[0]),
#     post='{}/provinces.json'.format(sys.path[0]),
# )


def parsed_city_post_table():
    log('parse')
    root = sys.path[0]
    path = PathTable.post
    citys = {}
    provinces = {}
    with open(path, 'r') as f:
        s = f.readline()
        while s != '':
            l = s.split('\t')
            name = l[1]
            postcode = l[0]
            provincecode = postcode[0: 2]
            citycode = postcode[2: 4]
            prefecturecode = postcode[4: 6]
            if citycode == '00' and prefecturecode == '00':
                provinces[provincecode] = name
            city = {
                'postcode': l[0],
                'provincecode': provincecode,
                'province': provinces[provincecode],
                'citycode': citycode,
                'prefecturecode': prefecturecode,
            }
            citys[name] = city
            s = f.readline()
            pass
    write_city_post_table(citys, provinces)
    return (citys, provinces)


def write_json_utf8(path, data):
    with open(path, 'w', encoding='utf8') as f:
        s = json.dumps(data, ensure_ascii=False)
        f.write(s)


def read_json_utf8(path):
    with open(path, 'r', encoding='utf8') as f:
        s = json.load(f)
    return s


def write_city_post_table(citys, provinces):
    path_citys = PathTable.citys
    write_json_utf8(path_citys, citys)

    path_provinces = PathTable.provinces
    write_json_utf8(path_provinces, provinces)


def city_post_table():
    path_citys = PathTable.citys
    path_provinces = PathTable.provinces
    if not os.path.exists(path_citys):
        return parsed_city_post_table()
    citys = read_json_utf8(path_citys)
    provinces = read_json_utf8(path_provinces)
    return (citys, provinces)


def openurl(url):
    s = urllib.request.urlopen(url).read()
    content = s.decode('utf-8')
    return content


def test():
    url = 'http://www.mca.gov.cn/article/sj/tjbz/a/2017/201801/201801151447.html'
    s = openurl(url)
    log(s)


def main():
    # test()
    # parsed_city_post_table()
    citys, provinces = city_post_table()
    log(provinces)
    pass


if __name__ == '__main__':
    main()
