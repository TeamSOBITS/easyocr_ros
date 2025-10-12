import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose
import cv2
import numpy as np
import easyocr
import time
import yaml
import os
from ament_index_python.packages import get_package_share_directory


class Easy_Ocr(Node):
    def __init__(self):
        super().__init__('easy_ocr')
        config_file_path = os.path.join(get_package_share_directory('easyocr_ros'), 'params', 'config.yaml')
        self.ocr_params = self.load_params_from_yaml(config_file_path)

        self.declare_parameter('topic_name', '/image_raw')
        self.declare_parameter('gpu', True)
        self.declare_parameter('classifier_name', 'easy_ocr')
        self.declare_parameter('languages', ['en'])
        self.declare_parameter('visualize_duration', 0.0167)
        self.declare_parameter('enable_visualization', True)
        self.declare_parameter('grayscale_mode', False)
        self.declare_parameter('downscale_ratio', 1.0)

        self.params = {param: self.get_parameter(param).value for param in [
            'topic_name', 'gpu', 'classifier_name', 'languages', 'visualize_duration', 'enable_visualization', 'grayscale_mode', 'downscale_ratio']}

        self.subscription = self.create_subscription(Image, self.params['topic_name'], self.listener_callback, 10)
        self.publisher = self.create_publisher(Detection2DArray, 'easy_ocr_result', 10)
        self.logger = self.get_logger()
        self.reader = easyocr.Reader(self.params['languages'], gpu=self.params['gpu'])
        self.image = None
        self.processed_image = None
        self.image_data = None  
        self.timer = self.create_timer(self.params['visualize_duration'], self.process_image)
        self.last_time = time.time()

    def load_params_from_yaml(self, yaml_file):
        with open(yaml_file, 'r') as file:
            return yaml.safe_load(file)

    def listener_callback(self, msg):
        self.height = msg.height
        self.width = msg.width
        self.image_data = msg.data
    
    def process_image(self):
        if self.image_data is None:
            self.logger.error("No image data received from the camera topic.")
            return

        try:
            self.image = np.frombuffer(self.image_data, dtype=np.uint8).reshape(self.height, self.width, -1)
            self.image = self.image[:, :, [2, 1, 0]]
            downscale_ratio = self.params['downscale_ratio']
            if downscale_ratio <= 0:
                self.logger.error("Invalid downscale_ratio: Value must be greater than 0")
                return

            self.image = cv2.resize(self.image, (int(self.width * downscale_ratio), int(self.height * downscale_ratio)))
            if self.params['grayscale_mode']:
                self.processed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)                    
            else:
                self.processed_image = self.image
            results = self.reader.readtext(self.processed_image, **self.ocr_params)

            detection_array_msg = Detection2DArray()
            detection_array_msg.header.stamp = self.get_clock().now().to_msg()
            detection_array_msg.header.frame_id = "camera_frame"
            for (bbox, text, prob) in results:
                self.logger.info(f"Detected text: {text} (confidence: {prob:.2f})")
    
                detection = Detection2D()
                x_min = float(bbox[0][0])
                y_min = float(bbox[0][1])
                x_max = float(bbox[2][0])
                y_max = float(bbox[2][1])
                width = x_max - x_min
                height = y_max - y_min
                center_x = x_min + width / 2
                center_y = y_min + height / 2

                detection.bbox.center.position.x = center_x
                detection.bbox.center.position.y = center_y
                detection.bbox.size_x = width
                detection.bbox.size_y = height

                hypothesis = ObjectHypothesisWithPose()
                hypothesis.hypothesis.class_id = text
                hypothesis.hypothesis.score = prob

                detection.results.append(hypothesis)
                detection_array_msg.detections.append(detection)

                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                cv2.rectangle(self.processed_image, top_left, bottom_right, (0, 255, 0), 2)

                cv2.putText(self.processed_image, f"{text} ({prob:.2f})", (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            self.publisher.publish(detection_array_msg)

            if self.params['enable_visualization']:
                cv2.imshow('OCR Visualization', self.processed_image)
                cv2.waitKey(1)

        except Exception as e:
            self.logger.error(f"Image processing error: {e}")

def main(args=None):
    rclpy.init(args=args)
    easy_ocr = Easy_Ocr()
    try:
        rclpy.spin(easy_ocr)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()