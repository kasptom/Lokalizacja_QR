class QrData:
    def __init__(self):
        self.text = "N/A"
        self.distance = -1
        self.r_vec = None
        self.t_vec = None
        self.camera_coordinates = [0, 0, 0]

    def set_text(self, text):
        self.text = text

    def set_distance(self, distance):
        self.distance = distance

    def set_rotation_and_translation(self, r_vec, t_vec):
        self.r_vec = r_vec
        self.t_vec = t_vec

    def set_camera_coordinates(self, coordinates):
        self.camera_coordinates = coordinates
