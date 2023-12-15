import pygame_widgets as pw
from pygame_widgets.textbox import TextBox
import pygame as pg
import sys


class UpperPanel():
    def __init__(self, screen, player, font_path, total_coins):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = 70
        self.rect = pg.Rect(0, 0, self.width,self.height)
        self.player = player
        self.font = pg.font.Font(font_path, 12)
        self.buttons_group = pg.sprite.Group()
        self.pause_button = Button(700, self.rect.centery, 100, 30, self.font, "Pause", self.buttons_group)
        self.total_coins = total_coins

    def draw(self, level_number):
        pg.draw.rect(self.screen, (50, 50, 50), self.rect)
        pg.draw.line(self.screen, "grey", (0, self.height), (self.width, self.height))
        coins_text = self.font.render(f"Coins: {str(self.player.get_coins)} /{str(self.total_coins)} ", True, "white")
        health_text = self.font.render(f"Health", True, "white")
        if self.player.get_has_key:
            key_status = self.font.render(f"Has key?: YES", True, "white")
        else:
            key_status = self.font.render(f"Has key?: NO", True, "white")
        level_status = self.font.render(f"Level: {level_number}", True, "white")
        score_status = self.font.render(f"Score: {self.player.get_score}", True, "white")
        self.screen.blit(health_text, (28, 15))
        self.screen.blit(coins_text, (150, 32))
        self.screen.blit(key_status, (270, 32))
        self.screen.blit(level_status, (400, 32))
        self.screen.blit(score_status, (500, 32))

class HealthBar():
    def __init__(self, x, y, width, height, max_health, font):
        self.__x = x
        self.__y = y
        self.__width= width
        self.__height= height
        self.__max_health = max_health
        self.__max_health_rect = pg.Rect(self.__x, self.__y, self.__width, self.__height)
        self.__remaining_health = self.__max_health
        self.__font = font
        

    # Getters
    @property
    def get_x(self):
        return self.__x
    
    @property
    def get_y(self):
        return self.__y

    @property
    def get_width(self):
        return self.__width
    
    @property
    def get_height(self):
        return self.__height
    
    @property
    def get_max_health(self):
        return self.__max_health
    
    @property
    def get_remaining_health(self):
        return self.__remaining_health
    
    # Setters
    @get_x.setter
    def set_x(self, x):
        self.__x = x

    @get_y.setter
    def set_y(self, y):
        self.__y = y

    @get_width.setter
    def set_width(self, width):
        self.__width = width

    @get_height.setter
    def set_height(self, height):
        self.__height = height

    @get_max_health.setter
    def set_max_health(self, max_health):
        self.__max_health = max_health

    @get_remaining_health.setter
    def set_remaining_health(self, remaining_health):
        self.__remaining_health = remaining_health
    
    def draw(self, surface):
        remaining_health_perc = self.__remaining_health / self.__max_health
        pg.draw.rect(surface, "red", self.__max_health_rect)
        pg.draw.rect(surface,"green3",  (self.__x, self.__y, self.__width * remaining_health_perc , self.__height))
        health_text = self.__font.render(f"{str(self.__remaining_health)} / {str(self.__max_health)}", True, "white")
        health_text_rect = health_text.get_rect()
        health_text_rect.center = self.__max_health_rect.center
        surface.blit(health_text,health_text_rect)
        surface.blit(health_text, health_text_rect)

