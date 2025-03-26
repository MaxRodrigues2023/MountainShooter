import pygame
from pygame import Surface
import random
import sys
from datetime import datetime
from pygame import Surface, Rect
from pygame.constants import K_RETURN, KEYDOWN, K_BACKSPACE, K_ESCAPE

from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
# import pygame import Surface, Rect
# import pygame.font import Font
from code.const import C_WHITE, C_GREEN, C_CYAN, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, EVENT_TIMEOUT, \
    TIMEOUT_STEP, TIMEOUT_LEVEL, C_YELLOW, SCORE_POS
from code.enemy import Enemy
from code.entity import Entity
from code.player import Player
from code.DBProxy import DBProxy

class Score:

    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        pass

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy('DBSCore')
        name = ''
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.score_text(48, 'YOU WIN!!!', C_GREEN, SCORE_POS['Title'])
            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = 'Enter Player 1  name (4 characters):'
            if game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = 'Enter Team name (4 characters):'
            # if game_mode == MENU_OPTION[2]:
            #     if player_score[0] >= player_score[1]:
            #         score = player_score[0]
            #         text = 'Enter Player 1 name (4 characters):'
            #     else:
            #         score = player_score[1]
            #         text = 'Enter Player 2 name (4 characters):'
            # self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()
            #     elif event.type == KEYDOWN:
            #         if event.key == K_RETURN and len(name) == 4:
            #             db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
            #             self.show()
            #         elif event.key == K_BACKSPACE:
            #             name = name[:-1]
            #         else:
            #             if len(name) < 4:
            #                 name += event.unicode
            # self.score_text(20, name, C_WHITE, SCORE_POS['Name'])
            # pygame.display.flip()
            else:  # MENU_OPTION[2]
                score = max(player_score)
                text = f'Enter Player {1 if player_score[0] >= player_score[1] else 2} name (4 characters):'

            self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])
            self.score_text(20, name, C_WHITE, SCORE_POS['Name'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
                        db_proxy.close()
                        self.show()  # Chama a tela de scores
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 4 and event.unicode.isalnum():
                        name += event.unicode.upper()

            pygame.display.flip()
            pass

    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)
        self.score_text(48, 'TOP 10 SCORE', C_YELLOW, SCORE_POS['Title'])
        self.score_text(20, 'NAME     SCORE       DATE       ', C_YELLOW, SCORE_POS['Label'])
        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for player_score in list_score:
            id_, name, score, date = player_score
            self.score_text(20, f'{name}     {score :05d}      {date}', C_YELLOW,
                            SCORE_POS[list_score.index(player_score)])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return

            pygame.display.flip()


    def score_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewrite", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"