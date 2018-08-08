from PIL import Image


log = print


def crop(image, frame):
    """
    image 是一个 Image 对象
    frame 是一个 tuple 如下 (x, y, w, h)
        用于表示一个矩形的左上角座标 x y 和 宽高 w h

    不修改原图像
    返回一个 Image 对象, 它是用 frame 把 image 裁剪出来的新图像
    """
    img = image.convert('RGBA')
    x, y, w, h = frame
    new = Image.new('RGBA', (w, h))
    wold = img.width
    hold = img.height
    inew = 0
    for i in range(x, x + w):
        jnew = 0
        for j in range(y, y + h):
            p = (i, j)
            pnew = (inew, jnew)
            pix = img.getpixel(p)
            new.putpixel(pnew, pix)
            jnew += 1
        inew += 1
    return new



def flip(image):
    """
    image 是一个 Image 对象

    不修改原图像
    返回一个 Image 对象, 它是 image 上下镜像的图像
    """
    img = image.convert('RGBA')
    w = img.width
    h = img.height
    new = Image.new('RGBA', (w, h))
    inew = 0
    for i in range(w):
        inew = w - i - 1
        for j in range(h):
            p = (i, j)
            pnew = (inew, j)
            pix = img.getpixel(p)
            new.putpixel(pnew, pix)
    return new



def flop(image):
    """
    image 是一个 Image 对象

    不修改原图像
    返回一个 Image 对象, 它是 image 左右镜像的图像
    """
    img = image.convert('RGBA')
    w = img.width
    h = img.height
    new = Image.new('RGBA', (w, h))
    inew = 0
    for i in range(h):
        inew = h - i - 1
        log(inew)
        for j in range(w):
            p = (j, i)
            pnew = (j, inew)
            pix = img.getpixel(p)
            new.putpixel(pnew, pix)
    return new


def main():
    img = Image.open('a.jpg')
    imgcrop = crop(img, (20, 20, 20, 20))
    imgcrop.save('crop.png')
    imgflip = flip(img)
    imgflip.save('flip.png')
    imgflop = flop(img)
    imgflop.save('flop.png')


if __name__ == '__main__':
    main()