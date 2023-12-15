import sys
import json
import pygame as pg
import gui
import random
from pytmx.util_pygame import load_pygame
from player import Player
from enemy import Enemy
from camera import Camera
from auxiliar import SurfaceManager as sf
from data_base import DataBase
from audio import Audio

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, sprite, group, is_obstacle):
        super().__init__(group)
        self.image = sprite
        self.is_obstacle = is_obstacle
        self.rect = self.image.get_rect(topleft=(x,y))    

    def draw(self, screen, camera_movement):
        self.rect.x += camera_movement[0]
        self.rect.y += camera_movement[1]
        screen.blit(self.image, self.rect)

class Coin(pg.sprite.Sprite):
    def __init__(self, group, scale_sprite):
        super().__init__(group)
        self.animation = sf.get_surface_from_spritesheet(f'assets/objects/coin.png', 14, 1, scale=scale_sprite)
        self.index_current_frame = 0
        self.current_frame = self.animation[self.index_current_frame]
        self.rect = self.current_frame.get_rect()
        self.frame_update_time = pg.time.get_ticks()
        self.time_btw_frames = 85
    
    def do_animation(self):
        if pg.time.get_ticks() - self.frame_update_time > self.time_btw_frames:
            if self.index_current_frame < len(self.animation) -1:
                self.index_current_frame += 1
            else:
                self.index_current_frame = 0
            self.frame_update_time = pg.time.get_ticks()
        self.current_frame = self.animation[self.index_current_frame]        
    
    def draw(self, screen, camera_movement):
        self.do_animation()
        self.rect.x += camera_movement[0]
        self.rect.y += camera_movement[1]
        screen.blit(self.current_frame, self.rect)

