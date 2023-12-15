import pygame as pg
from weapons import Weapon
from character import Character
from gui import HealthBar
import random
from audio import Audio

class Player(Character):
    def __init__(self, screen, name, health, speed, cols_idle, cols_walk, scale_sprite, fonth_path):
        super().__init__(screen, name, health, speed, cols_idle, cols_walk, scale_sprite, fonth_path)
        self.get_rect.center = (200,200)
        self.__weapon_1 = Weapon(self.get_screen, r"assets\weapons\staffs\staff_fire.png")
        self.__equipped_weapon = self.__weapon_1 
        self.__attack_cooldown = 300
        self.__attack_update_time = pg.time.get_ticks()
        self.__has_key = False
        self.__health_bar = HealthBar(15, 30, 80, 20, self.get_health, self.get_font)
        self.__coins = 0
        self.__score = 0
        self.atack_sfx = Audio("assets/sounds/atack_sound.wav", volume=0.3)
        self.coin_sfx = Audio("assets/sounds/coin_sound.wav", volume=0.3)

    # Getters
    @property
    def get_rect_center(self):
        return self.__rect.center
    
    @property
    def get_weapon_1(self):
        return self.__weapon_1

    @property
    def get_weapon_2(self):
        return self.__weapon_2
    
    @property
    def get_equipped_weapon(self):
        return self.__equipped_weapon
    @property
    def get_pj_group(self):
        return self.__pj_group

    @property
    def get_attack_cooldown(self):
        return self.__attack_cooldown

    @property
    def get_attack_update_time(self):
        return self.__attack_update_time
    
    @property
    def get_coins(self):
        return self.__coins
    
    @property
    def get_has_key(self):
        return self.__has_key

    @property
    def get_health_bar(self):
        return self.__health_bar
    
    @property
    def get_score(self):
        return self.__score

    # Setters
    @get_weapon_1.setter
    def set_weapon_1(self, weapon_1):
        self.__weapon_1 = weapon_1

    @get_equipped_weapon.setter
    def set_equipped_weapon(self, equipped_weapon):
        self.__equipped_weapon = equipped_weapon

    @get_pj_group.setter
    def set_pj_group(self, pj_group):
        self.__pj_group = pj_group

    @get_attack_cooldown.setter
    def set_attack_cooldown(self, attack_cooldown):
        self.__attack_cooldown = attack_cooldown

    @get_attack_update_time.setter
    def set_attack_update_time(self, attack_update_time):
        self.__attack_update_time = attack_update_time
    
    @get_coins.setter
    def set_coins(self, coins):
        self.__coins = coins

    @get_has_key.setter
    def set_has_key(self, has_key):
        self.__has_key = has_key

    @get_score.setter
    def set_score(self, score):
        self.__score = score

    
    def __attack(self):
        if pg.time.get_ticks() - self.__attack_update_time > self.__attack_cooldown:
            self.__equipped_weapon.create_pj()
            self.atack_sfx.play()
            self.__attack_update_time = pg.time.get_ticks()


        
    def handle_keyboard_event(self, event):
        """
        Maneja eventos de teclado y mouse relacionados al jugador.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                self.set_moving_left = True
            if event.key == pg.K_d:
                self.set_moving_right = True
            if event.key == pg.K_w:
                self.set_moving_up = True
            if event.key == pg.K_s:
               self.set_moving_down = True      
            if event.key == pg.K_r:
               daño = random.randint(1, 15)
               self.set_health = self.__health_bar.set_remaining_health = self.get_health - daño
               self.__coins += 1
               if self.get_has_key:
                   self.set_has_key = False 
               else:
                  self.set_has_key = True
                   
        if event.type == pg.KEYUP:
            if event.key == pg.K_a:
                self.set_moving_left = False
            if event.key == pg.K_d:
                self.set_moving_right = False
            if event.key == pg.K_w:
                self.set_moving_up = False
            if event.key == pg.K_s:
                self.set_moving_down = False

    def handle_mouse_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.__attack()
        #     if event.button == 3:
        #         if self.__equipped_weapon == self.__weapon_1:
        #             if self.__weapon_2:
        #                 self.__equipped_weapon(self.__weapon_2)
        #         elif self.__equipped_weapon == self.__weapon_2: 
        #             self.__equipped_weapon(self.__weapon_1)
  
    def grab_coin(self, coin_group):
        for coin in coin_group:
            if coin.rect.colliderect(self.get_rect):
                self.__score += 5
                self.__coins += 1
                self.coin_sfx.play()
                coin.kill()
                break
    
    def grab_key(self):
        self.get_has_key == True
        self.coin_sfx.play()
    
    def draw(self, obstacle_list, enemy_list, camera_movement, coin_group):
        """
        Dibuja al jugador, su arma y sus proyectiles.
        """
        self.set_dx = 0
        self.set_dy = 0
        self.move(obstacle_list)
        self.do_animation()
        self.grab_coin(coin_group)
        self.__equipped_weapon.draw(self.get_rect)
        for pj in self.__weapon_1.pj_group:
            pj.draw(obstacle_list, enemy_list, camera_movement)
        flipped_frame = pg.transform.flip(self.get_current_frame, self.get_flip, False)
        self.get_screen.blit(flipped_frame, self.get_rect)
        self.__health_bar.draw(self.get_screen)

                    
            
            
