from distutils.log import debug
from html import entities
import logging
import cv2
import numpy as np
from Entities import BaseEntity, ball_pre
import pyzed.sl as sl
import logging

logging.basicConfig(level=logging.WARNING)

prevBall = ball_pre([])

id_colors = [(232, 176, 59),
            (175, 208, 25),
            (102, 205, 105),
            (185, 0, 255),
            (99, 107, 252)]

class GUI:
    def __init__(self, name):

        self.gui_name = name

        self.mapper = mapper()
        self.scoreboard = scoreboard()

        self.box_thickness = 2
    
    def update(self, image, entites):

        self.image = image

        self.mapper.updateMap(entites, self.scoreboard)
        self.scoreboard.update()

        #add images into single image..cleaner

    def display(self):

        cv2.imshow(self.gui_name + " camera", self.image)
        cv2.imshow(self.gui_name + " map", self.mapper.map)
        cv2.imshow(self.gui_name + " scoreboard", self.scoreboard.frame)
        

    def render_boxes(self, entities, img_scale, is_tracking_on):

        overlay = self.image.copy()

        for entity in entities:

            if render_object(entity, is_tracking_on):

                base_color = generate_color_id_u(entity.id)

                # Display image scaled 2D bounding box
                top_left_corner = cvt(entity.object.bounding_box_2d[0], img_scale)
                top_right_corner = cvt(entity.object.bounding_box_2d[1], img_scale)
                bottom_right_corner = cvt(entity.object.bounding_box_2d[2], img_scale)
                bottom_left_corner = cvt(entity.object.bounding_box_2d[3], img_scale)

                cv2.line(self.image, (int(top_left_corner[0]), int(top_left_corner[1])),
                     (int(top_right_corner[0]), int(top_right_corner[1])), base_color, self.box_thickness)
                cv2.line(self.image, (int(bottom_left_corner[0]), int(bottom_left_corner[1])),
                        (int(bottom_right_corner[0]), int(bottom_right_corner[1])), base_color, self.box_thickness)

                # Creation of 2 vertical lines
                draw_vertical_line(self.image, bottom_left_corner, top_left_corner, base_color, self.box_thickness)
                draw_vertical_line(self.image, bottom_right_corner, top_right_corner, base_color, self.box_thickness)

                # Scaled ROI
                roi_height = int(top_right_corner[0] - top_left_corner[0])
                roi_width = int(bottom_left_corner[1] - top_left_corner[1])
                overlay_roi = overlay[int(top_left_corner[1]):int(top_left_corner[1] + roi_width)
                , int(top_left_corner[0]):int(top_left_corner[0] + roi_height)]

                overlay_roi[:, :, :] = base_color

                # Display Object label as text
                position_image = get_image_position(entity.object.bounding_box_2d, img_scale)
                text_position = (int(position_image[0] - 20), int(position_image[1] - 12))
                text_color = (255, 255, 255, 255)
                text = str(entity.id)
                cv2.putText(self.image, text, text_position, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, text_color, 1)

                # Diplay Object distance to camera as text
                if np.isfinite(entity.object.position[2]):
                    text = str(round(abs(entity.position[2]), 1)) + "M"
                    text_position = (int(position_image[0] - 20), int(position_image[1]))
                    cv2.putText(self.image, text, text_position, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, text_color, 1)

        # Here, overlay is as the left image, but with opaque masks on each detected objects(i didnt understand the comment)
        cv2.addWeighted(self.image, 0.7, overlay, 0.3, 0.0, self.image)

