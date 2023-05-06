import pygame
from sys import exit
from random import randint, choice
import math
import os

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        firefly_f1 = pygame.image.load('graphics/firefly-frame-1.png')
        firefly_f1 = pygame.transform.scale2x(firefly_f1)
        firefly_f2 = pygame.image.load('graphics/firefly-frame-2.png')
        firefly_f2 = pygame.transform.scale2x(firefly_f2)
        self.firefly_animation = [firefly_f1, firefly_f2]
        self.firefly_index = 0

        self.image = self.firefly_animation[self.firefly_index]
        self.rect = pygame.Rect(250,250,45,20)
        self.gravity = 0
    
    def user_input(self):
        if self.rect.top < 0:
            self.rect.top = 0
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.rect.bottom < 650:
                self.gravity = -8

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        
    def animation(self):
        self.firefly_index += 0.1
        if self.firefly_index >= len (self.firefly_animation):
            self.firefly_index = 0
        self.image = self.firefly_animation[int(self.firefly_index)]

    def reset_firefly(self):
        if game_active == False:
            self.rect = pygame.Rect(250,250,50,25)
        
    def update(self,reset=False):
        self.user_input()
        self.apply_gravity()
        self.animation()
        if reset == True:
            self.reset_firefly()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_val, y_val):
        super().__init__()
        electric_obs_1 = pygame.image.load('graphics/obstacle/obstacle-frame-1.png')
        electric_obs_1 = pygame.transform.scale(electric_obs_1,(200,400))
        electric_obs_2 = pygame.image.load('graphics/obstacle/obstacle-frame-2.png')
        electric_obs_2 = pygame.transform.scale(electric_obs_2,(200,400))
        self.electric_obs_animation = [electric_obs_1,electric_obs_2]

        self.animation_index = 0
        self.image = self.electric_obs_animation[self.animation_index]
        self.rect = pygame.Rect(x_val,y_val,130,390)
    
    def animation_state(self):
        self.animation_index += 0.090
        if self.animation_index >= len(self.electric_obs_animation):
            self.animation_index = 0
        self.image = self.electric_obs_animation[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.remove_obs()

    def remove_obs(self):
        if self.rect.x <= -150:
            self.kill()

class Coins(pygame.sprite.Sprite):
    def __init__(self,x_val,y_val):
        super().__init__()
        self.y_val =  y_val
        sprite_sheet_image = pygame.image.load('graphics/Coins/coins.png').convert_alpha()
        coin_image = pygame.Surface((140,140),pygame.SRCALPHA)
        coin_image = sprite_sheet_image.subsurface(0,0,125,125)
        coin_image = pygame.transform.scale(coin_image,(50,50))
        coin_image.set_colorkey((0,0,0))
        self.animation_index = 0
        self.image = coin_image

        self.rect = pygame.Rect(x_val,y_val,140,140)

    def remove_obs(self):
        if self.rect.x <= -150:
            self.kill()

    def update(self):
        self.rect.y = math.sin(pygame.time.get_ticks() / 100) * 8 + self.y_val
        self.rect.x -= 5
        self.remove_obs()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'Score: {current_time}',False,('White'))
    score_rect = score_surf.get_rect(center = (500,60))
    screen.blit(score_surf,score_rect)
    return current_time

def collision_obstacle():
        if pygame.sprite.spritecollide(firefly.sprite,obstacle_group,False):
            obstacle_group.empty()
            coins.empty()
            return False
        else:
            return True
        
def collision_coin():
    if pygame.sprite.spritecollide(firefly.sprite,coins,True):
        #Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=102844">Pixabay</a>
        coin_sound = pygame.mixer.Sound('audio/coin_sound.mp3')
        coin_sound.set_volume(0.3)
        coin_sound.play()
        return True
    else:
        return False
    
def save_coin_progress():
    f = open('num_coins.txt','w')
    f.write(str(num_coins))
    f.close()

def load_coin_progress():
    f = open('num_coins.txt','r')
    num_coins = int(f.read())
    f.close()
    return num_coins

pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption('Fireflyght')
text_font = pygame.font.Font('font/Pixeltype.ttf',75)
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
high_score = 0
num_coins = 0

#background music
#credits to David Renda
bg_music = pygame.mixer.Sound('audio/bg_music/bg_music.mp3')
bg_music.set_volume(0.3)
bg_music.play(loops = -1)

