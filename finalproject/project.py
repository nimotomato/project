import pygame
import random
import sys
import time
from pygame.math import Vector2
import os

pygame.init()

class DRIVER:
    def __init__(self):
        """initializes bois that we need"""
        self.dog = DOG()
        self.current_level = 1
        self.bones = self.spawn_bones()
        self.number_choco = self.current_level * CHOCO_AMOUNT_MULTI
        self.chocos = self.spawn_chocos()
        self.update_speed()
        self.choco_count = 0    

    def update(self):
        """moves the dog and checks for game over or score"""
        self.dog.move_dog()
        self.collision()
        self.check_game_over()
        self.update_level()
        self.update_speed()
        self.update_choco()
        self.remove_overlap()
        
    def update_level(self):
        """updates level, used for speed"""
        self.current_level = int((len(self.dog.body) - 3) / LEVEL) + 1
        
    def update_speed(self):
        """updates speed of dog"""
        pygame.time.set_timer(MOV_TICKER, STARTING_SPEED - (self.current_level * SPEED_INCREMENT))

    def draw_window(self):
        """draws graphics"""
        self.draw_background()
        for pos, bone in self.bones.items():
            bone.draw_bone()
        self.dog.draw_dog()
        for pos, choco in self.chocos.items():
            choco.draw_choco()
        self.draw_UI()

    def collision(self):
        """checks for collision, removes object collided with and spawns a new one"""
        if tuple(self.dog.body[0]) in self.bones:
            self.bones.pop(tuple(self.dog.body[0]))
            self.dog.add_mid()
            #duplicate
            bone = BONE()
            self.bones[tuple(bone.pos)] = bone
        elif tuple(self.dog.body[0]) in self.chocos:
            #deletes choco and spawns a new one
            self.chocos.pop(tuple(self.dog.body[0]))
            choco = CHOCO()
            self.chocos[tuple(choco.pos)] = choco
            #adds point to kidney failure meter
            self.choco_count += 1
   
    def spawn_bones(self):
        """spawns bones, keeps track in dict, tuple key"""
        bones = {}
        for i in range(NUMBER_BONES):
            bone = BONE()
            bones[tuple(bone.pos)] = bone
        return bones

    def spawn_chocos(self):
        """spawns choco, keeps track in dict, tuple key"""
        chocos = {}
        for i in range(self.number_choco):
            choco = CHOCO()
            chocos[tuple(choco.pos)] = choco
        return chocos

    def update_choco(self):
        """updates number of chocos depending on level"""
        if self.number_choco < self.current_level * CHOCO_AMOUNT_MULTI:
            var = (self.current_level * CHOCO_AMOUNT_MULTI) - self.number_choco
            for i in range(var):
                choco = CHOCO()
                self.chocos[tuple(choco.pos)] = choco
            self.number_choco = self.current_level * CHOCO_AMOUNT_MULTI
            
    def check_game_over(self):
        """check for game over"""
        if not 0 <= self.dog.body[0].x < BLOCK_NUMBER or not 0 <= self.dog.body[0].y < BLOCK_NUMBER:
            self.game_over()
        if self.choco_count == 4:
            self.game_over()
        for block in self.dog.body[1:]:
            if self.dog.body[0] == block:
                self.game_over()
            
    def game_over(self):
        """terminate game"""
        end_text = end_font.render("GAME OVER!", True, WHITE)
        WIN.blit(end_text, (230, 300))
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def draw_UI(self):
        """draws score and level"""
        #score
        score = len(self.dog.body) - 3
        score_text = (f"Score: {score}")
        score_surface = font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center = (40, 45))
        WIN.blit(score_surface, score_rect)
        
        #level
        level = int((len(self.dog.body) - 3) / LEVEL) + 1
        level_text = (f"Level: {level}")
        level_surface = font.render(level_text, True, WHITE)
        level_rect = level_surface.get_rect(center = (40, 20))
        WIN.blit(level_surface, level_rect)

        #bar
        bar_text = "KIDNEY DAMAGE "
        bar_surface = font.render (bar_text, True, RED)
        bar_rect = bar_surface.get_rect(center = (700, 20))
        WIN.blit(bar_surface, bar_rect)
        self.draw_bar()

    def draw_bar(self):
        """draws bar"""
        BAR_EMPTYSRC = pygame.image.load(os.path.join(path, "bar_empty.png"))
        BAR_EMPTY = pygame.transform.scale(BAR_EMPTYSRC, (BLOCK_SIZE * 4, BLOCK_SIZE))
        BAR_1SRC = pygame.image.load(os.path.join(path, "bar_third.png"))
        BAR_1 = pygame.transform.scale(BAR_1SRC, (BLOCK_SIZE * 4, BLOCK_SIZE))
        BAR_2SRC = pygame.image.load(os.path.join(path, "bar_2third.png"))
        BAR_2 = pygame.transform.scale(BAR_2SRC, (BLOCK_SIZE * 4, BLOCK_SIZE))
        BAR_FULL_SRC = pygame.image.load(os.path.join(path, "bar_full.png"))
        BAR_FULL = pygame.transform.scale(BAR_FULL_SRC, (BLOCK_SIZE * 4, BLOCK_SIZE))
        #draw bar
        if self.choco_count == 0:
            WIN.blit(BAR_EMPTY, (620, 25))
        elif self.choco_count == 1:
            WIN.blit(BAR_1, (620, 25))
        elif self.choco_count == 2:
            WIN.blit(BAR_2, (620, 25))
        elif self.choco_count == 3:
            WIN.blit(BAR_FULL, (620, 25))

    def draw_background(self):
        """draws background"""
        WIN.fill(WHITE)
        BG = pygame.image.load(os.path.join(path, "bg.jpg")).convert_alpha()
        WIN.blit(BG, (0, 0))

    def remove_overlap(self):
        """removes overlap by deleting overlapping bone and creating a new one in a different place"""
        for key in self.bones.copy():
            if key in self.chocos:
                self.bones.pop(key)   
                bone = BONE()
                self.bones[tuple(bone.pos)] = bone


