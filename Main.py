import pygame
import os
import Registration
import random
from enum import Enum
import SinglePlayer


# tamanho da janela

window_width = 1366
window_height = 768

background = pygame.image.load('data/fundo.png')


# botão escolhido enum


class Choosed(Enum):
    single = 'single_palyer'
    
    quit = 'quit'



def draw_title(window):
    ''' desemhar titulo '''

    # careegar fontes
    pygame.font.init()
    
    
    
    

    white_color = (255, 255, 255)

    # criar fonte
    font = pygame.font.SysFont('Arial Black', 60)
    # criar rotulo
    label = font.render('TETRIS', 1, white_color)
    # desenhar rotulo
    window.blit(label, (window_width / 2 - label.get_width() / 2, 60))


def draw_options(window):
    ''' desenhar pontos de menu '''

    # carregar fontes
    pygame.font.init()
    
   
    
    

    white_color = (255, 255, 255)

    # criar fonte
    font = pygame.font.SysFont('Times New Roman', 40)
    #font = pygame.font.Font(os.path.join('font','.ttf'), 40)

    # criar rótulo
    single_player_label = font.render('JOGAR', 1, white_color)
    # criar rótulo
    
    # criar rótulo
    quit_label = font.render('SAIR', 1, white_color)

    # desenhar rótulos

    window.blit(single_player_label, (window_width / 2 -
                single_player_label.get_width() / 2, 200))
    
    window.blit(quit_label, (window_width / 2 -
                quit_label.get_width() / 2, 280))


def draw_button_frames(window, choose):
    ''' desenhar quadros em torno de pontos de menu '''

    if choose == Choosed.single:
        r_w = 220
        rect = ((window_width - r_w) / 2, 200, r_w, 50)
    
    elif choose == Choosed.quit:
        r_w = 220
        rect = ((window_width - r_w) / 2, 280, r_w, 60)

    pygame.draw.rect(window, (128, 128, 128), rect, 4)


def draw_menu(window, choose):
    
    
    
    pygame.display.set_mode((window_width, window_height))
  
    
    window.fill((0, 0, 0))
    
    window.blit(background, (0, 0))
    
    
    
    
    # desenhar título
    draw_title(window)
    


    # desenhar pontos de menu
    draw_options(window)

    # desenhar quadros em torno de pontos de menu
    draw_button_frames(window, choose)

    # criar janela
    
    pygame.display.update()


def menu(window=None):
       
    pygame.init()

    
    
    # criar janela
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Tetris')
   
    
    # botão atual
    choosed_string = Choosed.single

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()
            

            if event.type == pygame.KEYDOWN:

                # botões de comutação
                if event.key == pygame.K_DOWN:
                    if choosed_string == Choosed.single:
                        choosed_string = Choosed.quit
                    
                    elif choosed_string == Choosed.quit:
                        choosed_string = Choosed.single

                # botões de comutação
                if event.key == pygame.K_UP:
                    if choosed_string == Choosed.single:
                        choosed_string = Choosed.quit
                    elif choosed_string == Choosed.quit:
                        choosed_string = Choosed.single
                    

                # executar botão
                if event.key == pygame.K_RETURN:

                    if choosed_string == Choosed.single:
                        SinglePlayer.main(window)

                   

                    if choosed_string == Choosed.quit:
                        pygame.display.quit()
                        quit()
        
        # desenhar menu
        draw_menu(window, choosed_string)


if __name__ == '__main__':
    menu()
