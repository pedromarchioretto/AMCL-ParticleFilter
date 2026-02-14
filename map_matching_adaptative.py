import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
MAP_WIDTH = 960
OFFSET_X = 960  
TILE_SIZE = 20

TOTAL_PONTOS_DESEJADO = 5000
LIMITE_MINIMO_PONTOS = 800    

LAYOUT = [
    "111111111111111111111111111111111111111111111111",
    "100000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000001",
    "101111111111110011111111111111001111111111111001",
    "101000000000010010000000000001001000000000001001",
    "101000000000010010000000000001001000000000001001",
    "101111001111110011111100111111001111110011111001",
    "100000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000001",
    "111111111100111111111111111111111111111111111111",
    "100000000100100000000000000000000000000000000001",
    "100000000100100000000000000000000000000000000001",
    "101111100100101111111111100111111111111111111001",
    "101000100100101000000000100100000000000000001001",
    "101000100100101000000000100100000000000000001001",
    "101100100100101011111100100101111111111111001001",
    "100000100100101010000100100101000000000001001001",
    "100000100100101010000100100101000000000001001001",
    "111001100100111010000100100101011111110011001001",
    "100000000100000010000100100101010000010010001001",
    "100000000100000010000100100101010000010010001001",
    "101111111111110011111100111101011110011111001001",
    "100000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000001",
    "111111111111111111111111111001111111111111111111",
    "100000000000000000000000010001000000000000000001",
    "100000000000000000000000010001000000000000000001",
    "101111111111111111111001110001011111111111111001",
    "101000000000000000001001000001010000000000001001",
    "101000000000000000001001000001010000000000001001",
    "101011111111111111001000000000010111111111001001",
    "101010000000000001001000000000010100000001001001",
    "101010000000000001001000000000010100000001001001",
    "101010111111110011001111111111110101111001001001",
    "101010100000010010000000000000000101000101001001",
    "101010100000010010000000000000000101000101001001",
    "101110101111010011111111111111111101110101001001",
    "100000101000010000000000000000000000010101001001",
    "100000101000010000000000000000000000010101001001",
    "111100111100111111111111111111111100111111001001",
    "100000000000000000000000000000000100000000001001",
    "100000000000000000000000000000000100000000001001",
    "101111111111111111111111111100111111111111001001",
    "101000000000000000000000000100100000000001001001",
    "101000000000000000000000000100100000000001001001",
    "101011111111111111111111100100111111110011001001",
    "101010000000000000000000100100000000010010001001",
    "101010000000000000000000100100000000010010001001",
    "101110111111111111111100111111111110011111001001",
    "100000000000000000000100000000000010000000001001",
    "100000000000000000000100000000000010000000001001",
    "100000000000000000000100000000000010000000000001",
    "100000000000000000000100000000000010000000000001",
    "111111111111111111111111111111111111111111111111"
]

def carregar_mapas():
    paredes_esq = []
    paredes_dir = []
    for r, row in enumerate(LAYOUT):
        for c, char in enumerate(row):
            if char == "1":
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                paredes_esq.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                paredes_dir.append(pygame.Rect(x + 960, y, TILE_SIZE, TILE_SIZE))
    return paredes_esq, paredes_dir

def reamostrar_pontos(sobreviventes):
    novos_pontos = list(sobreviventes)
    while len(novos_pontos) < TOTAL_PONTOS_DESEJADO and len(sobreviventes) > 0:
        pai = random.choice(sobreviventes)
        ruido_x = random.uniform(-15, 15)
        ruido_y = random.uniform(-15, 15)
        novos_pontos.append(pygame.Vector2(pai.x + ruido_x, pai.y + ruido_y))
    return novos_pontos

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

paredes_colisao, paredes_visuais_dir = carregar_mapas()
jogador = pygame.Rect(160, 280, 14, 14)
vel = 5

pontos_dir = []
for r, row in enumerate(LAYOUT):
    for c, char in enumerate(row):
        if char == "0":
            if random.random() < 0.3:
                x = (c * TILE_SIZE) + 960 + (TILE_SIZE // 2)
                y = (r * TILE_SIZE) + (TILE_SIZE // 2)
                pontos_dir.append(pygame.Vector2(x, y))

deslocamento_pontos = pygame.Vector2(0, 0)

while True:
    screen.fill((20, 20, 25)) 
    pos_antiga_x, pos_antiga_y = jogador.x, jogador.y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel
    jogador.x += dx
    for p in paredes_colisao:
        if jogador.colliderect(p):
            if dx > 0: jogador.right = p.left
            if dx < 0: jogador.left = p.right
    
    dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * vel
    jogador.y += dy
    for p in paredes_colisao:
        if jogador.colliderect(p):
            if dy > 0: jogador.bottom = p.top
            if dy < 0: jogador.top = p.bottom

    deslocamento_pontos.x += (jogador.x - pos_antiga_x)
    deslocamento_pontos.y += (jogador.y - pos_antiga_y)

    pygame.draw.rect(screen, (35, 35, 40), (0, 0, 960, 1080))    
    pygame.draw.rect(screen, (30, 30, 35), (960, 0, 960, 1080)) 

    for p in paredes_colisao:
        pygame.draw.rect(screen, (100, 105, 120), p)
    for p in paredes_visuais_dir:
        pygame.draw.rect(screen, (80, 85, 100), p)

    pontos_sobreviventes = []
    for p_pos in pontos_dir:
        x_atual = int(p_pos.x + deslocamento_pontos.x)
        y_atual = int(p_pos.y + deslocamento_pontos.y)

        grid_x = (x_atual - 960) // TILE_SIZE
        grid_y = y_atual // TILE_SIZE

        colidiu = False
        if 0 <= grid_y < len(LAYOUT) and 0 <= grid_x < len(LAYOUT[0]):
            if LAYOUT[grid_y][grid_x] == "1":
                colidiu = True
        else:
            colidiu = True

        if not colidiu:
            pontos_sobreviventes.append(p_pos)
            pygame.draw.circle(screen, (255, 0, 0), (x_atual, y_atual), 2)

    pontos_dir = pontos_sobreviventes

    if 0 < len(pontos_dir) < LIMITE_MINIMO_PONTOS:
        pontos_dir = reamostrar_pontos(pontos_dir)

    pygame.draw.rect(screen, (0, 255, 150), jogador)
    pygame.draw.line(screen, (255, 255, 255), (960, 0), (960, 1080), 2)

    pygame.display.flip()
    clock.tick(60)