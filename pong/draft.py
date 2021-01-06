import pygame
import sys
import math
import random

pygame.init()

clock = pygame.time.Clock()

# Setting up display window
# width
display_width = 900
display_height = 700

# colors
deep_blue = [48, 68, 99]
white = [255, 255, 255]
black = [0, 0, 0]
grey_shade = [230, 230, 230]
grey = [125, 125, 125]

center_line_top = pygame.Rect(
    (display_width/2)-10, 0, 5, (display_height/2)-20)
center_line_bottom = pygame.Rect(
    (display_width/2)-10, ((display_height/2)+20), 5, (display_height/2)+20)

top_border = pygame.Rect(1, 0, display_width-1, 2)
bottom_border = pygame.Rect(1, display_height-1, display_width-1, 2)


font = pygame.font.Font("fonts/6809 chargen.ttf", 50)


display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pong_Draft")


class Player():
    def __init__(self, name, color, font):
        self.color = color
        self.name = name
        self.score = 0
        self.score_txt = font.render(f"{self.score}", True, white)

        if self.name == "Player_1":
            self.rect = pygame.Rect(8, (display_height/2)-40, 8, 100)
        else:
            self.rect = pygame.Rect(
                display_width-16, (display_height/2)-40, 8, 100)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)
        if self.name == "Player_1":
            self.score_txt = font.render(f"{self.score}", True, white)
            display.blit(self.score_txt, (display_width/4, 30))

        else:
            self.score_txt = font.render(f"{self.score}", True, white)
            display.blit(self.score_txt,
                         (((display_width/2) + display_width/4), 30))

    def move(self, ball):
        keys = pygame.key.get_pressed()

        if self.name == "Player_1":
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.move_ip(0, -10)

            if keys[pygame.K_DOWN] and self.rect.bottom <= display_height:
                self.rect.move_ip(0, 10)

        else:
            if ball.rect.centerx > (display_width/2) and ball.velx > 0:
                if ball.rect.centerx > (display_width/2) + 100:
                    if self.rect.top > ball.rect.y and self.rect.top >= 0:
                        self.rect.move_ip(0, -12)

                    if self.rect.bottom < ball.rect.y and (self.rect.bottom) <= display_height:
                        self.rect.move_ip(0, 12)
                else:
                    if self.rect.top > ball.rect.y and self.rect.top >= 0:
                        self.rect.move_ip(0, -4)

                    if self.rect.bottom < ball.rect.y and (self.rect.bottom) <= display_height:
                        self.rect.move_ip(0, 4)

            else:
                if self.rect.top > (display_height/2) and self.rect.top >= 0 and ball.velx < 0:
                    self.rect.move_ip(0,-8)

                if self.rect.bottom < (display_height/2) and self.rect.bottom <=display_height and ball.velx < 0:
                    self.rect.move_ip(0,8)

