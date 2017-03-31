#!/usr/bin/python
"""
    QR code (from video) scanner based on examples from
    https://github.com/opencv/opencv
    https://github.com/Zbar/Zbar
"""
import math
import zbar
import numpy

import cv2
from PIL import Image

# create and configure a reader
scanner = zbar.ImageScanner()
scanner.parse_config('enable')

cap = cv2.VideoCapture(1)


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


def enlarge(point_a, point_b):
    k = 50
    coef_1 = point_a[0] - point_b[0]
    coef_2 = point_a[1] - point_b[1]
    return point_a[0] - (coef_1 * k), point_a[1] - (coef_2 * k)


def draw_xyz_axis(object_points, rvec, tvec, matrix, coefs, image_points, vertices):
    imgpts, jac = cv2.projectPoints(object_points, rvec, tvec, matrix, coefs, image_points)
    img_point = tuple(imgpts[0].ravel())
    img_point2 = tuple(imgpts[1].ravel())
    img_point3 = tuple(imgpts[2].ravel())
    img_point_ints = [(int(img_point[0]), int(img_point[1])), (int(img_point2[0]), int(img_point2[1])),
                      (int(img_point3[0]), int(img_point3[1]))]
    cv2.line(frame, vertices[0], img_point_ints[0], (255, 0, 0), 5)
    cv2.line(frame, vertices[0], img_point_ints[1], (0, 255, 0), 5)
    cv2.line(frame, vertices[0], img_point_ints[2], (0, 0, 255), 5)
    print rvec, tvec


def calculate_distance(vertices):
    fov = 90.0
    fov_rad = (fov / 180.0) * math.pi
    real_side_size = 27.5

    magic_factor = 3.1

    side_size = average_side_size(vertices)
    window_height = 480
    real_height = window_height * (real_side_size / side_size)
    distance = (real_height / 2) * math.atan(fov_rad / 2.0) * magic_factor
    camera_matrix = numpy.array(
        [[532.80992189, 0.0, 342.4952186],
         [0.0, 532.93346421, 233.8879292],
         [0.0, 0.0, 1.0]])
    object_points = numpy.array([
        (0.0, 0.0, 0.0),
        (10.0, 0.0, 0.0),
        (10.0, 10.0, 0.0),
        (0.0, 10.0, 0.0)])
    image_points = numpy.array(vertices, dtype=float)
    distortion_coefs = numpy.array([-2.81325576e-01, 2.91130395e-02, 1.21234330e-03, -1.40825369e-04, 1.54865844e-01])
    retval, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, distortion_coefs)
    axis_points = numpy.array([(10, 0, 0), (0, 10, 0), (0, 0, 10)], dtype=float)
    draw_xyz_axis(axis_points, rvec, tvec, camera_matrix, distortion_coefs, image_points, vertices)
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
        # mark_qr_code(qr_code.location)
        print_qr_info(qr_code)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    del image

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
