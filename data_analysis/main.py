import os
import sys
import json
import enum
import urllib.request
from city_table import city_post_table, PathTable

log = print


def add_csv_province(path):
    out = '序号,商品名,产地（省）,产地,价格\n'
    citys, provinces = city_post_table()
    with open(path, 'r') as f:
        s = f.readline()
        s = f.readline()
        while s != '':
            l = s.split(',')
            prefecture = l[2]
            log(l)
            log(prefecture)
            province = citys[prefecture]['province']
            l.insert(2, province)
            s_new = ','.join(l)
            out += s_new
            s = f.readline()
    return out


def write_csv(path, data):
    with open(path, 'w') as f:
        f.write(data)


def main():
    data = add_csv_province(PathTable.origin)
    write_csv(PathTable.out, data)
    pass


if __name__ == '__main__':
    main()
