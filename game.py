import gc
import sys, pygame, random
from sprites import Icicle, MainCharacter, Jump_Platform, Moving_Platform, \
    Bottom_Platform, Cloud_Platform, Seal
from constants import size, width, height, my_font

pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

speed = [0, 0]

platforms = pygame.sprite.Group()
trampolines = pygame.sprite.Group()

main = MainCharacter()

main_sprite = pygame.sprite.Group()
main_sprite.add(main)

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(main)

newest_platform = None
cooldown = 0

def generate_initial_platforms():
    """Generate the initial 10 platforms, plus the bottom one"""
    global newest_platform
    bottom = Bottom_Platform()
    platforms.add(bottom)
    all_sprites.add(bottom)
    for i in range(10):
        added = False
        while not added:
            new_platform = Jump_Platform(random.randint(40, width - 40),
            random.randint(55 * i, 55 * (i + 1)))
            if pygame.sprite.spritecollideany(new_platform, all_sprites) is None:
                platforms.add(new_platform)
                all_sprites.add(new_platform)
                if i == 0:
                    newest_platform = new_platform
                added = True
                if new_platform.trampoline is not None:
                    trampolines.add(new_platform.trampoline)
                    all_sprites.add(new_platform.trampoline)

def generate_random_platform():
    """Generate a random platform"""
    global newest_platform
    added = False
    while not added:
        random_int = random.randint(1, 10)
        if random_int in range(1, 8):
            new_platform = Jump_Platform(random.randint(40, width - 40),
                random.randint(newest_platform.rect.top - 100,
                newest_platform.rect.top - 10))
            if pygame.sprite.spritecollideany(new_platform, all_sprites) is None:
                added = True
        elif random_int == 8:
            new_platform = Cloud_Platform(random.randint(40, width - 40),
                random.randint(newest_platform.rect.top - 100,
                newest_platform.rect.top - 10))
            if pygame.sprite.spritecollideany(new_platform, all_sprites) is None:
                added = True
        else:
            max_left = random.randint(10, 200)
            max_right = random.randint(max_left + 120, 390)
            bottom_y = random.randint(newest_platform.rect.top - 100,
                newest_platform.rect.top - 30)
            new_platform = Moving_Platform(max_left, max_right, bottom_y)
            if pygame.sprite.spritecollideany(new_platform, all_sprites) is None:
                added = True
        if added:
            platforms.add(new_platform)
            all_sprites.add(new_platform)
            newest_platform = new_platform
            if new_platform.trampoline is not None:
                trampolines.add(new_platform.trampoline)
                all_sprites.add(new_platform.trampoline)

def generate_platforms():
    """Generate platforms if needed"""
    global newest_platform
    while len(platforms) < 11:
        generate_random_platform()
    if newest_platform.rect.top > 50:
        generate_random_platform()

def move_screen():
    """Move the screen when player gets too high"""
    main.score += round(abs(speed[1]) / 10)
    if main.score >= 100:
        try_spawn_seal()
    for entity in all_sprites:
        entity.rect.top += abs(speed[1])
        if entity.rect.top >= height:
            entity.kill()
            del entity

def try_spawn_seal():
    """Try to spawn an enemy"""
    if random.randint(1, 250) != 1:
        return
    x_center = random.randint(40, width - 40)
    y_center = random.randint(newest_platform.rect.top - 100, newest_platform.rect.top - 30)
    seal = Seal(x_center, y_center)
    if pygame.sprite.spritecollideany(seal, all_sprites) is None:
        enemies.add(seal)
        all_sprites.add(seal)

def detect_collisions():
    """Bouncing code"""
    coll = pygame.sprite.spritecollide(main, platforms, False)
    if coll:
        if main.rect.bottom <= coll[0].rect.bottom:
            if speed[1] > 0:
                speed[1] = -10
                if isinstance(coll[0], Cloud_Platform):
                    coll[0].kill()
    coll_tram = pygame.sprite.spritecollide(main, trampolines, False)
    if coll_tram:
        if main.rect.bottom <= coll_tram[0].rect.bottom:
            if speed[1] > 0:
                speed[1] = -25
                main.boosting = True

def draw_sprites():
    """Draw the sprites on the screen"""
    enemies.draw(screen)
    trampolines.draw(screen)
    platforms.draw(screen)
    bullets.draw(screen)
    main_sprite.draw(screen)

def print_score():
    """Print the player's score"""
    score_draw = my_font.render(str(main.score), 1, (0, 0, 0))
    screen.blit(score_draw, (30, 30))

def game_over():
    """Lose the game"""
    for sprite in all_sprites:
        sprite.kill()
    lose = my_font.render("Game over!", 1, (0, 0, 0))
    screen.blit(lose, (150, 200))
    pygame.display.flip()

generate_initial_platforms()

while 1:
    clock.tick(60)
    screen.fill((0, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        if speed[0] > -10:
            speed[0] -= 1.5
    if key[pygame.K_RIGHT]:
        if speed[0] < 10:
            speed[0] += 1.5
    if key[pygame.K_SPACE]:
        if cooldown <= 0:
            icicle = Icicle(main.rect.centerx, main.rect.top)
            bullets.add(icicle)
            all_sprites.add(icicle)
            cooldown = 30

    if speed[0] > 0:
        speed[0] -= 0.75
    elif speed[0] < 0:
        speed[0] += 0.75

    speed[1] += 0.3

    main.rect = main.rect.move(speed)

    if main.rect.centerx < 0:
        main.rect.center = (width - 1, main.rect.centery)
    if main.rect.centerx > width:
        main.rect.center = (1, main.rect.centery)

    detect_collisions()

    if main.rect.top < height / 3:
        move_screen()

    if speed[1] > 0:
        main.boosting = False

    generate_platforms()

    for platform in platforms:
        if isinstance(platform, Moving_Platform):
            platform.update()
    bullets.update()
    cooldown -= 1

    pygame.sprite.groupcollide(bullets, enemies, True, True)

    draw_sprites()

    print_score()

    coll_enemies = pygame.sprite.spritecollide(main, enemies, False)
    if coll_enemies:
        if not main.boosting:
            main.rect.bottom = height + 100
    if main.rect.bottom > height:
        game_over()

    pygame.display.flip()
    gc.collect()
