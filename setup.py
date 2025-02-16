from setuptools import find_packages, setup

package_name = 'easyocr_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/easy_ocr.launch.py']),  # Include the launch file
        ('share/' + package_name + '/params', ['params/config.yaml']),  # Include the config file
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ryo',
    maintainer_email='ryo@todo.todo',
    description='ROS2 package for EasyOCR integration',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'easy_ocr = src.easy_ocr:main',  # Adjusted the module path
        ],
    },
)