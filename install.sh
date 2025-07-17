# #!/bin/bash

echo "╔══╣ Install: easyocr_ros (STARTING) ╠══╗"

sudo apt update -y

sudo apt install -y ros-${ROS_DISTRO}-vision-msgs

cd ..
git clone -b humble-devel https://github.com/TeamSOBITS/sobits_msgs.git

sudo apt update
pip install easyocr pyyaml
pip3 install opencv-python
source ~/.bashrc

echo "╚══╣ Install: easyocr_ros (FINISHED) ╠══╝"