class Button(pg.sprite.Sprite):   
    def __init__(self, x, y, width, height, font, button_content, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.rect = pg.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.button_content = button_content
        self.font = font
        self.display = self.font.render(f"{self.button_content}", True, "white")
        self.mouse_is_hovering = False
        self.level_number = None
        
    def hover(self):
        if self.rect.collidepoint(*pg.mouse.get_pos()):
            self.display = self.font.render(f"{self.button_content}", True, "gold")
            self.mouse_is_hovering = True
        else:
            self.display = self.font.render(f"{self.button_content}", True, "white")
            self.mouse_is_hovering = False
     
    def draw(self, screen):
        self.hover()
        pg.draw.rect(screen, "darkslategray4", self.rect)
        screen.blit(self.display, self.display.get_rect(center=(self.x, self.y)))


class MainMenu():
    def __init__(self, screen, font_path, game_manager):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.button_font = pg.font.Font(font_path, 20)
        self.title_font = pg.font.Font(font_path, 40)
        self.buttons_group = pg.sprite.Group()
        self.title = self.title_font.render("dUTNgeon Explorer", True, "gold")
        self.levels_button = Button(self.screen.get_rect().centerx, 200, 150, 50, self.button_font, "Levels", self.buttons_group)
        self.settings_button = Button(self.screen.get_rect().centerx, 300, 150, 50, self.button_font, "Settings", self.buttons_group)
        self.quit_button = Button(self.screen.get_rect().centerx, 550, 150, 50, self.button_font, "Exit", self.buttons_group)
        self.levels_menu = LevelsMenu(self.screen, font_path, game_manager)
        


    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEMOTION:
                    for button in self.buttons_group:
                        button.hover()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons_group:
                        if button.mouse_is_hovering:
                            if button == self.levels_button:
                                self.levels_menu.run()
                            elif button == self.quit_button:
                                pg.quit()
                                sys.exit()
            
            self.screen.fill((20, 25, 25))
            self.screen.blit(self.title, self.title.get_rect(center=(self.screen.get_rect().centerx, 50)))
            for button in self.buttons_group:
                button.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)

class LevelsMenu:
    def __init__(self, screen, font_path, game_manager):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.button_font = pg.font.Font(font_path, 20)
        self.title_font = pg.font.Font(font_path, 40)
        self.buttons_group = pg.sprite.Group()
        self.title = self.title_font.render("Select Level", True, "gold")
        self.back_button = Button(self.screen.get_rect().centerx, 550, 100, 50, self.button_font, "Back", self.buttons_group)
        self.game_manager = game_manager
        self.level_buttons = pg.sprite.Group()

        # Agrega botones para niveles
        for level_number in range(1, len(self.game_manager.settings["levels"]) + 1):
            level_button = Button(self.screen.get_rect().centerx, 200 + (75 * (level_number - 1)), 150, 50, self.button_font, f"Level {level_number}", self.buttons_group)
            level_button.level_number = level_number
            self.level_buttons.add(level_button)

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEMOTION:
                    for button in self.buttons_group:
                        button.hover()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons_group:
                        if button.mouse_is_hovering:
                            if button == self.back_button:
                                self.game_manager.run_main_menu()
                            elif button in self.level_buttons:
                                self.game_manager.level = button.level_number
                                self.game_manager.run_level()

            self.screen.fill((20, 25, 25))
            self.screen.blit(self.title, self.title.get_rect(center=(self.screen.get_rect().centerx, 50)))
            for button in self.buttons_group:
                button.draw(self.screen)
            pg.display.flip()
            self.clock.tick(60)

class PauseMenu:
    def __init__(self, screen, font_path, game_manager):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.button_font = pg.font.Font(font_path, 20)
        self.title_font = pg.font.Font(font_path, 40)
        self.buttons_group = pg.sprite.Group()
        self.title = self.title_font.render("Pause", True, "gold")
        self.resume_button = Button(self.screen.get_rect().centerx, 450, 100, 50, self.button_font, "Resume", self.buttons_group)
        self.main_menu_button = Button(self.screen.get_rect().centerx, 550, 100, 50, self.button_font, "Main menu", self.buttons_group)
        self.game_manager = game_manager

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEMOTION:
                    for button in self.buttons_group:
                        button.hover()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons_group:
                        if button.mouse_is_hovering:
                            if button == self.resume_button:
                                running = False
                            elif button == self.main_menu_button:
                                self.game_manager.level = button.level_number
                                self.game_manager.main_menu.run()
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False


            self.screen.fill((20, 25, 25))
            self.screen.blit(self.title, self.title.get_rect(center=(self.screen.get_rect().centerx, 50)))
            for button in self.buttons_group:
                button.draw(self.screen)
            pg.display.flip()
            self.clock.tick(60)

