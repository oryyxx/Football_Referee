# Referee for football target
![gif](https://user-images.githubusercontent.com/91667636/190073399-196e78a7-a5d2-4518-9e43-3446b59eb734.gif)

Football target is a game consisting of two teams, each team has to score the ball through a goal in the center. Scoring from a further radius from the center gets more points (ie. blue = 0, green = 1, yellow = 2, red = 3).

The program acts like a referee, uses stereo cameras specifically [ZED 2 cameras](https://www.stereolabs.com/zed-2/) & [Yolov5x6](https://github.com/ultralytics/yolov5) for object recognition.

### Features:
- Recoginize and track objects (ie players & ball)
- Determine player's team based on shirt
- Keep track on who scored and how many points based on radius
- Display 2D map of the game

## Getting Started
### Hardware:
- RAM: +4 GB
- GPU: nvidia GPU (atleast 6-8gb VRAM)

### Drivers:
| Drivers  | Version | Link|
| ------------- | ------------- | ------------- |
| ZED SDK  | v3.7.7  | [link](https://www.stereolabs.com/developers/release/)  |
| CUDA  | v11.3  | [link](https://developer.nvidia.com/cuda-downloads)  |

### Installation
1. clone the repo via git
```
git clone https://github.com/sma1043/Football_Referee.git
```
### Python Libraries
All libraries can be found in the requirments.txt if you are using pip, you can easily the libraries by following the command:
```
pip install -r requirments.txt
```
### Run the program
The program can run from a connected camera or via pre recorded match
```
python main.py
or,
python main.py --svo demo.svo
```
