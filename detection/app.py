import cv2

from camera import Camera
from detection.processing.img_processor import ImgProcessor

camera = Camera(camera_id=1)
processor = ImgProcessor()

while True:
    if not camera.is_opened():
        camera.open()
        continue

    image_gray = camera.get_frame_gray_scale()

    # wrap image data
    qr_data = processor.extract_data(image_gray)

    if qr_data.distance >= 0:
        print "distance {}".format(qr_data.distance)
        print "camera coordinates {}".format(qr_data.camera_coordinates)
    # Display the resulting frame
    cv2.imshow('frame', image_gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    del image_gray

# When everything done, release the capture
camera.close()
cv2.destroyAllWindows()
