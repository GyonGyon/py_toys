from PIL import Image

log = print


# gray = int((r * 30 + g * 59 + b * 11) / 100)
# gray = int(r * 0.3 + g * 0.59 + b * 0.11)
# gray = (r * 76 + g * 151 + b * 28) >> 8
# gray = int((r + g + b) / 3)
# gray = g

def gray1(r, g, b):
    return int((r * 30 + g * 59 + b * 11) / 100)


def gray2(r, g, b):
    return int(r * 0.3 + g * 0.59 + b * 0.11)


def gray3(r, g, b):
    return (r * 76 + g * 151 + b * 28) >> 8


def gray4(r, g, b):
    return int((r + g + b) / 3)


def gray5(r, g, b):
    return g

graytype_table = {
    1: gray1,
    2: gray2,
    3: gray3,
    4: gray4,
    5: gray5,
}

def grayscale(image, graytype = 1):
    img = image.convert('RGBA')
    w = img.width
    h = img.height
    new = Image.new('RGBA', (w, h))
    for i in range(w):
        for j in range(h):
            p = (i, j)
            r, g, b, a = img.getpixel(p)
            gray = graytype_table[graytype](r, g, b)
            # if i == 25 and j == 25:
                # log(r, g, b, gray)
            new.putpixel(p, (gray, gray, gray, a))
    return new


def main():
    img = Image.open("sample.png")
    for i in range(1, 6):
        new = grayscale(img, i)
        new.save('gray{}.png'.format(i))


if __name__ == '__main__':
    main()
