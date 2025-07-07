import pygame
import math
import sys

from mathlib import Vector3, Matrix44

class Camera:
    def __init__(self, aspect_ratio, fov, movement_speed, sensitivity):
        self.aspect_ratio = aspect_ratio
        self.fov = fov
        self.movement_speed = movement_speed
        self.sensitivity = sensitivity

        # camera vectors
        self.position = Vector3([0.0, 0.0, 0.0]) # initial position at origin
        self.look = Vector3([0.0, 0.0, -1.0]) # initially looking down the negative z-axis
        self.up = Vector3([0.0, 1.0, 0.0]) 
        
        # euler angles for camera orientation
        self.yaw = -90.0 # yaw is initialized to -90.0 degrees to look along the negative z-axis
        self.pitch = 0.0
        
    
    def get_projection_matrix(self):
        # returns the perspective projection matrix
         return Matrix44.create_perspective_projection_matrix(self.fov, self.aspect_ratio, 0.1, 100.0)
    
    def get_view_matrix(self):
        # returns the view matrix using the look-at transformation
        return Matrix44.create_look_at_matrix(self.position, self.position + self.look, self.up)
    
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        # adjusts yaw and pitch based on mouse movement
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        # constrains pitch to prevent camera flipping
        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        # updates camera vectors after yaw and pitch changes
        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front.y = math.sin(math.radians(self.pitch))
        front.z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.look = front.normalize()
        
    def move_camera(self, vector):
        # moves the camera position by a given vector scaled by movement speed
        self.position += vector * self.movement_speed

    def process_keyboard_input(self, keys):
        # handles keyboard input for camera movement and exiting the application
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # project the look vector onto the xz plane for horizontal movement
        forward_on_plane = Vector3([self.look.x, 0.0, self.look.z])
        forward = forward_on_plane.normalize()

        # calculate the right vector for strafing
        right = forward.cross(self.up)

        # determine movement direction based on key presses
        move_direction = Vector3([0.0, 0.0, 0.0])
        if keys[pygame.K_w]:
            move_direction += forward
        if keys[pygame.K_s]:
            move_direction -= forward
        if keys[pygame.K_a]:
            # negate right vector for left movement
            move_direction -= right 
        if keys[pygame.K_d]:
            move_direction += right

        # vertical movement along the world y-axis
        if keys[pygame.K_SPACE]:
            move_direction.y += 1.0
        if keys[pygame.K_LSHIFT]:
            move_direction.y -= 1.0

        # apply the calculated movement to the camera
        self.move_camera(move_direction)