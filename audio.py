import pygame as pg
class Audio:
    def __init__(self, path, volume = 1, loop = 0) -> None:
        self.path = path
        self.volume = volume
        self.mixer_audio= pg.mixer.Sound(path) 
        self.loop = loop

    def play(self):
        self.mixer_audio.set_volume(self.volume)
        self.mixer_audio.play(self.loop)

    def mute(self):
        self. mixer_audio.set_volume(0)
    
    def get_volume(self):
        return self.mixer_audio.get_volume() 
    
    def set_volume(self,valor):
        if valor > 1:
            valor = 1
        self.mixer_audio.set_volume(valor)

    def control_volume(self, increase = True):
        if self.mixer_audio.get_volume() < 0.1 and self.mixer_audio.get_volume() > 0.0:
            if increase == True:
                self.volume += 0.01
            elif increase == False:
                self.volume -= 0.01
        elif self.mixer_audio.get_volume() == 0.0 and increase == True:
            self.volume += 0.01
        elif increase == False and self.mixer_audio.get_volume() == 0.1:
            self.volume -= 0.01