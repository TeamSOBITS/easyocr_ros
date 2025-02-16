import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from sobits_interfaces.msg import BoundingBox, BoundingBoxes
import cv2
import numpy as np
import easyocr
import time
import yaml
import os

class Easy_Ocr(Node):
    def __init__(self):
        super().__init__('easy_ocr')
        # Load parameters from YAML file
        script_dir = os.path.dirname(__file__)
        config_file_path = os.path.join(script_dir, '../params/config.yaml')
        self.ocr_params = self.load_params_from_yaml(config_file_path)

        # Declare parameters to be loaded from launch file
        self.declare_parameter('topic_name', '/image_raw')
        self.declare_parameter('gpu', True)
        self.declare_parameter('classifier_name', 'easy_ocr')
        self.declare_parameter('languages', ['en'])
        self.declare_parameter('visualize_duration', 0.0167)
        self.declare_parameter('enable_visualization', True)
        self.declare_parameter('grayscale_mode', False)
        self.declare_parameter('downscale_ratio', 2)  # Changed to integer type

        # Get parameters from launch file and overwrite
        self.params = {param: self.get_parameter(param).value for param in [
            'topic_name', 'gpu', 'classifier_name', 'languages', 'visualize_duration', 'enable_visualization', 'grayscale_mode', 'downscale_ratio']}

        self.subscription = self.create_subscription(Image, self.params['topic_name'], self.listener_callback, 10)
        self.publisher = self.create_publisher(BoundingBoxes, 'easy_ocr_result', 10)

        self.logger = self.get_logger()
        # Initialize EasyOCR reader
        self.reader = easyocr.Reader(self.params['languages'], gpu=self.params['gpu'])

        self.image = None
        self.processed_image = None
        self.image_data = None  

        # Update image based on frequency
        self.timer = self.create_timer(self.params['visualize_duration'], self.process_image)
        
        self.last_time = time.time()

    def load_params_from_yaml(self, yaml_file):
        with open(yaml_file, 'r') as file:
            return yaml.safe_load(file)

    def listener_callback(self, msg):
        # Get image message height and width
        self.height = msg.height
        self.width = msg.width
        # Get image data
        self.image_data = msg.data
    
    def process_image(self):
        if self.image_data is None:
            self.logger.error("No image data received from the camera topic.")
            return

        try:
            # Convert image data to NumPy array
            self.image = np.frombuffer(self.image_data, dtype=np.uint8).reshape(self.height, self.width, -1)

            # Check if downscale_ratio is a valid integer
            downscale_ratio = self.params['downscale_ratio']
            if downscale_ratio <= 0:
                self.logger.error("Invalid downscale_ratio: Value must be greater than 0")
                return

            # Reduce image resolution
            self.image = cv2.resize(self.image, (self.width // downscale_ratio, self.height // downscale_ratio))
            
            # Select image processing method
            if self.params['grayscale_mode']:
                self.processed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)                    
            else:
                self.processed_image = self.image
                
            # Apply EasyOCR with specified parameters
            results = self.reader.readtext(self.processed_image, **self.ocr_params)
            
            bounding_boxes_msg = BoundingBoxes()
            for (bbox, text, prob) in results:
                # Log detected text and confidence
                self.logger.info(f"Detected text: {text} (confidence: {prob:.2f})")
                
                # Create bounding box message
                bounding_box = BoundingBox()
                bounding_box.class_name = text
                bounding_box.probability = prob
                bounding_box.xmin = int(bbox[0][0])
                bounding_box.ymin = int(bbox[0][1])
                bounding_box.xmax = int(bbox[2][0])
                bounding_box.ymax = int(bbox[2][1])
                
                bounding_boxes_msg.bounding_boxes.append(bounding_box)
                
                # Draw bounding box
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                cv2.rectangle(self.processed_image, top_left, bottom_right, (0, 255, 0), 2)
                # Draw text
                cv2.putText(self.processed_image, f"{text} ({prob:.2f})", (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            self.publisher.publish(bounding_boxes_msg)

            # Display image
            if self.params['enable_visualization']:
                cv2.imshow('OCR Visualization', self.processed_image)
                cv2.waitKey(1)

        except Exception as e:
            # Log error message if an error occurs
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