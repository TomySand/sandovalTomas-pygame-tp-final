import pygame as pg
class Camera():
    def __init__(self, screen, player):
        self.__screen = screen
        self.__player = player
        self.__movement = [0,0]
        self.__limitx = (200, self.__screen.get_width() - 200)
        self.__limity = (200, self.__screen.get_height() - 200)

    def update(self):
        self.__movement = [0,0]
        if self.__player.get_rect.left < self.__limitx[0]:
            self.__movement[0] = self.__limitx[0] - self.__player.get_rect.left
            self.__player.get_rect.left = self.__limitx[0]
        if self.__player.get_rect.right > self.__limitx[1]:
            self.__movement[0] = self.__limitx[1] - self.__player.get_rect.right
            self.__player.get_rect.right = self.__limitx[1]

        if self.__player.get_rect.top < self.__limity[0]:
            self.__movement[1] = self.__limity[0] - self.__player.get_rect.top
            self.__player.get_rect.top = self.__limity[0]
        if self.__player.get_rect.bottom > self.__limity[1]:
            self.__movement[1] = self.__limity[1] - self.__player.get_rect.bottom
            self.__player.get_rect.bottom = self.__limity[1]
        return self.__movement
