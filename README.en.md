<a name="readme-top"></a>

[JA](README.md) | [EN](README.en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# EasyOCR for ROS

<!-- Table of Contents -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#introduction">Introduction</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#launch-and-usage">Launch and Usage</a></li>
    <li>
      <a href="#parameters">Parameters</a>
      <ul>
        <li><a href="#launch-parameters">Launch Parameters</a></li>
        <li><a href="#yaml-parameters">YAML Parameters</a></li>
      </ul>
    </li>
    <li><a href="#milestones">Milestones</a></li>
    <li><a href="#references">References</a></li>
  </ol>
</details>

## Introduction

This repository provides a ROS 2 package that uses EasyOCR to recognize text from images in real time.
It subscribes to an image topic, processes images with EasyOCR, and publishes recognized text along with bounding boxes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

Please describe the setup procedure for this repository here.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites


Ensure the following environment before proceeding with installation:

| System | Version                 |
| ------ | ----------------------- |
| Ubuntu | 22.04 (Jammy Jellyfish) |
| ROS    | Humble Hawksbill        |
| Python | 3.10                    |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

1. Move to your ROS 2 `src` folder:

   ```sh
   cd ~/colcon_ws/src/
   ```

2. Clone this repository:

   ```sh
   git clone -b humble-devel https://github.com/TeamSOBITS/easyocr_ros.git
   ```

3. Navigate into the repository:

   ```sh
   cd easyocr_ros/
   ```

4. Install dependencies:

   ```sh
   bash install.sh
   ```

5. Build the package:

   ```sh
   cd ~/colcon_ws/
   colcon build --symlink-install
   source ~/colcon_ws/install/setup.sh
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Launch and Usage

1. Launch your RGB camera.
2. Change the **topic_name** in [easy_ocr.launch.py](launch/easy_ocr.launch.py) to match your camera topic.
3. Run the launch file:

   ```sh
   ros2 launch easyocr_ros easy_ocr.launch.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Parameters

### Launch Parameters

The following parameters can be set in [easy_ocr.launch.py](launch/easy_ocr.launch.py):

| Parameter Name         | Description                                                                        | Default Value |
| ---------------------- | ---------------------------------------------------------------------------------- | ------------- |
| `topic_name`           | Topic name to subscribe to image data                                              | `/image_raw`  |
| `gpu`                  | Whether to use GPU for OCR processing                                              | `True`        |
| `classifier_name`      | Name of the classifier                                                             | `easy_ocr`    |
| `languages`            | Languages used by EasyOCR (supports 80+ languages)                                 | `['en']`      |
| `visualize_duration`   | Visualization interval in seconds                                                  | `0.0167`      |
| `enable_visualization` | Whether to enable OCR result visualization (may slow down processing)              | `True`        |
| `grayscale_mode`       | Whether to convert images to grayscale before processing (may improve performance) | `False`       |
| `downscale_ratio`      | Downscaling ratio (e.g., `0.5` means half-size images)                               | `0.5`           |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### YAML Parameters

The following parameters can be set in [config.yaml](params/config.yaml):

| Parameter                 | Description                                                                                       | Impact                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `decoder: greedy`         | Decoder type. Greedy selects the most likely character at each step.                              | Fast but may not yield the best result.          |
| `beamWidth: 5`            | Beam width for beam search decoder. Larger values increase accuracy but require more computation. | May improve accuracy at the cost of performance. |
| `batch_size: 1`           | Number of images processed in one batch. Larger sizes improve speed but use more memory.          | Higher throughput but more memory usage.         |
| `workers: 0`              | Number of threads used by data loader. 0 means single-threaded.                                   | More threads can speed up data loading.          |
| `allowlist: ''`           | Subset of characters to recognize. Useful for specific tasks like license plate recognition.      | Improves accuracy for limited character sets.    |
| `blocklist: ''`           | Characters to ignore. Ignored if allowlist is specified.                                          | Excludes unwanted characters.                    |
| `detail: 1`               | Output detail level. 1 is detailed, 0 is simplified.                                              | Provides more information at higher levels.      |
| `rotation_info: ''`       | Rotation angles to test for best OCR results. e.g., [90, 180, 270].                              | May improve accuracy for rotated text.           |
| `paragraph: ''`           | Whether to group results into readable paragraphs.                                                | Improves readability.                            |
| `min_size: 20`            | Minimum text box size (in pixels). Smaller boxes are filtered out.                                | Filters out noise.                               |
| `contrast_ths: 0.1`       | Threshold below which contrast is adjusted before reprocessing.                                   | Helps with low-contrast text.                    |
| `adjust_contrast: 0.5`    | Target contrast level for low-contrast text.                                                      | Improves readability.                            |
| `filter_ths: 0.003`       | Confidence threshold below which text boxes are discarded.                                        | Improves result reliability.                     |
| `text_threshold: 0.7`     | Minimum confidence for recognized text to be accepted.                                            | Improves accuracy.                               |
| `low_text: 0.4`           | Lower score threshold for text filtering.                                                         | Reduces false positives.                         |
| `link_threshold: 0.4`     | Confidence threshold for linking characters.                                                      | Improves linking accuracy.                       |
| `canvas_size: 2560`       | Maximum image size. Images are resized if larger than this.                                       | Controls memory usage.                           |
| `mag_ratio: 1.0`          | Image magnification ratio.                                                                        | May improve recognition in small text.           |
| `slope_ths: 0.1`          | Threshold for skewed text filtering.                                                              | Improves precision.                              |
| `ycenter_ths: 0.5`        | Threshold for Y-center filtering.                                                                 | Filters out misaligned text.                     |
| `height_ths: 0.5`         | Height threshold for text filtering.                                                              | Removes outliers.                                |
| `width_ths: 0.5`          | Width threshold for text filtering.                                                               | Filters out overly wide/narrow text.             |
| `y_ths: 0.5`              | Y-position threshold.                                                                             | Filters out vertical misplacements.              |
| `x_ths: 1.0`              | X-position threshold.                                                                             | Filters out horizontal misplacements.            |
| `add_margin: 0.1`         | Margin added to text boxes, as a proportion of box size.                                          | May improve recognition accuracy.                |
| `output_format: standard` | Output format. “standard” means default.                                                          | Adjusts the result format.                       |

For more details, refer to
[https://www.jaided.ai/easyocr/documentation/](https://www.jaided.ai/easyocr/documentation/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Milestones

* [ ] Implement `run_control`
* [ ] Add thresholding logic
* [ ] Add parameter to toggle drawing

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## References

* [EasyOCR](https://github.com/JaidedAI/EasyOCR)
* [easyocr_ros](https://github.com/knorth55/easyocr_ros)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/easyocr_ros/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/easyocr_ros/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/easyocr_ros/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/easyocr_ros/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[license-url]: LICENSE
