#!/usr/bin/python
"""
    QR code (from video) scanner based on examples from
    https://github.com/opencv/opencv
    https://github.com/Zbar/Zbar
"""
import zbar

import cv2
from PIL import Image

# create a reader
scanner = zbar.ImageScanner()

# configure the reader
scanner.parse_config('enable')

cap = cv2.VideoCapture()

while True:
    if not cap.isOpened():
        cap.open(0)
        continue
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ###########################
    # create a reader
    scanner = zbar.ImageScanner()

    # configure the reader
    scanner.parse_config('enable')

    # obtain image data
    pil = Image.fromarray(gray)
    width, height = pil.size
    raw = pil.tobytes()

    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for barcode(s)
    scanner.scan(image)

    # extract results
    for symbol in image:
        # do something useful with results
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        vertices = symbol.location
        # draw lines on the gray frame
        cv2.line(frame, vertices[0], vertices[1], (0, 0, 255))
        cv2.line(frame, vertices[1], vertices[2], (0, 255, 0))
        cv2.line(frame, vertices[2], vertices[3], (255, 0, 0))
        cv2.line(frame, vertices[3], vertices[0], (0, 255, 255))
        for vertex in vertices:
            print 'point', '(%s, %s)' % vertex

    ###########################

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # clean up
    del image

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
###
raw = gray
width = gray.columns
height = gray.rows