class CHOCO:
    """sets position for chocolate and also draws it"""
    def __init__(self):
        """inits random position"""
        self.set_choco_position()

    def draw_choco(self):
        """draws choco"""
        CHOCO_RECT = pygame.Rect(self.pos.x * BLOCK_SIZE, self.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        WIN.blit(CHOCO_IMG, CHOCO_RECT)

    def set_choco_position(self):
        """sets random position"""
        self.x = random.randint(0, BLOCK_NUMBER - 1)
        self.y = random.randint(0, BLOCK_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class BONE:
    """sets position for bone and also draws it"""
    def __init__(self):
        """inits random position"""
        self.set_bone_position()
        
    def draw_bone(self):
        """draws bone"""
        BONE_RECT = pygame.Rect(self.pos.x * BLOCK_SIZE, self.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        WIN.blit(BONE_IMG, BONE_RECT)

    def set_bone_position(self):
        """sets random position"""
        self.x = random.randint(0, BLOCK_NUMBER - 1)
        self.y = random.randint(0, BLOCK_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
                

class DOG:
    def __init__(self):
        """initializes body and direction using vectors because apparently they are easier to add"""
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        
        #used in adding a piece to the dog when touching bone
        self.new_mid = False       

        #checks for seeing direction of head
        self.r = True
        self.l = False
        self.u = False
        self.d = False

        #loads different versions of the images depending on orientation/direction
        #head
        self.DOG_HEAD_SRC = pygame.image.load(os.path.join(path, "d3.png")).convert_alpha()
        self.DOG_HEAD = pygame.transform.scale(self.DOG_HEAD_SRC, (BLOCK_SIZE, BLOCK_SIZE))
        self.DOG_HEAD_R = self.DOG_HEAD
        self.DOG_HEAD_L = pygame.transform.rotate(self.DOG_HEAD, 180)
        self.DOG_HEAD_U = pygame.transform.rotate(self.DOG_HEAD, 90)
        self.DOG_HEAD_D = pygame.transform.rotate(self.DOG_HEAD, 270)

        #mid section
        self.DOG_MID_SRC = pygame.image.load(os.path.join(path, "d2.png")).convert_alpha()
        self.DOG_MID_R = pygame.transform.scale(self.DOG_MID_SRC, (BLOCK_SIZE, BLOCK_SIZE))
        self.DOG_MID_L = pygame.transform.rotate(self.DOG_MID_R, 180)
        self.DOG_MID_U = pygame.transform.rotate(self.DOG_MID_R, 270)
        self.DOG_MID_D = pygame.transform.rotate(self.DOG_MID_R, 90)

        #tail section
        self.DOG_TAIL_SRC = pygame.image.load(os.path.join(path, "d1.png")).convert_alpha()
        self.DOG_TAIL_L = pygame.transform.scale(self.DOG_TAIL_SRC, (BLOCK_SIZE, BLOCK_SIZE))
        self.DOG_TAIL_R = pygame.transform.rotate(self.DOG_TAIL_L, 180)
        self.DOG_TAIL_U = pygame.transform.rotate(self.DOG_TAIL_L, 270)
        self.DOG_TAIL_D = pygame.transform.rotate(self.DOG_TAIL_L, 90)

        #curved section
        self.DOG_CURVE_SRC = pygame.image.load(os.path.join(path, "curve.png")).convert_alpha()
        self.DOG_CURVE_U = pygame.transform.scale(self.DOG_CURVE_SRC, (BLOCK_SIZE, BLOCK_SIZE))
        self.DOG_CURVE_D = pygame.transform.rotate(self.DOG_CURVE_U, 180)
        self.DOG_CURVE_L = pygame.transform.rotate(self.DOG_CURVE_U, 90)
        self.DOG_CURVE_R = pygame.transform.rotate(self.DOG_CURVE_U, 270)

    def draw_dog(self):
        #calls update tail
        self.update_tail()

        #selects what orientation to draw depending on how the coordinates relate to items next to it
        for index, block in enumerate(self.body):
            x_position = block.x * BLOCK_SIZE
            y_position = block.y * BLOCK_SIZE
            block_rect = pygame.Rect(x_position, y_position, BLOCK_SIZE, BLOCK_SIZE)
            if index == 0 and self.r == True:
                WIN.blit(self.DOG_HEAD_R, block_rect)
            elif index == 0 and self.l == True:
                WIN.blit(self.DOG_HEAD_L, block_rect)
            elif index == 0 and self.u == True:
                WIN.blit(self.DOG_HEAD_U, block_rect)
            elif index == 0 and self.d == True:
                WIN.blit(self.DOG_HEAD_D, block_rect)
            elif index == len(self.body) - 1:
                WIN.blit(self.DOG_TAIL, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    WIN.blit(self.DOG_MID_U, block_rect)
                elif previous_block.y == next_block.y:
                    WIN.blit(self.DOG_MID_L, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        WIN.blit(self.DOG_CURVE_U, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        WIN.blit(self.DOG_CURVE_L, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        WIN.blit(self.DOG_CURVE_R, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        WIN.blit(self.DOG_CURVE_D, block_rect)
                    
    def update_tail(self):
        """updates tail in relation to next last piece of the list"""
        tail_relationship = self.body[-2] - self.body[-1]
        if tail_relationship == Vector2(1, 0): self.DOG_TAIL = self.DOG_TAIL_L
        elif tail_relationship == Vector2(-1, 0): self.DOG_TAIL = self.DOG_TAIL_R
        elif tail_relationship == Vector2(0, 1): self.DOG_TAIL = self.DOG_TAIL_U
        elif tail_relationship == Vector2(0, -1): self.DOG_TAIL = self.DOG_TAIL_D

    def move_dog(self):
        """moves dog"""
        #if we have eaten a bone, new_mid is true and a mid piece is inserted
        if self.new_mid == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_mid = False
        #else just copy the body and move it one step
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_mid(self):
        #switch to see if we need to expand body
        self.new_mid = True
    
#path
path = "C:\\Users\marti\Desktop\\finalproject\images"

#colors
WHITE = (255, 255, 255)
RED = (255, 51, 51)

#fps
FPS = 60
clock = pygame.time.Clock()

#window
BLOCK_SIZE = 40
BLOCK_NUMBER = 20
HEIGHT = BLOCK_SIZE * BLOCK_NUMBER
WIDTH = BLOCK_SIZE * BLOCK_NUMBER
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#level const
LEVEL = 3

#starting speed and increment
STARTING_SPEED = 480
SPEED_INCREMENT = 30 

#bone
BONE_SRC = pygame.image.load(os.path.join(path, "bone.png")).convert_alpha()
BONE_IMG = pygame.transform.scale(BONE_SRC, (BLOCK_SIZE, BLOCK_SIZE))
NUMBER_BONES = 6

#chocolate
CHOCO_SRC = pygame.image.load(os.path.join(path, "chocolate.png")).convert_alpha()
CHOCO_IMG = pygame.transform.scale(CHOCO_SRC, (BLOCK_SIZE, BLOCK_SIZE))
CHOCO_MOVE_RATE = 5000 #ms
CHOCO_TICKER = pygame.USEREVENT
CHOCO_AMOUNT_MULTI = 8

#text initialization
font = pygame.font.SysFont(None, 24)
end_font = pygame.font.SysFont(None, 80)

#movement ticker
MOV_TICKER = pygame.USEREVENT

#initialize driver
game_driver = DRIVER()




def main():
    """main game loop"""
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOV_TICKER:
                #updates every state
                game_driver.update()
            if event.type == pygame.KEYDOWN:
                #keep track of head direction
                if event.key == pygame.K_UP and game_driver.dog.direction != Vector2(0, 1):
                    game_driver.dog.direction = Vector2(0, -1)
                    game_driver.dog.u = True
                    game_driver.dog.d = False
                    game_driver.dog.l = False
                    game_driver.dog.r = False
                if event.key == pygame.K_DOWN and game_driver.dog.direction != Vector2(0, -1):
                    game_driver.dog.direction = Vector2(0, 1)
                    game_driver.dog.d = True
                    game_driver.dog.u = False
                    game_driver.dog.l = False
                    game_driver.dog.r = False
                if event.key == pygame.K_LEFT and game_driver.dog.direction != Vector2(1, 0):
                    game_driver.dog.direction = Vector2(-1, 0)
                    game_driver.dog.l = True
                    game_driver.dog.d = False
                    game_driver.dog.u = False
                    game_driver.dog.r = False
                if event.key == pygame.K_RIGHT and game_driver.dog.direction != Vector2(-1, 0):
                    game_driver.dog.direction = Vector2(1, 0)
                    game_driver.dog.r = True
                    game_driver.dog.d = False
                    game_driver.dog.l = False
                    game_driver.dog.u = False

        #draw window
        game_driver.draw_window()
        #refresh display        
        pygame.display.update()

    #exits game
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()