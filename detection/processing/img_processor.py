import math
import zbar

import cv2
import numpy
from PIL import Image

from img_data import QrData


class ImgProcessor:
    def __init__(self):
        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('enable')
        self.qr_3d_model = numpy.array([
            (0.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (10.0, 10.0, 0.0),
            (0.0, 10.0, 0.0)])
        self.camera_matrix = numpy.array(
            [[532.80992189, 0.0, 342.4952186],
             [0.0, 532.93346421, 233.8879292],
             [0.0, 0.0, 1.0]])
        self.rotation_matrix = numpy.array(
            [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]], dtype=float)
        self.distortion_coefs = numpy.array(
            [-2.81325576e-01, 2.91130395e-02, 1.21234330e-03, -1.40825369e-04, 1.54865844e-01])
        self.window_height = 480
        self.fov = 90.0
        self.fov_rad = (self.fov / 180.0) * math.pi
        # self.real_side_size = 19.2
        self.real_side_size = 9.7
        self.magic_factor = 3.1
        self.axis_3d_model = numpy.array([(10, 0, 0), (0, 10, 0), (0, 0, 10)], dtype=float)

    def extract_data(self, frame):
        """
        Detects qr codes on image

        :param frame: array of pixels
        :return: data extracted from image
        :rtype: QrData
        """
        pil_image = ImgProcessor.convert_to_pil_format(frame)
        width, height = pil_image.size
        raw = pil_image.tobytes()
        zbar_image = zbar.Image(width, height, 'Y800', raw)

        qr_data = QrData()
        self.scanner.scan(zbar_image)

        # we assume there is only one code at a time
        qr_code = [code for code in zbar_image]
        if len(qr_code) == 0:
            return qr_data
        else:
            qr_code = qr_code[0]

        qr_data.set_text(qr_code.data)
        distance, side_size = self.calculate_distance(qr_code.location)

        qr_data.set_average_side_size(side_size)
        qr_data.set_distance(distance)

        qr_location = numpy.array(qr_code.location, dtype=float)

        retval, rvec, tvec = cv2.solvePnP(self.qr_3d_model, qr_location, self.camera_matrix, self.distortion_coefs)
        qr_data.set_rotation_and_translation(rvec, tvec)

        self.draw_xyz_axis(qr_code.location, qr_data.r_vec, qr_data.t_vec, frame)
        qr_data.set_camera_coordinates(self.get_camera_coordinates(qr_data.r_vec, qr_data.distance))
        return qr_data

    @staticmethod
    def average_side_size(qr_corners):
        sides_lengths = []
        n = len(qr_corners)
        for idx in range(0, n):
            x1 = qr_corners[idx][0]
            y1 = qr_corners[idx][1]
            x2 = qr_corners[(idx + 1) % n][0]
            y2 = qr_corners[(idx + 1) % n][1]
            sides_lengths.append(math.sqrt(math.pow(x2 - x1, 2.0) + (math.pow(y2 - y1, 2.0))))
        average_size = sum(sides_lengths) / n
        return average_size

    def draw_xyz_axis(self, qr_corners, r_vec, t_vec, image):
        corners = numpy.array(qr_corners, dtype=float)

        projected, jac = cv2.projectPoints(self.axis_3d_model, r_vec, t_vec,
                                           self.camera_matrix, self.distortion_coefs, corners)
        axis_end_x = tuple(projected[0].ravel())
        axis_end_y = tuple(projected[1].ravel())
        axis_end_z = tuple(projected[2].ravel())

        axis_end_x = tuple(int(coord) for coord in axis_end_x)
        axis_end_y = tuple(int(coord) for coord in axis_end_y)
        axis_end_z = tuple(int(coord) for coord in axis_end_z)

        axis_ends = [axis_end_x, axis_end_y, axis_end_z]

        cv2.line(image, qr_corners[0], axis_ends[0], (255, 0, 0), 5)
        cv2.line(image, qr_corners[0], axis_ends[1], (0, 255, 0), 5)
        cv2.line(image, qr_corners[0], axis_ends[2], (0, 0, 255), 5)

        rotation_matrix = cv2.Rodrigues(r_vec)[0]

        camera_position = - rotation_matrix.transpose() * t_vec
        for i in range(len(camera_position[0])):
            for j in range(len(camera_position[0])):
                camera_position[i][j] = int(camera_position[i][j])
                # print camera_position[2]

    def calculate_distance(self, vertices):
        side_size = ImgProcessor.average_side_size(vertices)
        if side_size <= 0:
            return

        real_height = self.window_height * (self.real_side_size / side_size)
        distance = (real_height / 2) * math.atan(self.fov_rad / 2.0) * self.magic_factor

        return distance, side_size

    def get_camera_coordinates(self, r_vec, distance):
        """
        Calculates coordinates in object world https://math.stackexchange.com/a/83578

        :param distance: estimated distance from camera
        :param r_vec: rotation vector
        :return: coordinates in qr code coordinate system
        """
        cv2.Rodrigues(r_vec, self.rotation_matrix)
        inv_rot = self.rotation_matrix.transpose()
        result = -inv_rot * numpy.array([0.0, 0.0, 1.0], dtype=float).transpose()
        return result.item(2) * distance, result.item(5) * distance, result.item(8) * distance

    @staticmethod
    def convert_to_pil_format(gray):
        # obtain image data
        pil = Image.fromarray(gray)
        return pil
