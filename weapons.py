import pygame as pg
from auxiliar import SurfaceManager as sf
import math

class Weapon():
    def __init__(self, screen, image):
        self.screen = screen
        self.angle = 0
        self.image = pg.transform.scale_by(pg.image.load(image), 1.6)
        self.rect = self.image.get_rect()
        self.pj_group = pg.sprite.Group()

    def create_pj(self):
        pj = Projectile(self.screen, r"assets\weapons\projectiles\fire_projectile.png", self.rect.centerx, self.rect.centery, self.angle, 8)
        pj.add(self.pj_group)

    def update_angle(self, player_rect):
        """
        Actualiza el angulo del arma.\n
        Args:
        - player_rect: rectangulo del jugador alrededor del cual se mueve el arma.
        """
        self.rect.center = player_rect.center
        pos = pg.mouse.get_pos()                                    
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)                        
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
  
    def draw(self, player_rect):
        """
        Dibuja el arma.\n
        Args:
        - player_rect: rectangulo del jugador alrededor del cual se dibuja el arma.
        """
        self.update_angle(player_rect)
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        weapon_posx = self.rect.centerx - self.rotated_image.get_width()/2
        weapon_posy = self.rect.centery - self.rotated_image.get_height()/2
        self.screen.blit(self.rotated_image, (weapon_posx, weapon_posy))
   
class Projectile(pg.sprite.Sprite):
    def __init__(self, screen, path_sprite_pj, x, y, angle, speed):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.sprite_pj = sf.get_surface_from_spritesheet(path_sprite_pj, 5, 1, scale =0.7)
        self.angle = angle
        self.speed = speed
        self.index_current_frame = 0
        self.current_frame = self.sprite_pj[self.index_current_frame]
        self.rect = self.current_frame.get_rect(center=(x, y))
        self.update_time = pg.time.get_ticks()
        self.time_btw_frames = 85
        self.dx = math.cos(math.radians(self.angle)) * self.speed
        self.dy =  -(math.sin(math.radians(self.angle)) * self.speed)
        
    def update(self, obstacle_list, enemy_list, camera_movement):
        self.rect.centerx += self.dx + camera_movement[0]
        self.rect.centery += self.dy + camera_movement[1]
        self.check_obstacle_collision(obstacle_list)
        self.check_enemy_collision(enemy_list)

    def check_enemy_collision(self, enemy_list):
        for enemy in enemy_list:
            if enemy.get_rect.colliderect(self.rect) and enemy.get_is_alive:
                enemy.got_hit()
                self.kill()
                break
    
    def check_obstacle_collision(self, obstacle_group):
        for obstacle in obstacle_group:
            if obstacle.rect.colliderect(self.rect):
                self.kill()
                break
                
    def do_animation(self):
        self.current_frame = pg.transform.rotate(self.sprite_pj[self.index_current_frame], self.angle)
        if pg.time.get_ticks() - self.update_time > self.time_btw_frames:
            if self.index_current_frame < len(self.sprite_pj) -1:
                self.index_current_frame += 1
            else:
                self.index_current_frame = 0
            self.update_time = pg.time.get_ticks()
        
    def draw(self, obstacle_list, enemy_list, camera_movement):
        self.update(obstacle_list, enemy_list, camera_movement)
        self.do_animation()
        self.screen.blit(self.current_frame, ((self.rect.centerx - self.current_frame.get_width()/2), self.rect.centery - self.current_frame.get_height()/2))

class DamageText(pg.sprite.Sprite):
  def __init__(self, font, x, y, damage, color):
    pg.sprite.Sprite.__init__(self)
    self.image = font.render(str(damage), True, color)
    self.rect = self.image.get_rect()
    self.rect.centerx = x
    self.rect.bottom = y
    self.time_to_kill = 500
    self.time_in_screen = pg.time.get_ticks()
    
  def update(self, camera_movement):
    self.rect.y -= 1
    self.rect.centerx += camera_movement[0]
    self.rect.centery += camera_movement[1]
    if pg.time.get_ticks() - self.time_in_screen > self.time_to_kill:
      self.kill()
      self.time_in_screen = pg.time.get_ticks()