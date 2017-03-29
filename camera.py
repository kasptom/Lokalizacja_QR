#!/usr/bin/python
"""
    QR code (from video) scanner based on examples from
    https://github.com/opencv/opencv
    https://github.com/Zbar/Zbar
"""
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
    print 'distance' '%s', calculate_distance(symbol.location)
    for vertex in symbol.location:
        print 'point', '(%s, %s)' % vertex


def calculate_distance(vertices):
    pass


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