class GameOverMenu:
    def __init__(self, screen, font_path, game_manager):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.button_font = pg.font.Font(font_path, 20)
        self.title_font = pg.font.Font(font_path, 40)
        self.buttons_group = pg.sprite.Group()
        self.title = self.title_font.render("Game Over", True, "gold")
        self.subtitle = self.button_font.render("Submit Score", True, "gold")
        self.submit_button = Button(self.screen.get_rect().centerx, 450, 100, 50, self.button_font, "Submit", self.buttons_group)
        self.textbox = TextBox(self.screen,350, self.screen.get_rect().centery, 100, 30, onSubmit=self.submit_score)
        self.ranking_menu = RankingMenu(self.screen, font_path, game_manager)
        self.score = None
        self.database = None
    

    def run(self, score, database):
        running = True
        self.score = score
        self.database = database
        score_display = self.button_font.render(f"Score: {str(self.score)}", True, "gold")
        while running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEMOTION:
                    for button in self.buttons_group:
                        button.hover()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons_group:
                        if button.mouse_is_hovering:
                            if button == self.submit_button:
                                self.submit_score()
        
                self.screen.fill((20, 25, 25))
                self.screen.blit(self.title, self.title.get_rect(center=(self.screen.get_rect().centerx, 50)))
                self.screen.blit(score_display, self.title.get_rect(center=(450, 200)))
                self.screen.blit(self.subtitle, self.title.get_rect(center=(450, 270)))

                for button in self.buttons_group:
                    button.draw(self.screen)
                
            pw.update(events)
            pg.display.flip()
            self.clock.tick(60)
    
    def submit_score(self):
        nombre = self.textbox.getText()
        self.database.insert_score(nombre, self.score)
        self.ranking_menu.run()
        
    
class RankingMenu:
    def __init__(self, screen, font_path, game_manager):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.game_manager = game_manager
        self.button_font = pg.font.Font(font_path, 20)
        self.title_font = pg.font.Font(font_path, 40)
        self.buttons_group = pg.sprite.Group()
        self.title = self.title_font.render("Ranking", True, "gold")
        self.levels_button = Button(self.screen.get_rect().centerx, 550, 100, 50, self.button_font, "Levels", self.buttons_group)
        self.levels_menu = LevelsMenu(self.screen, font_path, game_manager)
        self.name_display = self.button_font.render("Name", True, "gold")
        self.score_display = self.button_font.render("Score", True, "gold")

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEMOTION:
                    for button in self.buttons_group:
                        button.hover()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons_group:
                        if button.mouse_is_hovering:
                            if button == self.levels_button:
                                self.levels_menu.run()
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False

            self.screen.fill((20, 25, 25))
            self.screen.blit(self.title, self.title.get_rect(center=(self.screen.get_rect().centerx, 50)))
            rect_name_display = pg.draw.rect(self.screen, "darkslategray4", (100, 100, 250, 400))
            self.screen.blit(self.name_display, self.name_display.get_rect(center=(rect_name_display.centerx, rect_name_display.top + 30)))

            rect_score_display = pg.draw.rect(self.screen, "darkslategray4", (450, 100, 250, 400))
            self.screen.blit(self.score_display, self.score_display.get_rect(center=(rect_score_display.centerx, rect_score_display.top + 30)))
            for button in self.buttons_group:
                button.draw(self.screen)

            space_btw_data = 60
            initial_data_space = rect_score_display.top + 60
            for score_name_pair in self.game_manager.data_base.select_scores():
                name = self.button_font.render(f"{score_name_pair[0]}", True, "white")
                score = self.button_font.render(f"{score_name_pair[1]}", True, "white")
                self.screen.blit(name, name.get_rect(center=(rect_name_display.centerx, initial_data_space + space_btw_data)))
                self.screen.blit(score, score.get_rect(center=(rect_score_display.centerx, initial_data_space + space_btw_data)))
                initial_data_space += space_btw_data

            pg.display.flip()
            self.clock.tick(60)
    

        
