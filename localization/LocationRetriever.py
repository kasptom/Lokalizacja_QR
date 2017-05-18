import json


class LocationRetriever:
    def __init__(self, rawson_file_path):
        self.rawson = rawson_file_path
        self.room_map = self.load_json_from_file(file_name=rawson_file_path)

    def retrieve_location(self, qr_code_id):
        qr_code_list = self.room_map['qrcodes']
        qr_code_id_str = str(qr_code_id)
        for qr_code in qr_code_list:
            if qr_code['id'] == qr_code_id_str:
                print(qr_code)

    @staticmethod
    def load_json_from_file(file_name):
        file_pointer = open(file_name, 'r')
        return json.load(file_pointer)


retriever = LocationRetriever("../resources/room.roson")
retriever.retrieve_location(2)
