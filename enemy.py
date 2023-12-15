import random
import pygame as pg
from character import Character
from weapons import DamageText


class Enemy(Character):
    def __init__(self, screen, name, health, speed, cols_idle, cols_walk, scale_sprite, damage_text_group, fonth_path, player):
        super().__init__(screen, name, health, speed, cols_idle, cols_walk, scale_sprite, fonth_path)
        self.get_rect.center = (300,200)
        self.damage_text_group = damage_text_group
        self.player = player
        self.attack_cooldown = 800
        self.attack_update_time = pg.time.get_ticks()
     
    # Getters
    @property
    def get_rect_center(self):
        return self.__rect.center

    @property
    def get_attack_cooldown(self):
        return self.__attack_cooldown

    @property
    def get_attack_update_time(self):
        return self.__attack_update_time

    # Setters
    @get_attack_cooldown.setter
    def set_attack_cooldown(self, attack_cooldown):
        self.__attack_cooldown = attack_cooldown

    @get_attack_update_time.setter
    def set_attack_update_time(self, attack_update_time):
        self.__attack_update_time = attack_update_time
     
    def ai(self, player, obstacle_list):
        line_collison = False
        sight_line = ((self.get_rect.centerx, self.get_rect.centery), (player.get_rect.centerx, player.get_rect.centery))
        for obstacle in obstacle_list:
            if obstacle.rect.clipline(sight_line):
                line_collison = obstacle.rect.clipline(sight_line)
                break
                
        if line_collison:
            self.set_dx = 0
            self.set_dy = 0
        else:
            if self.get_rect.centerx > player.get_rect.centerx:
                self.set_dx = -self.get_speed
            if self.get_rect.centerx < player.get_rect.centerx:
                self.set_dx = self.get_speed
            if self.get_rect.centery > player.get_rect.centery:
                self.set_dy = -self.get_speed
            if self.get_rect.centery < player.get_rect.centery:
                self.set_dy = self.get_speed

    def attack(self):
        if self.get_rect.colliderect(self.player.get_rect):
            if pg.time.get_ticks() - self.attack_update_time > self.attack_cooldown:
                daño = random.randint(1, 10)
                self.player.set_health = self.player.get_health_bar.set_remaining_health = self.player.get_health - daño
                self.attack_update_time = pg.time.get_ticks()
                          
    def got_hit(self):
        damage = random.randint(5, 20)
        self.set_health = self.get_health - damage
        if self.get_health <= 0:
            self.player.set_score = self.player.get_score + 10
            self.kill()

        damage_text = DamageText(self.get_font, self.get_rect.centerx ,self.get_rect.top, damage, "red")  
        damage_text.add(self.damage_text_group)
    
   
    def draw(self, obstacle_list, camera_movement):
        """
        Dibuja al enemigo.
        """
        self.ai(self.player,obstacle_list)
        self.move(obstacle_list)
        self.get_rect.centerx += camera_movement[0]
        self.get_rect.centery += camera_movement[1]
        self.do_animation()
        self.attack()
        flipped_frame = pg.transform.flip(self.get_current_frame, self.get_flip, False)
        self.get_screen.blit(flipped_frame, self.get_rect)
            