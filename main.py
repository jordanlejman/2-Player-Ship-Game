import pygame as pg
import os

pg.font.init()
pg.mixer.init()

WIDTH, HEIGHT = 1280, 720
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Big Time Gaming")

# *** Important Variables ***
# Frames Per Second, ship velocities
FPS = 60
VEL_P1, VEL_P2 = 7, 7

MAX_HP = 10
MAX_BULLETS = 3
VEL_BULLET = 10

HP_FONT = pg.font.Font(os.path.join('Assets', 'Azonix.otf'), 40)
WIN_FONT = pg.font.Font(os.path.join('Assets', 'Azonix.otf'), 80)

# Line to separate the players
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BORDER = pg.Rect(635, 0, 10, HEIGHT)

# Sounds
SHOOT_SOUND = pg.mixer.Sound(os.path.join('Assets', 'shoot.wav'))
HIT_SOUND = pg.mixer.Sound(os.path.join('Assets', 'hit.ogg'))

# Sprites and their sizes
BOLT_WIDTH, BOLT_HEIGHT = 80, 40

P1_SPACESHIP = pg.image.load(os.path.join('Assets', 'player1.png'))
P1_BOLT = pg.image.load(os.path.join('Assets', 'p1bolt.png'))
P1_WIDTH, P1_HEIGHT = 150, 75
P1_SPACESHIP = pg.transform.scale(P1_SPACESHIP, (P1_WIDTH, P1_HEIGHT))
P1_BOLT = pg.transform.scale(P1_BOLT, (BOLT_WIDTH, BOLT_HEIGHT))

P2_SPACESHIP = pg.image.load(os.path.join('Assets', 'player2.png'))
P2_BOLT = pg.image.load(os.path.join('Assets', 'p2bolt.png'))
P2_WIDTH, P2_HEIGHT = 100, 100
P2_SPACESHIP = pg.transform.scale(P2_SPACESHIP, (P2_WIDTH, P2_HEIGHT))
P2_BOLT = pg.transform.scale(P2_BOLT, (BOLT_WIDTH, BOLT_HEIGHT))

P1_HIT = pg.USEREVENT + 1
P2_HIT = pg.USEREVENT + 2


def draw_window(p1, p2, p1_bullets, p2_bullets,
                p1_hp, p2_hp):
    WIN.fill((0, 2, 30))
    pg.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(P1_SPACESHIP, (p1.x, p1.y))
    WIN.blit(P2_SPACESHIP, (p2.x, p2.y))

    for bullet in p1_bullets:
        WIN.blit(P1_BOLT, (bullet.x, bullet.y))
    for bullet in p2_bullets:
        WIN.blit(P2_BOLT, (bullet.x, bullet.y))

    p1_hp_text = HP_FONT.render("Health: " + str(p1_hp), 1, WHITE)
    p2_hp_text = HP_FONT.render("Health: " + str(p2_hp), 1, WHITE)
    WIN.blit(p1_hp_text, (0, 0))
    WIN.blit(p2_hp_text, (WIDTH - p2_hp_text.get_width(), 0))

    pg.display.update()


def p1_movement(keys_pressed, p1):
    if keys_pressed[pg.K_a] and p1.x - VEL_P1 > 0:  # P1 Left
        p1.x -= VEL_P1
    if keys_pressed[pg.K_d] and p1.x + VEL_P1 + p1.width < BORDER.x:  # P1 Right
        p1.x += VEL_P1
    if keys_pressed[pg.K_w] and p1.y - VEL_P1 > 0:  # P1 Up
        p1.y -= VEL_P1
    if keys_pressed[pg.K_s] and p1.y + VEL_P1 + p1.height < HEIGHT:  # P1 Down
        p1.y += VEL_P1


def p2_movement(keys_pressed, p2):
    if keys_pressed[pg.K_LEFT] and p2.x - VEL_P2 > BORDER.x + BORDER.width:  # P2 Left
        p2.x -= VEL_P2
    if keys_pressed[pg.K_RIGHT] and p2.x + VEL_P2 + p2.width < WIDTH:  # P2 Right
        p2.x += VEL_P2
    if keys_pressed[pg.K_UP] and p2.y - VEL_P2 > 0:  # P2 Up
        p2.y -= VEL_P2
    if keys_pressed[pg.K_DOWN] and p2.y + VEL_P2 + p2.height < HEIGHT:  # P2 Down
        p2.y += VEL_P2


def handle_bullets(p1_bullets, p2_bullets, p1, p2):
    for bullet in p1_bullets:
        bullet.x += VEL_BULLET
        if p2.colliderect(bullet):
            pg.event.post(pg.event.Event(P2_HIT))
            p1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            p1_bullets.remove(bullet)

    for bullet in p2_bullets:
        bullet.x -= VEL_BULLET
        if p1.colliderect(bullet):
            pg.event.post(pg.event.Event(P1_HIT))
            p2_bullets.remove(bullet)
        elif bullet.x < -BOLT_WIDTH:
            p2_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WIN_FONT.render(text, 1, RED)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pg.display.update()
    pg.time.delay(5000)


def main():
    p1 = pg.Rect(200, 315, P1_WIDTH, P1_HEIGHT)
    p2 = pg.Rect(1000, 300, P2_WIDTH, P2_HEIGHT)
    p1_hp = MAX_HP
    p2_hp = MAX_HP
    p1_bullets = []
    p2_bullets = []
    clock = pg.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and len(p1_bullets) < MAX_BULLETS:
                    bullet = pg.Rect((p1.x + p1.width), (p1.y + p1.height//2 - BOLT_HEIGHT//2), BOLT_WIDTH, BOLT_HEIGHT)
                    p1_bullets.append(bullet)
                    SHOOT_SOUND.play()
                if event.key == pg.K_RCTRL and len(p2_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(p2.x, (p2.y + p2.height//2 - BOLT_HEIGHT//2), BOLT_WIDTH, BOLT_HEIGHT)
                    p2_bullets.append(bullet)
                    SHOOT_SOUND.play()

            if event.type == P1_HIT:
                p1_hp -= 1
                HIT_SOUND.play()
            if event.type == P2_HIT:
                p2_hp -= 1
                HIT_SOUND.play()

        win_text = ""
        if p1_hp <= 0:
            win_text = "Player 2 Wins"
        if p2_hp <= 0:
            win_text = "Player 1 Wins"
        if win_text != "":
            draw_winner(win_text)
            break

        keys_pressed = pg.key.get_pressed()
        p1_movement(keys_pressed, p1)
        p2_movement(keys_pressed, p2)
        handle_bullets(p1_bullets, p2_bullets, p1, p2)

        draw_window(p1, p2, p1_bullets, p2_bullets,
                    p1_hp, p2_hp)

    main()


if __name__ == "__main__":
    main()
