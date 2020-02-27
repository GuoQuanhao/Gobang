import pygame
import numpy as np
import sys
from white import White
from black import Black
import cursors


def map_update(w_flag, s_flag, pos):
    if w_flag and s_flag:
        sound.play()
        pygame.draw.circle(screen, White.color, pos, White.radius, White.width)
    if not w_flag and s_flag:
        sound.play()
        pygame.draw.circle(screen, Black.color, pos, Black.radius, Black.width)


def result(matrix, num):
    over = False
    bg_color = (72, 61, 139)
    text_color = (255, 255, 255)
    result_font = pygame.font.SysFont('Arial', 40)
    white_rectangle = result_font.render("White is winner", True, text_color, bg_color)
    white_rectangle.set_alpha(200)
    black_rectangle = result_font.render("Black is winner", True, text_color, bg_color)
    black_rectangle.set_alpha(200)
    if num >= 9:
        for row in range(0, 11):
            for i in range(0, 11):
                calculate_area = matrix[row:row + 5, i:i + 5]
                if np.sum(calculate_area) >= 5:
                    if (np.trace(calculate_area) == 5 or np.trace(
                            np.fliplr(calculate_area)) == 5) or (
                            5 in sum(calculate_area[:, ]) or 5 in sum(calculate_area.T[:, ])):
                        matrix = np.zeros([15, 15], dtype=int)
                        over = True
                        white_win()
                        victory.play()
                    elif (np.trace(calculate_area) == 50 or np.trace(
                            np.fliplr(calculate_area)) == 50) or (
                            50 in sum(calculate_area[:, ]) or 50 in sum(calculate_area.T[:, ])):
                        matrix = np.zeros([15, 15], dtype=int)
                        over = True
                        black_win()
                        victory.play()
                    else:
                        over = False
    pygame.display.flip()
    return over


def white_win():
    button_color = (0, 0, 255)
    text_color = (255, 255, 255)
    start_font = pygame.font.SysFont('Arial', 30)
    img_button = start_font.render("White is WINNER", True, text_color, button_color)
    img_button.set_alpha(170)
    screen.blit(img_button, [screen.get_width() / 2 - img_button.get_width() / 2,
                             screen.get_height()/2 - img_button.get_height() / 2 - 30])
    pygame.display.flip()


def black_win():
    button_color = (0, 0, 255)
    text_color = (255, 255, 255)
    start_font = pygame.font.SysFont('Arial', 30)
    img_button = start_font.render("Black is WINNER", True, text_color, button_color)
    img_button.set_alpha(170)
    screen.blit(img_button, [screen.get_width() / 2 - img_button.get_width() / 2,
                             screen.get_height()/2 - img_button.get_height() / 2 - 30])
    pygame.display.flip()


def start_button():
    button_color = (0, 0, 255)
    text_color = (255, 255, 255)
    start_font = pygame.font.SysFont('Arial', 30)
    img_button = start_font.render("Start", True, text_color, button_color)
    screen.blit(img_button, [screen.get_width() / 5 - img_button.get_width() / 2,
                             screen.get_height() - 40])
    pygame.display.flip()


def back_button():
    button_color = (0, 0, 255)
    text_color = (255, 255, 255)
    start_font = pygame.font.SysFont('Arial', 30)
    img_button = start_font.render("Back", True, text_color, button_color)
    screen.blit(img_button, [screen.get_width() / 2 - img_button.get_width() / 2,
                             screen.get_height() - 40])
    pygame.display.flip()


def again_button():
    button_color = (0, 0, 255)
    text_color = (255, 255, 255)
    start_font = pygame.font.SysFont('Arial', 30)
    img_button = start_font.render("Again", True, text_color, button_color)
    screen.blit(img_button, [4 * screen.get_width() / 5 - img_button.get_width() / 2,
                             screen.get_height() - 40])
    pygame.display.flip()


