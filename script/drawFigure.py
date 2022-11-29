#! /usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

x = [i for i in range(8)]
xTicks = ['Backpack', 'Cable', 'Classroom1', 'Couch', 'Flower', 'Mask', 'Shopvac', 'Sticks']

JPEG_PSNR = [28.80, 31.11, 32.79, 34.82, 29.99, 31.89, 30.83, 29.49]
L4_PSNR = [30.71, 34.08, 36.26, 37.40, 33.12, 36.51, 34.18, 31.44]
L8_PSNR = [30.85, 34.28, 36.49, 37.68, 33.29, 36.81, 34.34, 31.61]
L12_PSNR = [30.83, 34.26, 36.49, 37.73, 33.27, 36.76, 34.30, 31.62]

JPEG_SSIM = [0.9040, 0.9529, 0.9769, 0.9719, 0.9577, 0.9771, 0.9612, 0.9174]
L4_SSIM = [0.9400, 0.9806, 0.9922, 0.9879, 0.9853, 0.9935, 0.9861, 0.9561]
L8_SSIM = [0.9433, 0.9832, 0.9934, 0.9896, 0.9875, 0.9949, 0.9882, 0.9603]
L12_SSIM = [0.9434, 0.9834, 0.9936, 0.9898, 0.9876, 0.9949, 0.9882, 0.9606]

fig = plt.figure()
ax1 = fig.add_subplot(111)
s1 = ax1.scatter(x, L4_PSNR, color='lime', marker='*', s=100, alpha=0.9, linewidths=0, edgecolors='black', label='L4_PSNR')
s2 = ax1.scatter(x, L8_PSNR, color='orange', marker='o', s=50, alpha=0.9, linewidths=0, edgecolors='black', label='L8_PSNR')
s3 = ax1.scatter(x, L12_PSNR, color='red', marker='d', s=50, alpha=0.9, linewidths=0, edgecolors='black', label='L12_PSNR')
s4 = ax1.scatter(x, JPEG_PSNR, color='cyan', marker='s', s=50, alpha=0.9, linewidths=0, edgecolors='black', label='JPEG_PSNR')
ax1.set_xlabel('Image Involved')
ax1.set_ylabel('PSNR(dB)')

ax2 = ax1.twinx()
s5 = ax2.scatter(x, L4_SSIM, color='ivory', marker='*', s=70, alpha=0.9, linewidths=1.5, edgecolors='lime', label='L4_SSIM')
s6 = ax2.scatter(x, L8_SSIM, color='ivory', marker='o', alpha=0.9, linewidths=1.5, edgecolors='orange', label='L8_SSIM')
s7 = ax2.scatter(x, L12_SSIM, color='ivory', marker='d', alpha=0.9, linewidths=1.5, edgecolors='red', label='L12_SSIM')
s8 = ax2.scatter(x, JPEG_SSIM, color='ivory', marker='s', alpha=0.9, linewidths=1.5, edgecolors='cyan', label='JPEG_SSIM')
ax2.set_ylabel('SSIM')

plt.xticks(x, xTicks, rotation=0)
plt.legend([s1, s2, s3, s4, s5, s6, s7, s8], ['L4_PSNR', 'L8_PSNR', 'L12_PSNR', 'JPEG_PSNR', 'L4_SSIM', 'L8_SSIM', 'L12_SSIM', 'JPEG_SSIM'], loc='best', shadow=True)
# plt.title('')
plt.grid(True)
# plt.savefig('', dpi=300)
plt.show()
