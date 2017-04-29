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
            [[5.2899351181828501e+02, 0., 2.9450258403806163e+02],
             [0., 5.2899351181828501e+02, 2.2097639018482772e+02],
             [0.0, 0.0, 1.0]])
        self.rotation_matrix = numpy.array(
            [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]], dtype=float)
        self.distortion_coefs = numpy.array(
            [1.1393838013330945e-01, 1.2711065646876812e-01,
             -3.4306406160909859e-02, -1.0243554211321552e-02,
             -1.1529950378308689e+00])
        self.window_height = 480
        self.fov = 90.0
        self.fov_rad = (self.fov / 180.0) * math.pi
        self.real_side_size = 19.2
        # self.real_side_size = 9.7
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
        qr_data.set_camera_coordinates(self.get_camera_coordinates(qr_data.r_vec, qr_data.t_vec, qr_data.distance))
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

    def get_camera_coordinates(self, r_vec, t_vec, distance):
        """
        Calculates coordinates in object world.

        :param t_vec: translation vector
        :param distance: estimated distance from camera using :func:`ImgProcessor.calculate_distance`
        :param r_vec: rotation vector
        :return: coordinates in qr code coordinate system
        """
        cv2.Rodrigues(r_vec, self.rotation_matrix)
        inv_rot = self.rotation_matrix.transpose()

        camera_position = -numpy.matrix(inv_rot) * numpy.matrix(t_vec)
        camera_position = camera_position.item(0), camera_position.item(1), camera_position.item(2)
        return tuple(self.with_calculated_distance(camera_position, distance))

    @staticmethod
    def convert_to_pil_format(gray):
        # obtain image data
        pil = Image.fromarray(gray)
        return pil

    @staticmethod
    def distance_from_xyz(camera_position):
        return math.sqrt(
            math.pow(camera_position[0], 2) + math.pow(camera_position[1], 2) + math.pow(camera_position[2], 2)
        )

    def with_calculated_distance(self, camera_position, distance):
        """
        Applies distance calculated with :func:`ImgProcessor.calculate_distance`

        :param camera_position: coordinates calculated from rotation and translation
        :param distance: :func:`ImgProcessor.calculate_distance`
        :return: coordinates of a camera with corrected distance
        """
        distance_xyz = self.distance_from_xyz(camera_position)
        camera_position_with_distance = [camera_position[0] * distance / distance_xyz,
                                         camera_position[1] * distance / distance_xyz,
                                         camera_position[2] * distance / distance_xyz]
        return camera_position_with_distance
