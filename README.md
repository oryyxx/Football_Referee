# Referee for football target
![gif](https://user-images.githubusercontent.com/91667636/190073399-196e78a7-a5d2-4518-9e43-3446b59eb734.gif)

Football target is a game consisting of two teams, each team has to score the ball through a goal in the center. Scoring from a further radius from the center gets more points (ie. blue = 0, green = 1, yellow = 2, red = 3).

The program uses stereocameras specifically [ZED 2 cameras](https://www.stereolabs.com/zed-2/) to act like the referee & [Yolov5x6](https://github.com/ultralytics/yolov5) for object recognition.

### Features:
- Recoginize and track objects (ie players & ball)
- Determine player's team based on shirt
- Keep track on who scored and how many points based on radius
- Display 2D map of the game

## Getting Started
In order to run the program few packages need to be downloaded.

### Hardware:
- RAM: +4 GB
- GPU: Nividia GPU (atleast 6-8gb VRAM)

### Drivers:
| Drivers  | Version | Link|
| ------------- | ------------- | ------------- |
| ZED SDK  | v3.7.7  | [link](https://www.stereolabs.com/developers/release/)  |
| CUDA  | v11.3  | [link](https://developer.nvidia.com/cuda-downloads)  |

### Python Libraries
All libraries can be found in the requirments.txt if you are using pip, you can easily the libraries by following the command:
```
pip install -r requirments.txt
```
### Installation
1. clone the repo via git
```
git clone https://github.com/sma1043/Football_Referee.git
```
2. run the program
If you you would like to run the program live use (assuming ZED camera is connected):
```
python main.py
Or, you can run on a pre recorded match (musth be svo file):
python main.py --svo (videofile).svo
```
