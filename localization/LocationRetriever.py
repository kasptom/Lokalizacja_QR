import json

import numpy

DEFAULT_RAWSON_PATH = "../resources/room.roson"


class LocationRetriever:
    def __init__(self, rawson_file_path=None):
        self.rawson = rawson_file_path if rawson_file_path is not None else DEFAULT_RAWSON_PATH
        self.room_map = self.load_json_from_file(file_name=self.rawson)

    def retrieve_location(self, qr_code_id, coordinates):
        qr_code_list = self.room_map['qrcodes']
        for qr_code in qr_code_list:
            if qr_code['id'] == qr_code_id:
                return self.to_room_coordinates(qr_code, coordinates)
        return None

    @staticmethod
    def load_json_from_file(file_name):
        file_pointer = open(file_name, 'r')
        return json.load(file_pointer)

    @staticmethod
    def to_room_coordinates(qr_code, coordinates):
        a = coordinates[0] / 100.0
        b = coordinates[1] / 100.0
        c = coordinates[2] / 100.0
        position = qr_code['position']

        x_nw = position['NW']['x']
        y_nw = position['NW']['y']
        x_ne = position['NE']['x']
        y_ne = position['NE']['y']
        x_sw = position['SW']['x']
        y_sw = position['SW']['y']

        ox = numpy.array([x_ne - x_nw, y_ne - y_nw, 0], dtype=float)
        oy = numpy.array([x_sw - x_nw, y_sw - y_nw, 0], dtype=float)
        oz = numpy.cross(ox, oy)

        i = ox / numpy.linalg.norm(ox)
        j = oy / numpy.linalg.norm(oy)
        k = oz / numpy.linalg.norm(oz)

        height = qr_code['height']
        room_location = numpy.array([x_nw, y_nw, height], dtype=float) + a * i + b * j + c * k
        return room_location

