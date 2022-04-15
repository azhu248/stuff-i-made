#TETRIS 
from audioop import add
import math
import copy
import random
from turtle import clear
import pygame
pygame.init()
pygame.key.set_repeat(200, 50)
dropspeed = pygame.time.Clock()
game_over = False
dis=pygame.display.set_mode((700, 700))
frame_blocks = []
active_blocks = []
placed_blocks = []
frame_blocks = []
rotation = 0 # 1 is one cw 2 is 180 3 is one ccw
score = 0
for x in range(10):
    frame_blocks.append([x, 20])
for y in range(-2, 20):
    frame_blocks.append([10, y])
for y in range(-2, 20):
    frame_blocks.append([-1, y])
print(frame_blocks, "frame")
block_list = [0, 1, 2, 3, 4, 5, 6]
blankbox = pygame.image.load("newbox.png")
filledbox = pygame.image.load("filledbox.png")
placedbox = pygame.image.load("placedblock.png")
for x in range(10):
    for y in range(20):
        dis.blit(blankbox, (x * 35, y * 35))
def check_line():
    global score
    count = 0
    clear_blocks = []
    global placed_blocks
    rows_delete = set()
    for x in range(20):
        clear_blocks.clear()
        count = 0
        for y in placed_blocks:
            if x == y[1]:
                count += 1
                clear_blocks.append(y)
            if count == 10:
                rows_delete.add(x)
                placed_blocks = [x for x in placed_blocks if x not in clear_blocks]
    for row in rows_delete:
        score += 100
        for block in placed_blocks:
            if block[1] < row:
                block[1] += 1
def ui():
    blank = pygame.draw.rect(dis, (0, 0, 0), pygame.Rect(350, 0, 350, 700))
    score_font = pygame.font.SysFont('freesansbold', 50)
    score_surface = score_font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect()
    score_rect.center = (600, 150)
    dis.blit(score_surface, score_rect)

def clearboard():
    for x in range(10):
        for y in range(20):
            dis.blit(blankbox, (x * 35, y * 35))
def printboard():
    for block in placed_blocks:
        dis.blit(placedbox, (block[0] * 35, block[1] * 35))
    for block in active_blocks[0:4]:
        dis.blit(filledbox, (block[0] * 35, block[1] * 35))
def makeblock():
    global active_blocks
    global block_id
    global rotation
    global block_list
    if len(block_list) == 0:
        block_list = [0, 1, 2, 3, 4, 5, 6]
    x = random.randrange(len(block_list))
    block_id = block_list.pop(x)
    print(block_list, block_id)
    match block_id:
        case 0: gen_block = [[4, -1], [5, -1], [6, -1], [7, -1], [5.5, -1.5]] #line
        case 1: gen_block = [[5, -1], [5, -2], [6, -1], [6, -2]] #square
        case 2: gen_block = [[4, -1], [4, -2], [5, -1], [6, -1]] #j piece
        case 3: gen_block = [[4, -1], [6, -1], [5, -1], [6, -2]] #l piece
        case 4: gen_block = [[4, -1], [5, -2], [5, -1], [6, -2]] #s piece
        case 5: gen_block = [[4, -2], [5, -2], [5, -1], [6, -1]] #z piece
        case 6: gen_block = [[4, -1], [5, -2], [5, -1], [6, -1]] #t piece
    active_blocks = gen_block.copy()
    rotation = 0
def rotate_block(theta): 
    global active_blocks
    global rotation
    veto = False
    pre_rotate_blocks = copy.deepcopy(active_blocks)
    if block_id == 0:
        origin = active_blocks[4]
    if block_id != 0 and block_id != 1:
        origin = active_blocks[2]
    if block_id != 1:
        for coord in enumerate(active_blocks):
            x = coord[1][0] - origin[0]
            y = (coord[1][1] - origin[1]) 
            x_prime = math.cos(theta) * x - math.sin(theta) * y
            y_prime = math.sin(theta) * x + math.cos(theta) * y
            # print(x, y, x_prime, y_prime)
            # print(active_blocks)
            active_blocks[coord[0]][0] = round(origin[0] + x_prime, 1)
            active_blocks[coord[0]][1] = round(origin[1] + y_prime, 1)
    if kick_table_veto() == True:
        # if block_id != 0 and block_id != 1:
        #     for coord in active_blocks:
        #         coord[0] -= 1
        #     if kick_table_veto():
        #         for coord in active_blocks:
        #             coord[1] -= 1
        #         if kick_table_veto():
        #             for coord in active_blocks:
        #                 coord[0] += 1
        #                 coord[1] += 3
        if not kick_table(theta):
            active_blocks = pre_rotate_blocks.copy()
            veto = True
    if veto == False:
        if theta == math.pi/2:
            if rotation == 3:
                rotation = 0
            else:
                rotation += 1
        if theta == -1 * math.pi/2:
            if rotation == 0:
                rotation = 3
            else:
                rotation -= 1
