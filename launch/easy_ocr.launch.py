from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='easyocr_ros',
            executable='easy_ocr',
            name='easy_ocr',
            output='screen',
            parameters=[
                {'topic_name': '/image_raw'},    # Topic name to subscribe to for image data
                {'gpu': True},                   # Use GPU for OCR processing
                {'classifier_name': 'easy_ocr'}, # Name of the classifier
                {'languages': ['en']},           # Languages to be used by EasyOCR
                {'visualize_duration': 0.0167},  # Duration between visualizations (in seconds)
                {'enable_visualization': True},  # Enable visualization of OCR results
                {'grayscale_mode': False},       # Process images in grayscale mode if True
                {'downscale_ratio': 1.0}           # Ratio to downscale the image for processing　(e.g., 2 means half the original size)
            ]
        )
    ])