#firefly rect
firefly_f1 = pygame.image.load('graphics/firefly-cover.xcf').convert_alpha()
firefly_f1 = pygame.transform.scale(firefly_f1,(700,700))
firefly_surf = firefly_f1
firefly_rect = firefly_surf.get_rect(center = (475,300))

#background
background_surf = pygame.image.load('graphics/background/PixelSky.png')
background_surf = pygame.transform.scale(background_surf,(1000,600))

#start game instructions
game_name = text_font.render('Fireflyght',False,('Black')).convert()
game_inst = text_font.render('Press space to start!',False,('Black')).convert()
game_name_rect = game_name.get_rect(center = (500,100))
game_inst_rect = game_inst.get_rect(center = (500,500))

#Groups
firefly = pygame.sprite.GroupSingle()
firefly.add(Player())

obstacle_group = pygame.sprite.Group()

coins = pygame.sprite.Group()

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,randint(1000,1300))

#coin image for coin count
sprite_sheet_image = pygame.image.load('graphics/Coins/coins.png').convert_alpha()
coin_image = pygame.Surface((140,140),pygame.SRCALPHA)
coin_image = sprite_sheet_image.subsurface(0,0,125,125)
coin_image = pygame.transform.scale(coin_image,(50,50))

coin_image_rect = coin_image.get_rect(center = (920,40))

if os.path.exists('num_coins.txt'):
    num_coins = load_coin_progress()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_coin_progress()
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and game_active == False:
            if event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer:
            x_1 = randint(1000,1050)
            y_1 = randint(-300,-100)
            y_2 = y_1 + 550

            obstacle_top = Obstacle(x_1,y_1)
            obstacle_bottom = Obstacle(x_1,y_2)

            obstacle_group.add(obstacle_top)
            obstacle_group.add(obstacle_bottom)

            y_add = randint(400,500)

            place_coin = choice(['True','False','False','False'])
            if place_coin == 'True':
                coin = Coins(x_1 + 70,y_1 + y_add)
                coins.add(coin)

    if game_active:
        if firefly.sprite.rect.bottom > 650:
            game_active = False
            firefly.sprite.reset_firefly()
            obstacle_group.empty()
            coins.empty()

        else:
            coin_message = text_font.render(f'{num_coins}',False,('White'))
            coin_message_rect = coin_message.get_rect(center = (850,49))
            screen.blit(background_surf,(0,0))

            if high_score == 0:
                high_score = score
            elif high_score < score:
                high_score = score

            firefly.update()
            firefly.draw(screen)

            obstacle_group.update()
            obstacle_group.draw(screen)

            coins.update()
            coins.draw(screen)

            score = display_score()

            if collision_coin():
                num_coins += 1

            screen.blit(coin_image,coin_image_rect)
            screen.blit(coin_message,coin_message_rect)

            game_active = collision_obstacle()
    else:
        screen.fill((94,129,162))
        screen.blit(firefly_f1,firefly_rect)

        score_message = text_font.render(f'Your score: {score}',False,('Black'))
        score_message_rect = score_message.get_rect(center = (500,525))
        high_score_message = text_font.render(f'High score: {high_score}',False,('Black'))
        high_score_message_rect = high_score_message.get_rect(center = (500,450))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_active = True
                screen.fill((94,129,162))

        if score == 0:
            coin_message = text_font.render(f'{num_coins}',False,('White'))
            coin_message_rect = coin_message.get_rect(center = (850,49))
            game_name = text_font.render('Fireflyght',False,('Black')).convert()
            game_name_rect = game_name.get_rect(center = (500,100))
            game_inst = text_font.render('Press space to start!',False,('Black')).convert()
            game_inst_rect = game_inst.get_rect(center = (500,500))
            screen.blit(coin_image,coin_image_rect)
            screen.blit(coin_message,coin_message_rect)
            
            screen.blit(game_name,game_name_rect)
            screen.blit(game_inst,game_inst_rect)
        else:
            screen.blit(game_name,game_name_rect)

            screen.blit(high_score_message,high_score_message_rect)
            screen.blit(score_message,score_message_rect)

            screen.blit(coin_image,coin_image_rect)
            screen.blit(coin_message,coin_message_rect)

    pygame.display.update()
    clock.tick(60)
        