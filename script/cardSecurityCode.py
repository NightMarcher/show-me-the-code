#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def randomChar():
    return chr(random.randint(65, 90))

def randomColor1():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

def randomColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

if __name__ == '__main__':
	width, height = 60 * 4, 60
	image = Image.new('RGB', (width, height), (255, 255, 255))
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype('../Arial.ttf', 36)
	for w in range(width):
	    for h in range(height):
	        draw.point((w, h), fill=randomColor1())
	for c in range(4):
	    draw.text((60 * c + 10, 10), randomChar(), font=font, fill=randomColor2())
	image = image.filter(ImageFilter.BLUR)
	image.save('../cardSecurityCode.jpg', 'jpeg')
