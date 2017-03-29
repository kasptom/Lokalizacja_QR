#!/usr/bin/python
"""
    QR code (from video) scanner based on examples from
    https://github.com/opencv/opencv
    https://github.com/Zbar/Zbar
"""
import math
import zbar

import cv2
from PIL import Image

# create and configure a reader
scanner = zbar.ImageScanner()
scanner.parse_config('enable')

cap = cv2.VideoCapture()


def mark_qr_code(vertices):
    cv2.line(frame, vertices[0], vertices[1], (0, 0, 255), 3)
    cv2.line(frame, vertices[1], vertices[2], (0, 255, 0), 3)
    cv2.line(frame, vertices[2], vertices[3], (255, 0, 0), 3)
    cv2.line(frame, vertices[3], vertices[0], (0, 255, 255), 3)


def print_qr_info(symbol):
    print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
    distance, side_size = calculate_distance(symbol.location)
    print 'distance', distance, 'avg side size', side_size
    # for vertex in symbol.location:
    #     print 'point', '(%s, %s)' % vertex


def average_side_size(vertices):
    sides_lengths = []
    n = len(vertices)
    for idx in range(0, n):
        x1 = vertices[idx][0]
        y1 = vertices[idx][1]
        x2 = vertices[(idx + 1) % n][0]
        y2 = vertices[(idx + 1) % n][1]
        sides_lengths.append(math.sqrt(math.pow(x2 - x1, 2.0) + (math.pow(y2 - y1, 2.0))))
    average_size = sum(sides_lengths) / n
    # print 'avg size', average_size
    return average_size


def calculate_distance(vertices):
    fov = 45.0
    fov_rad = (fov / 180.0) * math.pi
    real_side_size = 27

    magic_factor = 6.67

    side_size = average_side_size(vertices)
    window_height = 480
    real_height = window_height * (real_side_size / side_size)
    distance = (real_height/2) * math.atan(fov_rad / 2.0) * magic_factor
    return distance, side_size


while True:
    if not cap.isOpened():
        cap.open(0)
        continue
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # obtain image data
    pil = Image.fromarray(gray)
    width, height = pil.size
    raw = pil.tobytes()

    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for qr codes
    scanner.scan(image)

    # extract results
    for qr_code in image:
        mark_qr_code(qr_code.location)
        print_qr_info(qr_code)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    del image

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