class mapper:
    def __init__(self, mapSize = 512, radius = 50, goalw = 5, goalh = 10):

        self.mapSize = mapSize
        self.radius = radius
        goalx = goalw / 2
        goaly = goalh / 2

        self.map = np.zeros((self.mapSize,self.mapSize,3), np.uint8)

        self.goalStart = (int(self.map.shape[1]/2 - goalx), int(self.map.shape[0]/2 - goaly - 10))
        self.goalEnd = (int(goalx + self.map.shape[1]/2 + goalw), int(goaly + self.map.shape[0]/2 + goalh))

        self.xoffset = (self.map.shape[1] / 2) + 6
        self.yoffset = (self.map.shape[0] / 2) + 205 + 24
        self.ballplayer = 0
        self.lastHadBall = 0

    def updateMap(self, entities, scoreboard):

        scoreboard.clearPlayers()
        self.map = np.zeros((self.mapSize,self.mapSize,3), np.uint8)

        cv2.circle(self.map,(int(self.map.shape[1]/2), int(self.map.shape[0]/2)), self.radius * 4, (0,0,255), -1)
        cv2.circle(self.map,(int(self.map.shape[1]/2), int(self.map.shape[0]/2)), self.radius * 3, (0,255,255), -1)
        cv2.circle(self.map,(int(self.map.shape[1]/2), int(self.map.shape[0]/2)), self.radius * 2, (0,255,50), -1)
        cv2.circle(self.map,(int(self.map.shape[1]/2), int(self.map.shape[0]/2)), self.radius, (255,50,50), -1)
        cv2.rectangle(self.map, self.goalStart, self.goalEnd, (0,0,255), -1)

        foundBall = False
        for entity in entities:

            try:
                if BaseEntity.isPlayer(entity):
                    px = int(self.xoffset + entity.point[0] * self.radius)
                    py = int(self.yoffset + (entity.point[1] * self.radius))

                    scoreboard.addPlayer(entity)

                    cv2.circle(self.map, (px, py), 8, (128,50,50), -1)
                    cv2.putText(self.map, str(entity.id), (px + 1, py + 1), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), 1)
                elif BaseEntity.isBall(entity):
                    self.bx = int(self.xoffset + entity.point[0] * self.radius)
                    self.by = int(self.yoffset + (entity.point[1] * self.radius))

                    cv2.circle(self.map, (self.bx, self.by), 8, (255,255,255), -1)
                    foundBall = True

                    prevBall.ball_pre.append((self.bx, self.by))

                    if len(prevBall.ball_pre) > 15:
                        del prevBall.ball_pre[0]

            except Exception as e:
                 logging.error("The error raised is: ", e)

        scoreboard.ballplayer = 0

        isScore = False

        if foundBall:

            if len(prevBall.ball_pre) > 6:
                if BaseEntity.isIntersect(points=prevBall.ball_pre, start=self.goalStart, end=self.goalEnd):
                    isScore = True

            for entity in entities:

                if BaseEntity.isPlayer(entity):

                    if entity.id == self.lastHadBall and isScore:

                        distanceFromCenter = BaseEntity.absDistance(entity.point, (self.map[1] / 2, self.map[0]/2))

                        if distanceFromCenter <= self.radius * 1:
                            entity.score = 0
                        elif distanceFromCenter <= self.radius * 2:
                            entity.score = 1
                        elif distanceFromCenter <= self.radius * 3:
                            entity.score = 2
                        else:
                            entity.score = 3                        

                    px = int(self.xoffset + entity.point[0] * self.radius)
                    py = int(self.yoffset + (entity.point[1] * self.radius))

                    distanceFromball = BaseEntity.absDistance((px, py), (self.bx, self.by))

                    if distanceFromball <= 50:
                        scoreboard.ballplayer = entity.id
                        self.lastHadBall = entity.id

class scoreboard:
    def __init__(self, size = 512):

        self.size = size
        self.frame = np.zeros((self.size,self.size,3), np.uint8)
        self.players = []
        self.ballplayer = 0

    def update(self):

        self.frame = np.zeros((self.size,self.size,3), np.uint8)
        cv2.putText(self.frame, "| PLAYERS | COORDINATE | TEAM | SCORES |", (5, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255), 1)

        i = 0 
        for player in self.players:

            if player.id == self.ballplayer:
                cv2.putText(self.frame, f"| {player.id} | {player.point} | {player.team} | {player.score} |", (5, 20 + 20 * i), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 255), 1)
            else:
                cv2.putText(self.frame, f"| {player.id} | {player.point} | {player.team} | {player.score} |", (5, 20 + 20 * i), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255), 1)
            i += 1

    def addPlayer(self, player):
        self.players.append(player)

    def clearPlayers(self):
        self.players.clear()

def render_object(object_data, is_tracking_on):
    if is_tracking_on:
        return object_data.tracking_state == sl.OBJECT_TRACKING_STATE.OK
    else:
        return (object_data.tracking_state == sl.OBJECT_TRACKING_STATE.OK) or (
                    object_data.tracking_state == sl.OBJECT_TRACKING_STATE.OFF)

def generate_color_id_u(idx):
    arr = []
    if idx < 0:
        arr = [236, 184, 36, 255]
    else:
        color_idx = idx % 5
        arr = [id_colors[color_idx][0], id_colors[color_idx][1], id_colors[color_idx][2], 255]
    return arr


def draw_vertical_line(left_display, start_pt, end_pt, clr, thickness):
    n_steps = 7
    pt1 = [((n_steps - 1) * start_pt[0] + end_pt[0]) / n_steps
        , ((n_steps - 1) * start_pt[1] + end_pt[1]) / n_steps]
    pt4 = [(start_pt[0] + (n_steps - 1) * end_pt[0]) / n_steps
        , (start_pt[1] + (n_steps - 1) * end_pt[1]) / n_steps]

    cv2.line(left_display, (int(start_pt[0]), int(start_pt[1])), (int(pt1[0]), int(pt1[1])), clr, thickness)
    cv2.line(left_display, (int(pt4[0]), int(pt4[1])), (int(end_pt[0]), int(end_pt[1])), clr, thickness)

def cvt(pt, scale):
    """
    Function that scales point coordinates
    """
    out = [pt[0] * scale[0], pt[1] * scale[1]]
    return out

def get_image_position(bounding_box_image, img_scale):
    out_position = np.zeros(2)
    out_position[0] = (bounding_box_image[0][0] + (bounding_box_image[2][0] - bounding_box_image[0][0]) * 0.5) * \
                      img_scale[0]
    out_position[1] = (bounding_box_image[0][1] + (bounding_box_image[2][1] - bounding_box_image[0][1]) * 0.5) * \
                      img_scale[1]
    return out_position