#! /usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

def addNum2Avatar(img):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('../Arial.ttf', size=70)
    color = '#ff0000'
    width, height = img.size
    draw.text((width - 75, 0), '99', font=font, fill=color)
    img.save('../markedAvatar.jpg', 'jpeg')

if __name__ == '__main__':
    image = Image.open('../avatar.jpg')
    addNum2Avatar(image)
