"""
https://mp.weixin.qq.com/s/pphBiEX099ZkDV0hWwnbhw

pip install opencv-contrib-python==4.7.0.72
"""
import cv2
import numpy as np


# init detector
detector = cv2.wechat_qrcode_WeChatQRCode(
    "cnn_models/detect.prototxt",
    "cnn_models/detect.caffemodel",
    "cnn_models/sr.prototxt",
    "cnn_models/sr.caffemodel"
)

# read image

# Method 1
# with open("test.png", "rb") as f:
#     bs = f.read()
# array = np.frombuffer(bs, dtype=np.uint8)
# img = cv2.imdecode(array, cv2.IMREAD_GRAYSCALE)

# Method 2
# img = cv2.imread("test.png", cv2.IMREAD_COLOR)

# Method 3
img = cv2.imread("test-reverse.png", cv2.IMREAD_GRAYSCALE)
img = 255 - img  # reverse gray scale

# detect
strings, coordinates = detector.detectAndDecode(img)
print(strings)
print(coordinates)

# draw
for target in coordinates:
    color = (0, 0, 255)
    thick = 2
    for pos in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        start = int(target[pos[0]][0]), int(target[pos[0]][1])
        end = int(target[pos[1]][0]), int(target[pos[1]][1])
        cv2.line(img, start, end, color, thick)
cv2.imwrite("detected.jpg", img)
