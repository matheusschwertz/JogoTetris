import pygame
import random
from Main import menu
from enum import Enum

background = pygame.image.load('data/fundo.png')


#largura do bloco e altura do bloco
block_size = 30 
#quantidade de linhas
rows = 10 
#quantidade de colagens
colls = 20

#tamanho da grade
play_width = rows * block_size 
play_height = colls * block_size 

#tamanho da janela
window_width = 1366
window_height = 800 

#iniciar grade x posição
top_left_x = (window_width - play_width) // 2  
#iniciar grade y posição
top_left_y = window_height - play_height - 100 

#Formas

I = [['0000'],

     ['0',
      '0',
      '0',
      '0']]

O = [['00',
      '00',]]

J = [['0..',
      '000'],

     ['00',
      '0.',
      '0.'],

     ['000',
      '..0'],

     ['.0',
      '.0',
      '00']]

L = [['..0',
      '000'],

     ['0.',
      '0.',
      '00'],

     ['000',
      '0..'],

     ['00',
      '.0',
      '.0']]

T = [['.0.',
      '000'],

     ['0.',
      '00',
      '0.'],

     ['000',
      '.0.'],

     ['.0',
      '00',
      '.0']]

S = [['.00',
      '00.'],

     ['0.',
      '00',
      '.0']]

Z = [['00.',
      '.00'],

     ['.0',
      '00',
      '0.']]

shapes = [I,O,J,L,T,S,Z]
#cores
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

#enum game state
class State(Enum):
    play = 'play'
    pause = 'pause'
    game_over = 'game_over'

class Piece:
    def __init__(self,x,y,shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(shape_colors)
        self.rotation = 0

def fall(shape,grid):
    ''' abaixe o bloco para baixo'''

    while check_free_space(shape,grid):
        shape.y += 1

    return shape.y - 1

def check_game_over(positions):
    ''' se algum bloco atingiu o limite superior retorna True senão retorna False '''

    for pos in positions:
        x , y = pos

        if y == 0:
            return True 

    return False 

def check_free_space(shape,grid):
    ''' Esta função retorna A forma verdadeira não colide com a borda ou outra forma '''

    #obter todos os espaços livres da grade
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]

    #converter de lista 2d para lista 1d
    accepted_pos = [j for i in accepted_pos for j in i]

    #converter a forma atual em coordenadas
    form = convert_shape_to_position(shape)

    #verifique as coordenadas 
    for pos in form:
        if pos not in accepted_pos and pos[1] >= 0:
            return False

    return True

def convert_shape_to_position(shape):
    ''' converter forma em coordenadas '''

    position = [] 

    #obter um tipo de forma
    form = shape.shape[shape.rotation % len(shape.shape)]

    #obter uma altura de forma 
    shape_height = len(form)

    #converter forma em coordenadas
    for i , line in enumerate(form):
        row = list(line)
        for j , column in enumerate(row):
            if column == '0':
                position.append((shape.x + j,shape.y + i))

    for i in range(len(position)):
        position[i] = (position[i][0] - 1,position[i][1] - shape_height)

    return position

