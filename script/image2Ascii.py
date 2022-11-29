#! /usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image

def getChar(length, r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    gray = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return Ascii[int(gray / 256.0 * length)]

if __name__ == '__main__':
    Ascii = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'.'
    length = len(Ascii)
    image = Image.open('../Eva.jpg')
    width, height = 180, 100
    image = image.resize((width, height))
    for i in range(height):
        txt = ''
        for j in range(width):
            txt += getChar(length, *image.getpixel((j, i)))
        txt += '\n'
        with open('../Ascii', 'a') as f:
            f.write(txt)
