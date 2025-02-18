# #!/bin/bash

echo "╔══╣ Install: easyocr_ros (STARTING) ╠══╗"

cd ..
git clone -b feature/humble-devel https://github.com/TeamSOBITS/sobits_msgs.git

sudo apt update
pip install easyocr pyyaml
pip3 install opencv-python
source ~/.bashrc

echo "╚══╣ Install: easyocr_ros (FINISHED) ╠══╝"
