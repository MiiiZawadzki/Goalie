import pygame
import sys
import random
import time

clock = pygame.time.Clock()
pygame.font.init()
pygame.display.set_caption('Goalie')
programIcon = pygame.image.load('ikona.png')
pygame.display.set_icon(programIcon)
myfont = pygame.font.SysFont('calibri', 64)
myfont2 = pygame.font.SysFont('calibri', 48)
myfont3 = pygame.font.SysFont('calibri', 128)
pygame.init()
pygame.display.set_caption('Goalie')
screen = pygame.display.set_mode((800, 600))

running = True

points = 0

timer = time.time()

lvl = 1

class Cannon:
    cannon_img = pygame.image.load("cannon.png").convert()
    cannon_img.set_colorkey((255, 255, 255))


class Bullet:
    bullet_pos = [400, 120]
    bullet_color = (186, 44, 115)
    bullet_radius = 20
    bullet_rect = pygame.Rect(bullet_pos[0] - 20, bullet_pos[1] - 20, 40, 40)
    bullet_speed = 10
    bullet_reset_time = 0.1
    bullet_state = "ready"
    bullet_x = 0

    def Draw(self):
        self.bullet_rect = pygame.Rect(self.bullet_pos[0] - 20, self.bullet_pos[1] - 20, 40, 40)
        pygame.draw.circle(screen, self.bullet_color, (self.bullet_pos[0], self.bullet_pos[1]), self.bullet_radius)

    def Reset(self):
        self.bullet_pos = [400, 120]
        self.bullet_state = "ready"
        self.bullet_color = (186, 44, 115)

    def Shot(self):
        global lvl
        if self.bullet_state == "ready":
            if points == 0:
                self.bullet_x = 0
            else:
                self.bullet_x = random.randrange(-8, 8)
                if points < 20:
                    lvl = 1
                if 20 <= points < 40:
                    lvl = 2
                if 40 <= points < 60:
                    lvl = 3
                if points >= 60:
                    lvl = 4
            if lvl == 1:
                self.bullet_speed = 10
            if lvl == 2:
                self.bullet_speed = 11
            if lvl == 3:
                self.bullet_speed = 13
            if lvl == 4:
                self.bullet_speed = 15
            if player.player_rect.width == 100:
                x = random.randrange(1, 50)
                if x == 4:
                    self.bullet_color = (193, 207, 218)
                    self.bullet_x = 0
        self.bullet_state = "fire"
        self.bullet_pos[0] += self.bullet_x
        self.bullet_pos[1] += self.bullet_speed


class Player:
    player_pos = [350, 500]
    player_color = (193, 207, 218)
    player_move = 0
    player_dir = {"left": False, "right": False}
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 100, 20)
    player_boosts = {"jump": False}
    player_upgrade_timer = 0
    player_upgrade_elapse = 0

    def Upgrade(self):
        self.player_rect.width = 200

    def Reset(self):
        self.player_rect.width = 100
        player.player_upgrade_timer = 0


class Pole:
    pole_pos = [0, 0]
    pole_size = [10, 100]
    pole_color = (193, 207, 218)

    def Draw(self):
        self.pole_rect = pygame.Rect(self.pole_pos[0], self.pole_pos[1], self.pole_size[0], self.pole_size[1])
        pygame.draw.rect(screen, self.pole_color, self.pole_rect)


class Bound:
    bound_pos = [0, 0]
    bound_size = [0, 0]
    bound_color = (193, 207, 218)

    def __init__(self, pos, size):
        self.bound_pos = pos
        self.bound_size = size
        self.bound_rect = pygame.Rect(self.bound_pos[0], self.bound_pos[1], self.bound_size[0], self.bound_size[1])


