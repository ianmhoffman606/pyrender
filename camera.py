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

        self.position = Vector3([0.0, 0.0, 0.0]) # start at origin
        self.look = Vector3([0.0, 0.0, -1.0]) # look at -Z
        self.up = Vector3([0.0, 1.0, 0.0]) 
        
        self.yaw = -90.0 
        self.pitch = 0.0
        
    
    def getProjectionMatrix(self):
         return Matrix44.create_perspective_projection_matrix(self.fov, self.aspect_ratio, 0.1, 100.0)
    
    def getViewMatrix(self):
        return Matrix44.create_look_at_matrix(self.position, self.position + self.look, self.up)
    
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front.y = math.sin(math.radians(self.pitch))
        front.z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.look = front.normalize()

    def moveCamera(self, vector):
        self.position += vector * self.movement_speed

    def process_keyboard_input(self, keys):

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # Project the look vector onto the XZ plane for horizontal movement.
        forward_on_plane = Vector3([self.look.x, 0.0, self.look.z])
        forward = forward_on_plane.normalize()

        right = forward.cross(self.up)

        move_direction = Vector3([0.0, 0.0, 0.0])
        if keys[pygame.K_w]:
            move_direction += forward
        if keys[pygame.K_s]:
            move_direction -= forward
        if keys[pygame.K_a]:
            move_direction -= right
        if keys[pygame.K_d]:
            move_direction += right

        # Vertical movement remains along the world Y-axis.
        if keys[pygame.K_SPACE]:
            move_direction.y += 1.0
        if keys[pygame.K_LSHIFT]:
            move_direction.y -= 1.0

        self.moveCamera(move_direction)