def create_new_shape():
    ''' create new random shape '''

    return Piece(rows // 2,0,random.choice(shapes))

def create_grid(positions = {}):
    ''' criar nova forma aleatória '''

    #criar grade vazia
    grid = [[(0,0,0) for _ in range(rows)] for _ in range(colls)]

    #grade preenchida
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in positions:
                grid[i][j] = positions[(j,i)]

    return grid

def draw_grid_lines(window):
	''' desenhar linhas de grade cinza '''

	silver_color = (128,128,128)

	for i in range(colls):
		for j in range(rows):
			pygame.draw.rect(window,silver_color,(j * block_size + top_left_x,i * block_size + top_left_y,block_size,block_size),1)

def draw_grid(window,grid):
    ''' desenhar grade '''

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            rect = (top_left_x + j * block_size,top_left_y + i * block_size,block_size,block_size)
            color = grid[i][j]
            pygame.draw.rect(window,color,rect)

def draw_grid_border(window):
    ''' desenhar borda ao redor da grade'''

	#parâmetros de borda
    silver_color = (128,128,128)
    rect = (top_left_x,top_left_y,play_width,play_height)
    border_width = 4

	#desenhar borda
    pygame.draw.rect(window,silver_color,rect,border_width)

def draw_main_title(window):
    ''' desenhar título principal '''

    #carregar fontes
    pygame.font.init()

    white_color = (255,255,255)

    #criar fonte
    font = pygame.font.SysFont('Arial Black',40)
    #criar rótulo
    label = font.render('TETRIS',1,white_color)
    #desenhar rótulo
    window.blit(label,(window_width / 2 - label.get_width() / 2,30))

def draw_pause(window):
    #carregar fonte
    pygame.font.init()

    white_color = (255,255,255)

    #criar fonte
    font = pygame.font.SysFont('Arial Black',40)
    #criar rótulo
    label = font.render('Pause',1,white_color)
    #desenhar rótulo
    window.blit(label,(window_width / 2 - label.get_width() / 2,window_height / 2 - label.get_height()))

def draw_game_over(window):
    #carregar fontes
    pygame.font.init()

    white_color = (255,255,255)

    #criar fonte
    font = pygame.font.SysFont('Arial Black',40)
    #criar rótulo
    label = font.render('Perdeu!Pressione qualquer tecla...',1,white_color)
    #desenhar rótulo
    window.blit(label,(window_width / 2 - label.get_width() / 2,window_height / 2 - label.get_height()))

def draw_next_shape(window,shape):
    #carregar fonte
    pygame.font.init()

    white_color = (255,255,255)

    #criar fonte
    font = pygame.font.SysFont('Arial Black',20)
    #criar rótulo
    label = font.render('próxima peça:',1,white_color)

    form = shape.shape[shape.rotation % len(shape.shape)] 

    #coordenadas de início
    start_x = top_left_x + play_width + 100 
    start_y = window_height / 2 - 100

    #desenhar forma
    for i , line in enumerate(form):
        row = list(line)
        for j , column in enumerate(row):
            if column == '0':
                pygame.draw.rect(window,shape.color,
                    (start_x + j * block_size,start_y + i * block_size,block_size,block_size))
                pygame.draw.rect(window,(128,128,128),
                    (start_x + j * block_size,start_y + i * block_size,block_size,block_size),2)

    #desenhar rótulo
    window.blit(label,(start_x - 20,start_y - 50))

def draw_score(window,score):
    #carrega fontes
    pygame.font.init()

    white_color = (255,255,255)

    start_x = top_left_x + play_width + 95
    start_y = window_height / 2 - 100

    #criar fonte
    font = pygame.font.SysFont('Arial Black',20)
    #criar rótulo
    label = font.render('Pontuação:' + str(score),1,white_color)
    #desenhar rótulo
    window.blit(label,(start_x,window_height / 2 + 50))

def clear_rows(grid,positions):
    ''' limpar linhas preenchidas '''

    index = 0
    flag = False
    height = 0

    for i in range(len(grid) -1,-1,-1):
        row = grid[i]
        if (0,0,0) not in row:

            flag = True

            index = i
            height += 1

            for j in range(len(row)):
                try:
                    del positions[(j,i)]
                except:
                    continue

    if flag:
        for i in range(index - 1,-1,-1):
            for j in range(rows):
                if (j,i) in positions:
                    color = positions[(j,i)]
                    del positions[(j,i)]
                    positions[(j,i + height)] = color

    return height * 200  

def draw_window(window,grid,game_state,next_shape,score):
    window.fill((0,0,0)) 

    #desenhar título principal
    draw_main_title(window)

    #desenhar grade
    draw_grid(window,grid)

    #desenhar grade não preenchida de prata na grade
    draw_grid_lines(window)

    #desenhar borda ao redor da grade
    draw_grid_border(window)

    #desenhe a próxima forma à direita
    draw_next_shape(window,next_shape)

    #desenhar score
    draw_score(window,score)

    #desenhar rótulo pausa
    if game_state == State.pause:
        draw_pause(window)

    #desenhar rótulo game over
    if game_state == State.game_over:
        draw_game_over(window)

    #tela de atualização
    pygame.display.update()

def main(window):
    pygame.init()
    pygame.mixer.music.load("data/trilha tetris.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1) 

    #criar janela
    window = pygame.display.set_mode((window_width,window_height))

    #criar grade
    grid = create_grid()

    positions = {}

    #definir o estado do jogo
    game_state = State.play

    new_shape = False

    #criar forma atual
    current_shape = create_new_shape()

    #criar a próxima forma
    next_shape = create_new_shape()

    score = 0
    
    #velocidade de queda determinada
    fall_speed = 0.25

    fall_time = 0

    level_time = 0

    clock = pygame.time.Clock()

    while True:

        if game_state == State.play:

            #criar grade com blocos preenchidos
            grid = create_grid(positions)

            #obter o tempo desde a última atualização
            update_time = clock.tick(60)

            fall_time += update_time

            level_time += update_time

            #aumente a velocidade
            if level_time / 1000 > 5:
                level_time = 0
                if fall_speed > 0.15:
                    fall_speed -= 0.005

            #mover a forma para baixo
            if fall_time / 1000 > fall_speed:
                current_shape.y += 1 
                fall_time = 0

                #se a forma colidir com a borda ou outra forma
                if not check_free_space(current_shape,grid):
                    current_shape.y -= 1
                    new_shape = True

            #obter teclas pressionadas
            keys = pygame.key.get_pressed()

        	#manipulação de entrada
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    #vire à esquerda
                    if event.key == pygame.K_LEFT:
                        current_shape.x -= 1
                        if not check_free_space(current_shape,grid):
                            current_shape.x += 1

                    #mover para a direita
                    if event.key == pygame.K_RIGHT:
                        current_shape.x += 1
                        if not check_free_space(current_shape,grid):
                            current_shape.x -= 1

                    #girar
                    if event.key == pygame.K_UP:
                        current_shape.rotation += 1
                        if not check_free_space(current_shape,grid):
                            current_shape.rotation -= 1
                    
                    #orma de queda
                    if event.key == pygame.K_SPACE:
                        current_shape.y = fall(current_shape,grid)

                    #pause
                    if event.key == pygame.K_p:
                        game_state = State.pause

            #acelerar
            if keys[pygame.K_DOWN]:
                current_shape.y += 1 
                if not check_free_space(current_shape,grid):
                    current_shape.y -= 1

            #obter a posição da forma atual
            current_shape_position = convert_shape_to_position(current_shape)

            #adicionar forma atual à grade
            for i in range(len(current_shape_position)):
                x , y = current_shape_position[i]
                
                if y >= 0:
                  grid[y][x] = current_shape.color

                ''' crie uma nova forma, verifique se as linhas estão preenchidas, atualize a pontuação, defina a próxima forma '''
            if new_shape:
                for pos in current_shape_position:
                    p = (pos[0],pos[1])
                    positions[p] = current_shape.color

                new_shape = False
                current_shape = next_shape
                next_shape = create_new_shape()
                score += 10
                score += clear_rows(grid,positions)


            ''' se houver blocos na primeira linha, termine o jogo '''
            if check_game_over(positions):
                game_state = State.game_over

            #janela de desenho
            draw_window(window,grid,game_state,next_shape,score)

        elif game_state == State.pause:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                
                if event.type == pygame.KEYDOWN:

                    #continuar jogando
                    if event.key == pygame.K_p:
                        game_state = State.play

        elif game_state == State.game_over:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

                #voltar ao cardápio
                if event.type == pygame.KEYDOWN:
                    menu(window)