class Key(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pg.image.load(r'assets/objects/key.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.grabbed = False
      
    def draw(self, screen, camera_movement):
        self.rect.x += camera_movement[0]
        self.rect.y += camera_movement[1]
        screen.blit(self.image, self.rect)

class GameManager:
    def __init__(self, json_path):
        pg.init()
        pg.display.set_caption("DUTNgeon Escape")
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.font_path = r"assets/fonts/Retro Gaming.ttf"
        self.frame_rate = 60
        self.player = Player(self.screen, "mage", 100, 3.5, 6, 6, 2, self.font_path)
        self.debug = False
        self.settings = self.load_settings(json_path)
        self.level = 1
        self.map = load_pygame(f"levels/level_{self.level}.tmx")
        self.enemy_list = pg.sprite.Group()
        self.obstacle_group = pg.sprite.Group()
        self.floor_group = pg.sprite.Group()
        self.damage_text_group = pg.sprite.Group()
        self.coins_group = pg.sprite.Group()
        self.door_group = pg.sprite.Group()
        self.upper_panel = gui.UpperPanel(self.screen, self.player, self.font_path, self.settings[f"levels"][f"level_{self.level}"]["coins_number"])
        self.camera = Camera(self.screen, self.player)
        
        self.main_menu = gui.MainMenu(self.screen, self.font_path, self)
        self.pause_menu = gui.PauseMenu(self.screen, self.font_path, self)
        self.game_over_menu = gui.GameOverMenu(self.screen, self.font_path, self)
        self.key = None
        self.running = False
        self.data_base = DataBase()
        self.menu_theme = Audio(r"assets\sounds\menu_theme.wav", loop = -1)
        self.level_theme = Audio(r"assets\sounds\level_theme.wav", loop = -1)
        
    def load_settings(self, json_path) -> dict:
        with open(json_path,"r") as file:
            return json.load(file)
    
    def load_map(self):
        self.map = load_pygame(f"levels/level_{self.level}.tmx")
        self.player.set_rect.center = self.settings["levels"][f"level_{self.level}"]["player_pos"]
        for layer in self.map.visible_layers:
            for x, y, sprite in layer.tiles(): 
                x = x * 32
                y = y * 32

                if layer.is_obstacle and not layer.is_door:
                    group = self.obstacle_group
                elif layer.is_obstacle and layer.is_door:
                    group = self.door_group
                elif not layer.is_obstacle and not layer.is_door:
                    group = self.floor_group
                Tile(x, y, sprite, group, layer.is_obstacle)

    def load_enemies(self, level_number):
        available_tiles = [tile for tile in self.floor_group if not tile.is_obstacle]
        for _ in range(self.settings[f"levels"][f"level_{level_number}"]["enemies_number"]):
            if available_tiles:
                random_tile = random.choice(available_tiles)
                enemy = Enemy(self.screen, "goblin", 40, 2.3, 4 ,4, 2, self.damage_text_group, self.font_path, self.player)
                enemy.get_rect.center = random_tile.rect.center
                available_tiles.remove(random_tile)
                self.enemy_list.add(enemy)
        return available_tiles
    
    def load_coins(self, level_number, available_tiles):
        for _ in range(self.settings[f"levels"][f"level_{level_number}"]["coins_number"]):
            if available_tiles:
                random_tile = random.choice(available_tiles)
                coin = Coin(self.coins_group, 1)
                coin.rect.center = random_tile.rect.center
                available_tiles.remove(random_tile)
        return available_tiles
    
    def load_key(self, available_tiles):
        random_tile = random.choice(available_tiles)
        self.key = Key(random_tile.rect.centerx, random_tile.rect.centery)
    
    def open_door(self):
        for tile in self.door_group:
            tile.kill()
        self.level_complete()

    def level_complete(self):
        self.level += 1
        if self.level in range(1, len(self.settings["levels"]) + 1 ):
            self.run_level()
        else:
            self.level_theme.mixer_audio.stop() 
            score = self.player.get_score 
            self.player.set_score = 0
            self.game_over_menu.run(score, self.data_base)

    def reset(self):
        self.menu_theme.mixer_audio.stop() 
        self.level_theme.mixer_audio.stop() 
        self.level_theme.play() 
        self.enemy_list.empty()
        self.obstacle_group.empty()
        self.floor_group.empty()
        self.damage_text_group.empty()
        self.coins_group.empty()
        self.player.set_health = self.player.get_health_bar.set_remaining_health = self.player.get_max_health
        self.player.set_has_key = False
        self.player.set_coins = 0
        self.upper_panel.total_coins = self.settings[f"levels"][f"level_{self.level}"]["coins_number"]
            

    def draw_map(self, camera_movement):
        for tile in self.floor_group:
            tile.draw(self.screen, camera_movement)
        for tile in self.obstacle_group:
            tile.draw(self.screen, camera_movement)
        for tile in self.door_group:
            tile.draw(self.screen, camera_movement)

    def run_main_menu(self):
        self.menu_theme.play()
        self.main_menu.run()

    def run_level(self):

        """
        Ejecuta el bucle principal del juego.
        """
        
        self.reset()
        self.load_map()          
        available_tiles = self.load_enemies(self.level)
        available_tiles = self.load_coins(self.level, available_tiles)
        self.load_key(available_tiles)
        self.running = True
        while self.running:
            self.screen.fill((20,25,25))
            camera_movement = self.camera.update()
            self.draw_map(camera_movement)
            for event in pg.event.get():
                self.player.handle_keyboard_event(event)
                self.player.handle_mouse_event(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN :
                    if event.key == pg.K_ESCAPE:
                        self.pause_menu.run()
                        self.player.set_moving_down = False
                        self.player.set_moving_up = False
                        self.player.set_moving_right = False
                        self.player.set_moving_left = False
            
            #dibujar enemigos       
            for enemy in self.enemy_list:
                enemy.draw(self.obstacle_group, camera_movement)

            #dibujar monedas
            for coin in self.coins_group:
                coin.draw(self.screen, camera_movement)

            #agarrar llave
            if self.player.get_rect.colliderect(self.key.rect):
                self.player.set_has_key = True
                self.upper_panel.has_key = "YES"
                self.key.grabbed = True
            
            #abrir puerta
            if self.player.get_has_key:  
                for tile in self.door_group:
                    if self.player.get_rect.colliderect(tile.rect):
                        self.open_door()
                        break
                
            #mover texto de daño respcto a camara
            for text in self.damage_text_group:
                text.update(camera_movement)
            
            self.damage_text_group.draw(self.screen)
            self.upper_panel.draw(self.level)
            self.player.draw(self.obstacle_group, self.enemy_list, camera_movement, self.coins_group)
            if not self.key.grabbed:
                self.key.draw(self.screen, camera_movement)
            self.clock.tick(self.frame_rate)
            if self.player.get_health <= 0:
                self.level_theme.mixer_audio.stop() 
                score = self.player.get_score 
                self.player.set_score = 0
                self.game_over_menu.run(score, self.data_base)
                self.player.set_score = 0
                
            pg.display.flip()
        
 
    