def check_hits(list):
    if player.player_rect.colliderect(pole1.pole_rect):
        player.player_rect.left = pole1.pole_rect.right
    if player.player_rect.colliderect(pole2.pole_rect):
        player.player_rect.right = pole2.pole_rect.left

    if bullet.bullet_rect.colliderect(player.player_rect):
        global points, timer
        points += 1
        bullet.bullet_rect.bottom = player.player_rect.top
        if bullet.bullet_color == (193, 207, 218):
            timer = time.time()
            player.player_upgrade_timer = time.time() + 10
            player.Upgrade()
        time.sleep(bullet.bullet_reset_time)
        bullet.Reset()

    if bound_left.bound_rect.colliderect(bullet.bullet_rect):
        tmp = bullet.bullet_x
        bullet.bullet_x = 0
        bullet.bullet_pos[0] = bound_left.bound_rect.right + bullet.bullet_radius
        bullet.bullet_x = -tmp

    if bound_right.bound_rect.colliderect(bullet.bullet_rect):
        tmp = bullet.bullet_x
        bullet.bullet_x = 0
        bullet.bullet_pos[0] = bound_right.bound_rect.left - bullet.bullet_radius
        bullet.bullet_x = -tmp
    if pole1.pole_rect.colliderect(bullet.bullet_rect):
        if bullet.bullet_pos[0] <= 94:
            tmp = bullet.bullet_x
            bullet.bullet_x = 0
            bullet.bullet_pos[0] = pole1.pole_rect.left - bullet.bullet_radius
            bullet.bullet_x = -tmp
        else:
            tmp = bullet.bullet_x
            bullet.bullet_x = 0
            bullet.bullet_pos[0] = pole1.pole_rect.right + bullet.bullet_radius
            bullet.bullet_x = -tmp

    if pole2.pole_rect.colliderect(bullet.bullet_rect):
        if bullet.bullet_pos[0] <= 704:
            tmp = bullet.bullet_x
            bullet.bullet_x = 0
            bullet.bullet_pos[0] = pole2.pole_rect.left - bullet.bullet_radius
            bullet.bullet_x = -tmp
        else:
            tmp = bullet.bullet_x
            bullet.bullet_x = 0
            bullet.bullet_pos[0] = pole2.pole_rect.right + bullet.bullet_radius
            bullet.bullet_x = -tmp


def Control():
    if player.player_dir["left"]:
        player.player_move = -10
    if player.player_dir["right"]:
        player.player_move = 10
    if not player.player_dir["right"] and not player.player_dir["left"]:
        player.player_move = 0

    player.player_rect.x += player.player_move


def Check_pos():
    if bullet.bullet_rect.top > 580:
        if pole1.pole_rect.x < bullet.bullet_pos[0] < pole2.pole_rect.x:
            global points
            points -= 3
        bullet.Reset()


def Upgrades():
    global timer
    if player.player_upgrade_timer != 0:
        tmp = int((time.time() - timer))
        player.player_upgrade_elapse = tmp
    if time.time() > player.player_upgrade_timer:
        player.Reset()


cannon = Cannon()

bullet = Bullet()

player = Player()

pole1 = Pole()
pole1.pole_pos = [90, 500]
pole2 = Pole()
pole2.pole_pos = [700, 500]

bound_down = Bound([0, 599], [800, 1])
bound_up = Bound([0, 1], [800, 1])
bound_left = Bound([0, 1], [1, 600])
bound_right = Bound([799, 1], [1, 600])


def MainMenu():
    mainMenu_Click = False
    while True:
        screen.fill((45, 48, 71))

        start_button = pygame.Rect(200, 100, 400, 100)
        how_button = pygame.Rect(200, 250, 400, 100)
        quit_button = pygame.Rect(200, 400, 400, 100)

        pygame.draw.rect(screen, (193, 207, 218), start_button)
        pygame.draw.rect(screen, (193, 207, 218), how_button)
        pygame.draw.rect(screen, (193, 207, 218), quit_button)

        play = myfont.render("start game", True, (45, 48, 71))
        how = myfont.render("how to play", True, (45, 48, 71))
        quitt = myfont.render("quit", True, (45, 48, 71))

        screen.blit(play, (260, 118))
        screen.blit(how, (260, 268))
        screen.blit(quitt, (260, 418))

        mousePos = pygame.mouse.get_pos()

        if start_button.collidepoint(mousePos[0], mousePos[1]):
            if mainMenu_Click:
                Game()

        if how_button.collidepoint(mousePos[0], mousePos[1]):
            if mainMenu_Click:
                How()

        if quit_button.collidepoint(mousePos[0], mousePos[1]):
            if mainMenu_Click:
                pygame.quit()
                sys.exit(0)

        mainMenu_Click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mainMenu_Click = True
        pygame.display.update()


