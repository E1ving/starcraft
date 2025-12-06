import pygame
import sys
import traceback
import supply
import bullet
import enemy
import myplane

from pygame.locals import *
import random


pygame.init()
pygame.mixer.init()

bg_size = width, height = 512, 768 # 背景尺寸
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("星际争霸 ver1.1.4")

# background = pygame.image.load("images/background.png").convert()
background_base = [pygame.image.load("images/background1.png"),\
              pygame.image.load("images/background2.png"),\
              pygame.image.load("images/background3.png"),\
              pygame.image.load("images/background4.png"),\
              pygame.image.load("images/background5.png")]
background = background_base[0].convert()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (195,200,201)
WHITE = (255, 255, 255)
BLUE = (47, 94, 148)
DARK_RED = (100, 1, 13)
YELLOW = (154, 98, 3)

# 载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
slow_sound = pygame.mixer.Sound("sound/get_slow.wav")  # 新增减速音效
me_down_sound.set_volume(0.2)

# 用于添加敌机的函数
def add_small_enemies(group1 ,group2 ,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
def add_mid_enemies(group1 ,group2 ,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)
def add_big_enemies(group1 ,group2 ,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

# 升级增加敌机速度
def inc_speed(target,inc):
    for each in target:
        each.speed = each.speed + inc

# 升级增加敌机子弹速度
def inc_bullet_speed(target,inc):
    for each in target:
        each.speed = each.speed + inc

#  升级增加敌机子弹伤害
def inc_bullet_hurt(target,inc):
    for each in target:
        each.hurt = each.hurt + inc

def main(mode):
    global background
    # 播放主游戏BGM
    pygame.mixer.music.load("sound/gaming.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer_music.play(-1) # 背景音乐循环播放（如有其他音乐可注释此行）

   # 玩家飞机列表和子弹池初始化
    if mode == 1:
        me_list = [myplane.MyPlane(bg_size, init_pos=(width // 2, height - 100))]
    else:
        me_list = [
            myplane.MyPlane(bg_size, init_pos=(width // 4, height - 100)),
            myplane.MyPlane(bg_size, init_pos=(width * 3 // 4, height - 100))
        ]
    me_group = pygame.sprite.Group(me_list)

    # 为每个玩家分配独立的子弹池和索引
    BULLET1_NUM = 6
    BULLET2_NUM = 12
    bullets1 = []
    bullets2 = []
    bullet1_indices = []
    bullet2_indices = []
    for me in me_list:
        bullets1.append([bullet.Bullet1(me.rect.midtop) for _ in range(BULLET1_NUM)])
        bullets2.append([bullet.Bullet2(me.rect.midtop) for _ in range(BULLET2_NUM)])
        bullet1_indices.append(0)
        bullet2_indices.append(0)

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 暂停游戏标志
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    # 游戏难度
    level = 1

    # 生命条数
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/Jersey10-Regular.ttf", 54)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # 存档判断
    recorded = False


    # 全屏炸弹
    bomb_image = pygame.image.load("images/bomb_supply.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/Jersey10-Regular.ttf", 40)
    bomb_num_max = 3
    bomb_num = 1

    # 子弹补给储存
    bullet_supply_num_max = 3
    bullet_supply_num = 1

    # 记录原始速度用于减速恢复
    original_enemy_speeds = {}
    original_enemy_bullet_speeds = {}

    # 每20s发放一次补给
    bullet_supply = supply.Bullet_supply(bg_size)
    bomb_supply = supply.Bomb_supply(bg_size)
    slow_supply = supply.Slow_supply(bg_size)  # 新增减速补给

    SUPPLY_TIME = USEREVENT

    # 缩小炸弹和子弹补给图片用于UI显示
    bomb_icon = pygame.transform.scale(bomb_image, (bomb_rect.width // 2, bomb_rect.height // 2))
    bullet_supply_icon = pygame.transform.scale(bullet_supply.image, (bullet_supply.image.get_width() // 2,
                                                                      bullet_supply.image.get_height() // 2))
    icon_margin = 10

    # 补给计时器
    pygame.time.set_timer(SUPPLY_TIME, 20 * 1000)

    # 增益计时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    # 重生无敌计时器
    INVINCIBLE_TIME = USEREVENT + 2

    # 减速效果计时器
    SLOW_TIME = USEREVENT + 3  # 新增减速计时器

    # 减速效果标志
    is_slow = False  # 新增减速标志
    slow_end_time = 0  # 新增，记录减速结束时间

    # 标志是否使用增益子弹
    is_double_bullet = False

    # 统计得分
    score = 0
    score_font = pygame.font.Font("font/Jersey10-Regular.ttf", 40)

    enemies = pygame.sprite.Group() # 敌机组，包含所有敌机


    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15) # 实例化小型机

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 6) # 实例化中型机

    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 3) # 实例化大型机



    # 敌机子弹
    e_bullets = []

    # 生成敌机子弹
    e_bullet1 = []
    e_bullet1_index = 0
    E_BULLET1_NUM = 12
    for i in range(BULLET1_NUM):
        for s_e in small_enemies:
            e_bullet1.append(bullet.Enemy_Bullet1(s_e.rect.midtop))

    e_bullet2 = []
    e_bullet2_index = 0
    E_BULLET2_NUM = 8
    for i in range(BULLET2_NUM):
        for s_e in mid_enemies:
            e_bullet2.append(bullet.Enemy_Bullet2(s_e.rect.midtop))

    clock = pygame.time.Clock()

    switch_image = True # 用于切换图片
    # 实现尾部喷气效果
    delay = 100
    running = True


    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            # 重绘暂停键（暂停与开始键绘制重叠问题需解决）
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                        # pygame.draw.rect(screen, GRAY, (410, 10, 50, 50)) # 画面美化（针对原背景background）
                    else:
                        paused_image = pause_pressed_image
                        # pygame.draw.rect(screen, GRAY, (410, 10, 50, 50))
                else:
                    if paused:
                        paused_image = resume_nor_image
                        # pygame.draw.rect(screen, GRAY, (410, 10, 50, 50))
                    else:
                        paused_image = pause_nor_image
                        # pygame.draw.rect(screen, GRAY, (410, 10, 50, 50))
            # 是否按下暂停检测
            elif event.type == KEYDOWN:
                # 玩家1道具键
                if event.key == K_y:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
                if event.key == K_u:
                    if bullet_supply_num > 0 and not is_double_bullet:
                        bullet_supply_num -= 1
                        is_double_bullet = True
                        pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                # 玩家2道具键
                if event.key == K_k:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
                if event.key == K_l:
                    if bullet_supply_num > 0 and not is_double_bullet:
                        bullet_supply_num -= 1
                        is_double_bullet = True
                        pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)

            elif event.type == SUPPLY_TIME:
                supply_sound.play()

                choice = random.randint(1, 4)
                if choice == 1:
                    bullet_supply.reset()
                elif choice == 2:
                    bomb_supply.reset()
                else:  # 3和4都为减速补给
                    slow_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

            # 减速效果结束
            elif event.type == SLOW_TIME:
                is_slow = False
                slow_end_time = 0  # 清零
                # 恢复敌机和敌人子弹速度
                for e in enemies:
                    if id(e) in original_enemy_speeds:
                        e.speed = original_enemy_speeds[id(e)]
                for eb in e_bullet1 + e_bullet2:
                    if id(eb) in original_enemy_bullet_speeds:
                        eb.speed = original_enemy_bullet_speeds[id(eb)]
                original_enemy_speeds.clear()
                original_enemy_bullet_speeds.clear()
                pygame.time.set_timer(SLOW_TIME, 0)

        ############## 升级点：辅以黑屏过场 ##############
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 2)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 1)
            # 提升敌机速度
            inc_speed(small_enemies,0.5)
            # 提升子弹速度
            inc_bullet_speed(e_bullet1, 1)
            # 提升子弹伤害
            inc_bullet_hurt(e_bullet1, 0.5)
            inc_bullet_hurt(e_bullet2, 0.5)
            # 背景重绘
            background = background_base[1]

        if level == 2 and score > 200000:
            level = 3
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 2)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            # 提升敌机速度
            inc_speed(small_enemies,0.5)
            inc_speed(mid_enemies,0.3)
            # 提升子弹速度
            inc_bullet_speed(e_bullet1, 0.5)
            inc_bullet_speed(e_bullet2, 1)
            # 提升子弹伤害
            inc_bullet_hurt(e_bullet1, 0.5)
            inc_bullet_hurt(e_bullet2, 0.5)
            # 背景重绘
            background = background_base[2]

        if level == 3 and score > 400000:
            level = 4
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 1)
            add_mid_enemies(mid_enemies, enemies, 1)
            add_big_enemies(big_enemies, enemies, 1)
            # 提升敌机速度
            inc_speed(small_enemies,0.5)
            inc_speed(mid_enemies,0.3)
            inc_speed(big_enemies,0.2)
            # 提升子弹速度
            inc_bullet_speed(e_bullet1,0.5)
            inc_bullet_speed(e_bullet2,0.5)
            # 提升子弹伤害
            inc_bullet_hurt(e_bullet1, 0.5)
            inc_bullet_hurt(e_bullet2, 0.5)
            # 背景重绘
            background = background_base[3]

        if level == 4 and score > 800000:
            level = 5
            upgrade_sound.play()
            ############# Boss关制作（待编写）#############
            background = background_base[4]

        if life_num and not paused:
            # 飞机移动控制
            key_pressed = pygame.key.get_pressed()
            for idx, me in enumerate(me_group):
                if idx == 0:
                    # 玩家1使用WASD
                    if key_pressed[K_w]:
                        me.moveUp()
                    if key_pressed[K_s]:
                        me.moveDown()
                    if key_pressed[K_a]:
                        me.moveLeft()
                    if key_pressed[K_d]:
                        me.moveRight()
                elif idx == 1:
                    # 玩家2使用方向键
                    if key_pressed[K_UP]:
                        me.moveUp()
                    if key_pressed[K_DOWN]:
                        me.moveDown()
                    if key_pressed[K_LEFT]:
                        me.moveLeft()
                    if key_pressed[K_RIGHT]:
                        me.moveRight()

            screen.blit(background, (0, 0))  # 背景绘制
            # 绘制炸弹补给，检查是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                for me in me_group:
                    if pygame.sprite.collide_mask(bomb_supply, me):
                        get_bomb_sound.play()
                        if bomb_num < bomb_num_max:
                            bomb_num += 1
                        bomb_supply.active = False
                        break

            # 绘制子弹补给，检查是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                for me in me_group:
                    if pygame.sprite.collide_mask(bullet_supply, me):
                        get_bullet_sound.play()
                        if bullet_supply_num < bullet_supply_num_max:
                            bullet_supply_num += 1
                        bullet_supply.active = False
                        break

            # 绘制减速补给，检查是否获得
            if slow_supply.active:
                slow_supply.move()
                screen.blit(slow_supply.image, slow_supply.rect)
                for me in me_group:
                    if pygame.sprite.collide_mask(slow_supply, me):
                        slow_sound.play()
                        # 记录原始速度并减半
                        for e in enemies:
                            if e.active:
                                original_enemy_speeds[id(e)] = e.speed
                                e.speed = max(0.5, e.speed * 0.5)
                        for eb in e_bullet1 + e_bullet2:
                            if eb.active:
                                original_enemy_bullet_speeds[id(eb)] = eb.speed
                                eb.speed = max(1, eb.speed * 0.5)
                        is_slow = True
                        slow_end_time = pygame.time.get_ticks() + 10000  # 10秒后结束
                        pygame.time.set_timer(SLOW_TIME, 10 * 1000)  # 10秒减速效果
                        slow_supply.active = False
                        break

           # 我方飞机发射子弹
            if not (delay % 10):
                bullet_sound.play()
                for idx, me in enumerate(me_list):
                    if is_double_bullet:
                        i = bullet2_indices[idx]
                        left_pos = (me.rect.centerx - 33, me.rect.top - 4)
                        right_pos = (me.rect.centerx + 8, me.rect.top - 4)
                        bullets2[idx][i].reset(left_pos)
                        bullets2[idx][(i + 1) % BULLET2_NUM].reset(right_pos)
                        bullet2_indices[idx] = (i + 2) % BULLET2_NUM
                    else:
                        i = bullet1_indices[idx]
                        bullets1[idx][i].reset((me.rect.centerx - 11, me.rect.top - 20))
                        bullet1_indices[idx] = (i + 1) % BULLET1_NUM

            # 敌机子弹实例化
            if not (delay % 100):
                e_bullets.append(e_bullet1)
                for s_e in small_enemies:
                    if s_e.active and s_e.rect.bottom > 0:
                        e_bullet1[e_bullet1_index].reset((s_e.rect.centerx - 9, s_e.rect.bottom - 3))
                        e_bullet1_index = (e_bullet1_index + 1) % E_BULLET1_NUM
                e_bullets.append(e_bullet2)
                for s_e in mid_enemies:
                    if s_e.active and s_e.rect.bottom > 0:
                        e_bullet2[e_bullet2_index].reset((s_e.rect.centerx - 9, s_e.rect.bottom - 3))
                        e_bullet2_index = (e_bullet2_index + 1) % E_BULLET2_NUM

           # 检测所有玩家的子弹是否击中敌机
            for idx in range(len(me_list)):
                for b in bullets1[idx] + bullets2[idx]:
                    if b.active:
                        b.move()
                        screen.blit(b.image, b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                        if enemy_hit:
                            b.active = False
                            for e in enemy_hit:
                                if e in mid_enemies or e in big_enemies:
                                    e.hit = True
                                    e.energy -= 1
                                    if e.energy == 0:
                                        e.active = False
                                elif e in small_enemies:
                                    e.active = False
            # 检测子弹是否击中我方飞机
            for eb in e_bullet1:
                if eb.active:
                    eb.move()
                    screen.blit(eb.image,eb.rect)
                    me_hit = pygame.sprite.spritecollide(eb, me_group, False, pygame.sprite.collide_mask)
                    for me in me_hit:
                        eb.active = False
                        if not me.invincible:
                            me.energy -= eb.hurt
                            if me.energy <= 0:
                                me.active = False

            for eb in e_bullet2:
                if eb.active:
                    eb.move()
                    screen.blit(eb.image,eb.rect)
                    me_hit = pygame.sprite.spritecollide(eb, me_group, False, pygame.sprite.collide_mask)
                    for me in me_hit:
                        eb.active = False
                        if not me.invincible:
                            me.energy -= eb.hurt
                            if me.energy <= 0:
                                me.active = False


           # 绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), \
                                     2)
                    # 出现音效
                    if each.rect.bottom > -50:
                        enemy3_fly_sound.play(-1)
                else:
                    # 敌机被摧毁
                    screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            score += 10000
                            enemy3_down_sound.stop()
                            each.reset()

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)
                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), \
                                                    (each.rect.right, each.rect.top - 5), \
                                                    2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5), \
                                                           (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), \
                                                           2)
                else:
                    # 敌机被摧毁
                    screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()
            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 敌机被摧毁
                    screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 检测我方飞机是否被撞
            for me in me_group:
                enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
                if enemies_down:
                    if not me.invincible:
                        me.active = False
                    for e in enemies_down:
                        e.active = False

            # 绘制我方飞机
            for idx, me in enumerate(me_group):
                if me.active:
                    if level == 1 or level == 3 or level == 4:
                        # 玩家1用me.images[0]，玩家2用me.images[1]
                        img = me.images[min(idx, 1)]
                        rect = img.get_rect(center=me.rect.center)
                        screen.blit(img, rect)
                    elif level == 2:
                        img = me.night_images[min(idx, 1)]
                        rect = img.get_rect(center=me.rect.center)
                        screen.blit(img, rect)
                    elif level == 5:
                        img = me.ex_images[min(idx, 1)]
                        rect = img.get_rect(center=me.rect.center)
                        screen.blit(img, rect)
                else:
                    rect = me.destroy_images[me_destroy_index].get_rect(center=me.rect.center)
                    screen.blit(me.destroy_images[me_destroy_index], rect)
                    if not (delay % 3):
                        if me_destroy_index == 0:
                            me_down_sound.play()
                        me_destroy_index = (me_destroy_index + 1) % 4
                        if me_destroy_index == 0:
                            life_num -= 1
                            me.reset()
                            pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # 绘制每个玩家的血槽
            for me in me_group:
                pygame.draw.line(screen, BLACK, (me.rect.left, me.rect.bottom + 5),
                                 (me.rect.right, me.rect.bottom + 5), 2)
                energy_remain = me.energy / myplane.MyPlane.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen, energy_color, (me.rect.left, me.rect.bottom + 5),
                                 (me.rect.left + me.rect.width * energy_remain, me.rect.bottom + 5), 2)

            # 绘制剩余生命条数
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width - (i + 1) * life_rect.width, height - life_rect.height))

            # 绘制炸弹数
            bomb_text = bomb_font.render("×%d" % bomb_num, True, DARK_RED)
            text_rect = bomb_text.get_rect()
            bomb_icon_x = icon_margin
            bomb_icon_y = height - icon_margin - bomb_icon.get_height()
            screen.blit(bomb_icon, (bomb_icon_x, bomb_icon_y))
            screen.blit(bomb_text, (bomb_icon_x + bomb_icon.get_width() + 5,
                                    bomb_icon_y + bomb_icon.get_height() // 2 - text_rect.height // 2))

            # 绘制子弹补给数
            bullet_supply_text = bomb_font.render("×%d" % bullet_supply_num, True, BLUE)
            bullet_icon_x = icon_margin + 90
            bullet_icon_y = height - icon_margin - bullet_supply_icon.get_height()
            screen.blit(bullet_supply_icon, (bullet_icon_x, bullet_icon_y))
            screen.blit(bullet_supply_text, (bullet_icon_x + bullet_supply_icon.get_width() + 5,
                                             bullet_icon_y + bullet_supply_icon.get_height() // 2 - text_rect.height // 2))

            # 绘制分数
            score_text = score_font.render("Score : %s" % str(score), True, (255, 255, 255))
            screen.blit(score_text, (10, 5))

            # 绘制减速效果提示
            if is_slow:
                remain_ms = slow_end_time - pygame.time.get_ticks()
                remain_sec = max(0, int(remain_ms / 1000) + 1)
                slow_text = score_font.render(f"slowing time: {remain_sec}s", True, YELLOW)
                screen.blit(slow_text, (width - 290, 5))

        # 游戏结束判断
        elif life_num == 0:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(SUPPLY_TIME,0)

            if not recorded:
                recorded = True
                # 读取历史最高分数，若分数高于最高分则存档
                with open("record.txt", "r") as f:
                    record_score = int(f.read())
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))

            # 绘制结束画面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (width - again_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    background = background_base[0]
                    main(mode)
                # 如果用户点击“结束游戏”
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

        # 绘制暂停按钮
        screen.blit(paused_image,paused_rect)

        # 用于延迟飞机绘制频率（降帧）
        if not (delay % 8):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100


        pygame.display.flip() # 刷新屏幕
        clock.tick(60)

def select_mode():
    gamename_font = pygame.font.Font("font/Jersey10-Regular.ttf", 96)
    select_font = pygame.font.Font("font/Jersey10-Regular.ttf", 48)
    tip_font = pygame.font.Font("font/Jersey10-Regular.ttf", 24)
    gamename_text = gamename_font.render("Star Craft", True, (242,197,92))
    single_text = select_font.render("1. Single Player", True, (255, 255, 255))
    double_text = select_font.render("2. Two Players", True, (255, 255, 255))
    tip_text = tip_font.render("Press 1 or 2 to select mode", True, (216,65,70))
    main_bg = pygame.image.load("images/main_interface.png").convert()
    # 闪烁控制变量
    show_tip = True
    tip_timer = 0
    tip_interval = 90  # 闪烁间隔帧数，大幅降低闪烁频率
    # 播放选择界面BGM（确保在主循环前播放）
    pygame.mixer.music.load("sound/game_music.mp3")
    pygame.mixer.music.play(-1)
    # 移除闪烁特效，tip文字每帧都显示
    while True:
        screen.blit(main_bg, (0, 0))
        screen.blit(gamename_text, ((width - single_text.get_width() - 180), height // 3 - 100))
        screen.blit(single_text, ((width - single_text.get_width()) // 2, height // 3 + 80))
        screen.blit(double_text, ((width - double_text.get_width()) // 2, height // 3 + 160))
        screen.blit(tip_text, ((width - tip_text.get_width()) // 2, height // 3 + 260))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_1 or event.key == K_2):
                pygame.mixer.music.stop()  # 进入游戏时停止BGM
                if event.key == K_1:
                    return 1
                elif event.key == K_2:
                    return 2

if __name__ == "__main__":
    try:
        mode = select_mode()  # 选择模式
        main(mode)            # 把模式参数传给 main
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()