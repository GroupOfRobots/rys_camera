from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image

import rclpy

from picamera2 import Picamera2
from builtin_interfaces.msg import Time

import cv2
from cv_bridge import CvBridge
import numpy as np

WIDTH = 640
HEIGHT = 480

FRAME_INTERVAL = 0.1

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')

        self.publisher = self.create_publisher(Image, 'video_frames', 10)

        self.picam2 = Picamera2()
        # self.picam2.configure(self.picam2.create_video_configuration(main={"size": (HEIGHT, WIDTH)}))
        # config = self.picam2.create_preview_configuration(lores={"size": (640,480)})
        config = self.picam2.create_preview_configuration(lores={"size": (640,480)})

        self.picam2.configure(config)

        self.picam2.start()

        self.frame_id = 0

        self.create_timer(FRAME_INTERVAL, self.image_callback)

    def get_time_msg(self):
        time_msg = Time()
        msg_time = self.get_clock().now().seconds_nanoseconds()
        time_msg.sec = int(msg_time[0])
        time_msg.nanosec = int(msg_time[1])
        return time_msg

    def image_callback(self):
        yuv = self.picam2.capture_array("lores")
        self.img = cv2.cvtColor(yuv, cv2.COLOR_YUV420p2RGB)[0:450, 100:540]
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(gray, kernel, iterations=1)
        ret, thresh = cv2.threshold(img_erosion, 127, 255, cv2.THRESH_BINARY_INV)
        # Negative binn
        # thresh = cv2.bitwise_not(thresh)

        br = CvBridge()
        msg = br.cv2_to_imgmsg(thresh)
        msg.header.stamp = self.get_time_msg()
        self.frame_id += 1
        msg.header.frame_id = str(self.frame_id)

        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)
    image_publisher.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