def How():
    font = pygame.font.SysFont('calibri', 24)
    while True:
        screen.fill((45, 48, 71))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()
        text1 = font.render("This game is about defending the goal by moving the platform.", True,
                            (193, 207, 218))
        text12 = font.render("You can control platform using left or right arrow.", True,
                            (193, 207, 218))
        text2 = font.render("Defense gives plus one point to the result, and pass gives minus three.", True,
                            (193, 207, 218))
        text3 = font.render("Upgrades:", True, (193, 207, 218))
        text4 = font.render(" - Increase platform size for 10s.", True, (193, 207, 218))
        text5 = font.render("To go back press Esc.", True, (193, 207, 218))
        screen.blit(text1, (40, 40))
        screen.blit(text12, (40, 80))
        screen.blit(text2, (40, 120))
        screen.blit(text3, (40, 170))
        screen.blit(text4, (80, 210))
        screen.blit(text5, (40, 500))
        pygame.draw.circle(screen, (255, 255, 255), (40 + 20, 160 + 60), 20)
        pygame.display.update()


def Game():
    game_time = time.time()
    running1 = True
    while running1:
        hit_elements = []
        screen.fill((45, 48, 71))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
                running1 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.player_dir["left"] = True
                if event.key == pygame.K_ESCAPE:
                    running1 = False
                if event.key == pygame.K_RIGHT:
                    player.player_dir["right"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.player_dir["left"] = False
                if event.key == pygame.K_RIGHT:
                    player.player_dir["right"] = False

        pole1.Draw()
        pole2.Draw()
        bullet.Draw()

        Control()

        pygame.draw.rect(screen, player.player_color, player.player_rect)

        pygame.draw.rect(screen, bound_down.bound_color, bound_down.bound_rect)
        pygame.draw.rect(screen, bound_up.bound_color, bound_up.bound_rect)
        pygame.draw.rect(screen, bound_left.bound_color, bound_left.bound_rect)
        pygame.draw.rect(screen, bound_right.bound_color, bound_right.bound_rect)

        Upgrades()

        points_text = myfont2.render("Points: " + str(points), True, (193, 207, 218))
        time_text = myfont2.render("Upgrade: " + str(10 - player.player_upgrade_elapse), True, (193, 207, 218))
        game_time_text = myfont2.render("Time: " + str((int(time.time() - game_time-5)))+" s", True, (193, 207, 218))
        lvl_text = myfont2.render("Lvl: " + str(lvl), True, (193, 207, 218))
        screen.blit(points_text, (10, 10))
        screen.blit(game_time_text, (10, 70))
        screen.blit(lvl_text, (10, 130))
        if player.player_upgrade_timer != 0:
            screen.blit(time_text, (550, 10))

        bullet.Shot()
        hit_elements.append(pole1.pole_rect)
        hit_elements.append(pole2.pole_rect)
        hit_elements.append(bullet.bullet_rect)
        hit_elements.append(bound_right.bound_rect)
        hit_elements.append(bound_left.bound_rect)

        check_hits(hit_elements)
        Check_pos()
        screen.blit(cannon.cannon_img, (380, 40))

        while 5 - int(time.time() - game_time) >= 0:
            screen.fill((45, 48, 71))
            x = myfont3.render(str(5 - int(time.time() - game_time)), True, (193, 207, 218))
            screen.blit(x, (400-32, 300-64))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    running1 = False
        pygame.display.update()
        clock.tick(60)


MainMenu()