def kick_table_veto():
    for placedblock in placed_blocks:
        for block in active_blocks:
            if block == placedblock:
                return True
    for placedblock in frame_blocks:
        for block in active_blocks:
            if block == placedblock:
                return True
    return False
def kick_table(theta):
    if block_id != 0 and block_id != 1:
        if rotation == 0 and theta == math.pi/2:
            for block in active_blocks:
                block[0] -= 1
            if kick_table_veto():
                for block in active_blocks:
                    block[1] -= 1
                if kick_table_veto():
                    for block in active_blocks:
                        block[0] += 1
                        block[1] += 3
                    if kick_table_veto():
                        for block in active_blocks:
                            block[0] -= 1
                        if kick_table_veto():
                            return False
def moveblock_down():
    veto = False
    for placedblock in placed_blocks:
        for block in active_blocks:
            if block[1] + 1 == placedblock[1] and block[0] == placedblock[0]:
                veto = True
    for placedblock in frame_blocks:
        for block in active_blocks:
            if block[1] + 1 == placedblock[1] and block[0] == placedblock[0]:
                veto = True
    if not veto:
        for block in range(5):
            try:
                active_blocks[block][1] += 1
            except Exception:
                pass
def automovedown():
    global active_blocks
    for block in range(5):
        try:
            active_blocks[block][1] += 1
        except Exception:
            pass
def moveblock_side(dir):
    global active_blocks
    if dir == 0:
        veto = False
        for placedblock in placed_blocks:
            for block in active_blocks:
                if block[0] == placedblock[0] + 1 and block[1] == placedblock[1]:
                    veto = True
        for placedblock in frame_blocks:
            for block in active_blocks:
                if block[0] == placedblock[0] + 1 and block[1] == placedblock[1]:
                    veto = True
        if not veto:
            for block in range(5):
                try:
                    active_blocks[block][0] -= 1
                except Exception:
                    pass
    if dir == 1:
        veto = False
        for placedblock in placed_blocks:
            for block in active_blocks:
                if block[0] == placedblock[0] - 1 and block[1] == placedblock[1]:
                    veto = True
        for placedblock in frame_blocks:
            for block in active_blocks:
                if block[0] == placedblock[0] - 1 and block[1] == placedblock[1]:
                    veto = True
        if not veto:
            for block in range(5):
                try:
                    active_blocks[block][0] += 1
                except Exception:
                    pass
def solidify_blocks():
    global placed_blocks
    for block in active_blocks:
        for placedblock in placed_blocks:
            if block[1] == placedblock[1] - 1 and block[0] == placedblock[0]:
                placed_blocks = placed_blocks + active_blocks[0:4].copy()
                active_blocks.clear()
                makeblock()
    for block in active_blocks:
        for placedblock in frame_blocks:
            if block[1] == placedblock[1] - 1 and block[0] == placedblock[0]:
                placed_blocks = placed_blocks + active_blocks[0:4].copy()
                active_blocks.clear()
                makeblock()
makeblock()
dropcond = 0
while not game_over:

    ui()
    clearboard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moveblock_side(1)
            if event.key == pygame.K_LEFT:
                moveblock_side(0)
            if event.key == pygame.K_DOWN:
                moveblock_down()
            if event.key == pygame.K_SPACE:
                for x in range(22):
                    moveblock_down()
                solidify_blocks()
                check_line()
            if event.key == pygame.K_UP:
                rotate_block(math.pi/2)
            if event.key == pygame.K_z:
                rotate_block(-1 * math.pi/2)


   
    dropcond += 1
    if dropcond == 30:
        solidify_blocks()
        automovedown()
        check_line()
        dropcond = 0
    dropspeed.tick(60)
    
    printboard()
    pygame.display.update()
pygame.quit()
quit()# stuff-i-made