class Ball():
    def __init__(self, color, display):
        self.color = color
        self.velx = 12
        self.vely = 0
        self.rect = pygame.Rect(50, 260, 10, 10)
        self.center = self.rect.center
        self.path = [[0, 0], [0, 0]]
        #self.mag = 4

    def draw(self, display):
        pygame.draw.ellipse(display, self.color, self.rect)

    def move(self, other1, other2, top_border, bottom_border):

        self.rect.x += self.velx
        self.rect.y += self.vely

        #centx,centy = find_center(self)
        #temp = self.path[1]
        ##self.path[0] = temp
        #self.path[1] = [centx,centy]
        global display_width

        # Check if collided with screen borders
        if self.rect.colliderect(bottom_border):
            print("Collided with bottom border")
            self.vely = -self.vely

        if self.rect.colliderect(top_border):
            self.vely = -self.vely
            print("Collided with top border")

        if self.rect.colliderect(other1) and self.velx < 0:
            print("Collided with Player 1")
            padcentx, padcenty = find_center(other1)

            if abs(self.rect.left - other1.rect.right) < 10:

                if self.rect.centery < other1.rect.centery:
                    if (self.rect.centery > other1.rect.centery-10):
                        # Found off stackexchange
                        self.velx = 10
                        self.vely = -6

                    elif (self.rect.centery > other1.rect.centery-20):
                        self.velx = 6
                        self.vely = -6

                    # add an elif statement
                    elif (self.rect.centery > other1.rect.centery - 40):
                        self.velx = 6
                        self.vely = -10
                    else:
                        self.velx = 3
                        self.vely = -9

                if self.rect.centery > other1.rect.centery:
                    if (self.rect.centery < other1.rect.centery+10):
                        self.velx = 10
                        self.vely = 6

                    elif (self.rect.centery < other1.rect.centery + 20):
                        self.velx = 6
                        self.vely = 6

                    elif (self.rect.centery < other1.rect.centery + 40):
                        self.velx = 6
                        self.vely = 10
                    else:
                        self.velx = 3
                        self.vely = 9

                if self.rect.centery == other1.rect.centery:
                    self.velx = 12
                    self.vely = 0

            if abs(self.rect.bottom - other1.rect.top) < 10 and self.vely > 0:
                print("Ball bottom hit paddle top")
                self.vely = -self.vely

            if abs(self.rect.top - other1.rect.bottom) < 10 and self.vely < 0:
                print("Ball top hit paddle bottom")
                self.vely = -self.vely

        if self.rect.colliderect(other2) and self.velx > 0:
            print("Collided with Player 2")

            if abs(self.rect.right - other2.rect.left) < 10:
                if self.rect.centery < other2.rect.centery:
                    if (self.rect.centery > other2.rect.centery-10):
                        # Found off stackexchange
                        self.velx = -10
                        self.vely = -6

                    elif (self.rect.centery > other2.rect.centery-20):
                        self.velx = -6
                        self.vely = -6

                    elif (self.rect.centery > other2.rect.centery-40):
                        self.velx = -6
                        self.vely = -10
                    else:
                        self.velx = -3
                        self.vely = -9

                if self.rect.centery > other2.rect.centery:
                    if (self.rect.centery < other2.rect.centery+10):
                        self.velx = -10
                        self.vely = 6

                    elif (self.rect.centery < other2.rect.centery + 20):
                        self.velx = -6
                        self.vely = 6

                    elif(self.rect.centery < other2.rect.centery + 40):
                        self.velx = -6
                        self.vely = 10
                    else:
                        self.velx = -3
                        self.vely = 9

                if self.rect.centery == other2.rect.centery:
                    self.velx = -12
                    self.vely = 0

            if abs(self.rect.bottom - other2.rect.top) < 10 and self.vely > 0:
                self.vely = -self.vely

            if abs(self.rect.top - other2.rect.bottom) < 10 and self.vely < 0:
                self.vely = -self.vely

        if self.rect.left <= 0:
            other2.score += 1
            self.rect.center = self.center
            self.velx = 12
            self.vely = 0

        if self.rect.right >= display_width:
            other1.score += 1
            self.rect.center = self.center
            self.velx = 12
            self.vely = 0


def find_center(other):
    center_x, center_y = ((other.rect.left + other.rect.left + other.rect.width)/2,
                          (other.rect.top + other.rect.top + other.rect.height)/2)
    # Need center of paddle SURFACE
    center_x = center_x + (other.rect.width/2)
    return (center_x, center_y)


def find_grad(path):
    y = path[1][1]-path[0][1]
    x = path[1][0]-path[0][0]
    grad = y/x
    return grad


player = Player("Player_1", grey_shade, font)
player_2 = Player("Player_2", grey_shade, font)
pong = Ball(white, display)
# player.init(display)
pong.draw(display)


def game(display):
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display.fill(black)

        # move player
        player.move(pong)
        player_2.move(pong)
        # pong.move(display,player,player_2)

        pong.move(player, player_2, top_border, bottom_border)
        # Update display after player movement
        player.draw(display)
        player_2.draw(display)
        pong.draw(display)
        #Draw center lines
        pygame.draw.rect(display, white, center_line_top)
        pygame.draw.rect(display, white, center_line_bottom)

        # Draw borders
        pygame.draw.rect(display, white, bottom_border)
        pygame.draw.rect(display, white, top_border)

        # Update window display
        pygame.display.flip()
        clock.tick(60)

def menu(display):
    against_cpu = pygame.Rect((display_width/2) -100,display_height/2,300,100)
    ai_against_cpu = pygame.Rect((display_width/2) -100,(display_height/2)-130,300,100)
    while True:
        
        display.fill(black)
        
        menu_name = font.render("Pong draft",True,white)
        display.blit(menu_name,(display_width/2 -100,30))
        mx, my = pygame.mouse.get_pos()
        if against_cpu.collidepoint((mx, my)):
            if click:
                game(display)

        if ai_against_cpu.collidepoint((mx, my)):
            if click:
                game(display)

        #A menu where you decide whether to play against cpu or ai against cpu
        
        pygame.draw.rect(display,white,against_cpu)
        pygame.draw.rect(display,white,ai_against_cpu)

        display.blit(font.render('P1 vs Cpu',True,black),(display_width/2 - 70,display_height/2 + 25))
        display.blit(font.render(' AI vs Cpu',True,black),((display_width/2) - 70,(display_height/2) - 105))
        pygame.display.flip()
        
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True



menu(display)