chess_order = []
board_order = []

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 50)
    size = width, height = 535, 586
    screen = pygame.display.set_mode(size)
    screen.fill((255, 0, 0))
    background = pygame.image.load('picture/chessboard.png')
    game_icon = pygame.image.load('picture/logo.png')
    pygame.display.set_icon(game_icon)
    White = White()
    Black = Black()
    start_flag = False
    back_flag = False
    again_flag = False
    white_flag = True
    chess_over = False
    screen.blit(background, (0, 0))
    chess_board = np.zeros([15, 15], dtype=int)
    back_num = 0
    chess_num = 0
    black_num = 0
    white_num = 0
    position = (0, 0)
    clock = pygame.time.Clock()
    pygame.mixer.music.load('music/bg_music.mp3')
    pygame.mixer.music.play(-1, 0.0)
    sound = pygame.mixer.Sound('music/put_down.wav')
    click_sound = pygame.mixer.Sound('music/click.wav')
    forbidden = pygame.mixer.Sound('music/forbid.wav')
    victory = pygame.mixer.Sound('music/victory.wav')
    while True:
        clock.tick(60)
        again_button()
        start_button()
        back_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            x, y = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x in range(0, 536) and y in range(0, 537) and not start_flag:
                curs, mask = cursors.compile(cursors.text_no, 'X', '.')
                pygame.mouse.set_cursor((24, 24), (0, 0), curs, mask)
            elif start_flag and x in range(0, 536) and y in range(0, 537):
                curs, mask = cursors.compile(cursors.thickarrow_strings, 'X', '.')
                pygame.mouse.set_cursor((24, 24), (0, 0), curs, mask)
            else:
                curs, mask = cursors.compile(cursors.text_arrow, 'X', '.')
                pygame.mouse.set_cursor((24, 24), (0, 0), curs, mask)
            if not start_flag and event.type == pygame.MOUSEBUTTONDOWN and x in range(0, 536) and y in range(0, 537):
                forbidden.play()
            if chess_over and x in range(0, 536) and y in range(0, 537)and event.type == pygame.MOUSEBUTTONDOWN:
                forbidden.play()
            if chess_over and x in range(0, 536) and y in range(0, 537):
                curs, mask = cursors.compile(cursors.text_no, 'X', '.')
                pygame.mouse.set_cursor((24, 24), (0, 0), curs, mask)
            if click[0] == 1 and (x in range(81, 133) and y in range(546, 582)):
                click_sound.play()
                start_flag = True
            if click[0] == 1 and (x in range(240, 294) and y in range(546, 582)) and not start_flag:
                click_sound.play()
            if click[0] == 1 and (x in range(396, 459) and y in range(546, 582))and not start_flag:
                click_sound.play()
            if click[0] == 1 and (x in range(240, 294) and y in range(546, 582)) and start_flag and np.sum(chess_board) and not chess_over:
                click_sound.play()
                back_flag = True
            if click[0] == 1 and (x in range(240, 294) and y in range(546, 582)):
                click_sound.play()
            if click[0] == 1 and (x in range(396, 459) and y in range(546, 582))and start_flag:
                click_sound.play()
                again_flag = True
            if (x in range(0, 536) and y in range(0, 537)) and start_flag and not back_flag and not again_flag:
                x_chess = round((x - 23) / 35) * 35 + 23
                y_chess = round((y - 23) / 35) * 35 + 23
                x_board = round((x - 23) / 35)
                y_board = round((y - 23) / 35)
                position = (x_board, y_board)
                pos_chess = (x_chess, y_chess)
                if not chess_over:
                    if white_flag and position[0] in range(0,15) and position[1] in range(0,15):
                        if event.type == pygame.MOUSEBUTTONDOWN and not chess_board[position]:
                            map_update(white_flag, start_flag, pos_chess)
                            chess_order.append(pos_chess)
                            board_order.append(position)
                            chess_board[position] = 1
                            white_flag = bool(1 - white_flag)
                            chess_num += 1
                            chess_over = result(chess_board, chess_num)
                    else:
                        if position[0] in range(0,15) and position[1] in range(0,15):
                            if event.type == pygame.MOUSEBUTTONDOWN and not chess_board[position]:
                                map_update(white_flag, start_flag, pos_chess)
                                chess_order.append(pos_chess)
                                board_order.append(position)
                                chess_board[position] = 10
                                white_flag = bool(1 - white_flag)
                                chess_num += 1
                                chess_over = result(chess_board, chess_num)
            if start_flag and not back_flag and again_flag:
                chess_board = np.zeros([15, 15], dtype=int)
                chess_order.clear()
                board_order.clear()
                screen.blit(background, (0, 0))
                again_flag = False
                chess_over = False
            if start_flag and back_flag and not again_flag and not chess_over:
                if chess_order:
                    chess_board[board_order[-1]] = 0
                    pos_point = chess_order[-1]
                    back_bg1 = pygame.transform.chop(background, (0, 0, pos_point[0] - 11, pos_point[1] - 11))
                    back_bg2 = pygame.transform.rotate(back_bg1, 180)
                    back_bg3 = pygame.transform.chop(back_bg2,
                                                     (0, 0, back_bg2.get_width() - 22, back_bg2.get_height() - 22))
                    final_bg = pygame.transform.rotate(back_bg3, 180)
                    screen.blit(final_bg, (pos_point[0] - 11, pos_point[1] - 11))
                    chess_order.pop()
                    board_order.pop()
                    back_flag = False
        screen.blit(screen, (0, 0))
        pygame.display.update()
