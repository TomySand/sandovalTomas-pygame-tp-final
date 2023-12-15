from auxiliar import SurfaceManager as sf
import pygame as pg
import math
from audio import Audio

class Character(pg.sprite.Sprite):
    def __init__(self, screen, name, health, speed, cols_idle, cols_walk, scale_sprite, fonth_path):
        pg.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.__max_health = health
        self.__health = self.__max_health
        self.__speed = speed
        self.__idle = sf.get_surface_from_spritesheet(f'assets/mobs/{name}/idle.png', cols_idle, 1, scale=scale_sprite)
        self.__walk = sf.get_surface_from_spritesheet(f'assets/mobs/{name}/walk.png', cols_walk, 1, scale=scale_sprite)
        self.__current_animation = self.__idle
        self.__index_current_frame = 0
        self.__current_frame = self.__current_animation[self.__index_current_frame]
        self.__rect = self.__current_frame.get_rect()
        self.__dx = 0
        self.__dy = 0
        self.__frame_update_time = pg.time.get_ticks()
        self.__time_btw_frames = 85
        self.__moving = {"left": False, "right": False, "up": False, "down": False}
        self.__flip = False
        self.__is_alive = True
        self.__font = pg.font.Font(fonth_path, 10) 
        self.__name = name

    # Getters
    @property
    def get_screen(self):
        return self.__screen
    
    @property
    def get_health(self):
        return self.__health

    @property
    def get_speed(self):
        return self.__speed

    @property
    def get_idle(self):
        return self.__idle

    @property
    def get_walk(self):
        return self.__walk

    @property
    def get_current_animation(self):
        return self.__current_animation

    @property
    def get_index_current_frame(self):
        return self.__index_current_frame

    @property
    def get_current_frame(self):
        return self.__current_frame

    @property
    def get_rect(self):
        return self.__rect

    @property
    def get_dx(self):
        return self.__dx

    @property
    def get_dy(self):
        return self.__dy

    @property
    def get_frame_update_time(self):
        return self.__frame_update_time

    @property
    def get_time_btw_frames(self):
        return self.__time_btw_frames

    @property
    def get_moving_right(self):
        return self.__moving["right"]

    @property
    def get_moving_left(self):
        return self.__moving["left"]
    
    @property
    def get_moving_up(self):
        return self.__moving["up"]
    
    @property
    def get_moving_down(self):
        return self.__moving["down"]
    
    @property
    def get_flip(self):
        return self.__flip
    
    @property
    def get_is_alive(self):
        return self.__is_alive
    
    @property
    def get_font(self):
        return self.__font
    
    @property
    def get_max_health(self):
        return self.__max_health
    
    # Setters
    @get_screen.setter
    def set_screen(self, screen):
        self.__screen = screen

    @get_health.setter
    def set_health(self, health):
        self.__health = health

    @get_speed.setter
    def set_speed(self, speed):
        self.__speed = speed

    @get_idle.setter
    def set_idle(self, idle):
        self.__idle = idle

    @get_walk.setter
    def set_walk(self, walk):
        self.__walk = walk

    @get_current_animation.setter
    def set_current_animation(self, current_animation):
        self.__current_animation = current_animation

    @get_index_current_frame.setter
    def set_index_current_frame(self, index_current_frame):
        self.__index_current_frame = index_current_frame

    @get_current_frame.setter
    def set_current_frame(self, current_frame):
        self.__current_frame = current_frame

    @get_rect.setter
    def set_rect(self, rect):
        self.__rect = rect

    @get_dx.setter
    def set_dx(self, dx):
        self.__dx = dx

    @get_dy.setter
    def set_dy(self, dy):
        self.__dy = dy

    @get_frame_update_time.setter
    def set_frame_update_time(self, frame_update_time):
        self.__frame_update_time = frame_update_time

    @get_time_btw_frames.setter
    def set_time_btw_frames(self, time_btw_frames):
        self.__time_btw_frames = time_btw_frames

    @get_moving_right.setter
    def set_moving_right(self, moving):
        self.__moving["right"] = moving

    @get_moving_left.setter
    def set_moving_left(self, moving):
        self.__moving["left"] = moving
    
    @get_moving_up.setter
    def set_moving_up(self, moving):
        self.__moving["up"] = moving
    
    @get_moving_down.setter
    def set_moving_down(self, moving):
        self.__moving["down"] = moving

    @get_flip.setter
    def set_flip(self, flip):
        self.__flip = flip
    
    @get_is_alive.setter
    def set_is_alive(self, is_alive):
        self.__is_alive = is_alive
    
    @get_max_health.setter
    def get_max_health(self, max_health):
        self.__max_health = max_health
    
    def __select_animation(self):
        if all(value is False for value in self.__moving.values()):
            return self.__idle
        else:
            return self.__walk

    def do_animation(self):
        self.__current_animation = self.__select_animation()
        if pg.time.get_ticks() - self.__frame_update_time > self.__time_btw_frames:
            if self.__index_current_frame < len(self.__current_animation) -1:
                self.__index_current_frame += 1
            else:
                self.__index_current_frame = 0
            self.__frame_update_time = pg.time.get_ticks()
        self.__current_frame = self.__current_animation[self.__index_current_frame]          
        
    def move(self, obstacle_list):
        """
        Mueve al personaje.
        """
        if self.__name == "mage":
            if self.__moving["left"]:
                self.__dx = -self.__speed
            if self.__moving["right"]:
                self.__dx = self.__speed
            if self.__moving["up"]:
                self.__dy = -self.__speed
            if self.__moving["down"]:
                self.__dy = self.__speed
        
        if self.__dx != 0 and self.__dy !=0:
            self.__dx = self.__dx * (math.sqrt(2)/2)
            self.__dy = self.__dy * (math.sqrt(2)/2)
        if self.__name == "mage":
            self.__rect.centerx += self.__dx
            for tile in obstacle_list:
                if tile.rect.colliderect(self.__rect):
                    if self.__dx > 0: 
                        self.__rect.right = tile.rect.left
                    if self.__dx < 0: 
                        self.__rect.left = tile.rect.right

            self.__rect.centery += self.__dy
            for tile in obstacle_list:
                if tile.rect.colliderect(self.__rect):
                    if self.__dy > 0:
                        self.__rect.bottom = tile.rect.top
                    if self.__dy < 0: 
                        self.__rect.top = tile.rect.bottom
        else:
            self.__rect.centerx += self.__dx
            self.__rect.centery += self.__dy

    
        if self.get_dx > 0: 
            self.set_flip  = False
        elif self.get_dx < 0:
            self.set_flip = True