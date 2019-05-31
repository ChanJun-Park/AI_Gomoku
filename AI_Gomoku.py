# TODO 3 x 3 반칙 on/off 기능 구현

import pygame, sys
from pygame.locals import *
from gomoku_constant import *
import minmax
import alpha_beta
import alpha_beta3

def main():
    global DISPLAYSURF, BASICFONT,\
    STONE_SELECT_SURF, STONE_SELECT_RECT, \
    NEW_SURF, NEW_RECT, \
    TURN_SURF, TURN_RECT, \
    P1_COLOR, P2_COLOR

    global turn

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Go Board Test')

    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    NEW_SURF, NEW_RECT = makeText('New', BLACK, WHITE, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)

    # 새 게임 단위 루프
    while True:
        P1_COLOR, P2_COLOR = selectStoneColor()
        if P1_COLOR == BLACK:
            turn = PLAYER1
        else:
            turn = PLAYER2

        # 바둑돌의 상태를 저장하는 2차원 리스트
        goBoard = getInitialBoard()


        # 흑돌(선수) 처리
        goBoard[int(GO_BOARD_X_COUNT / 2)][int(GO_BOARD_Y_COUNT / 2)] = turn
        turn = (PLAYER1 if turn == PLAYER2 else PLAYER2)

        stoneCnt = 1

        mousex = 0
        mousey = 0

        # 마지막에 착수된 좌표
        lastx = int(GO_BOARD_X_COUNT / 2)
        lasty = int(GO_BOARD_Y_COUNT / 2)

        drawBoard(goBoard, lastx, lasty)

        # AI 객체 생성 (여기서 난이도 조절?)
        ai = None
        level = selectLevel()
        if level == 1:
            ai = minmax.Ai1(goBoard)
        elif level == 2:
            ai = alpha_beta.Ai7(goBoard)
        else:
            ai = alpha_beta3.Ai10(goBoard)

        ai.resetEvaluationSpace(lastx, lasty)
        ai.resetSearchSpace(lastx, lasty)

        # 메인 게임 루프
        while True:
            DISPLAYSURF.fill(BGCOLOR)
            drawBoard(goBoard, lastx, lasty)

            # 게임 승패 판정
            gameState = finishCheck(goBoard, stoneCnt)
            if gameState != CONTINUE:
                drawFinishEvent(gameState)
                waitForNewGame()
                break

            #AI 차례 처리
            if turn == PLAYER2:
                lastx, lasty = ai.placement()
                stoneCnt += 1
                turn = (PLAYER1 if turn == PLAYER2 else PLAYER2)
                continue

            mouseClicked = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos
                    mouseClicked = True

            # 바둑판 위의 좌표
            boardx, boardy = getBoardPosAtPixel(mousex, mousey)
            if boardx != None and boardy != None:
                if not goBoard[boardx][boardy]:
                    drawPseudoStone(goBoard, boardx, boardy)
                if not goBoard[boardx][boardy] and mouseClicked:
                    lastx = boardx
                    lasty = boardy
                    goBoard[boardx][boardy] = turn
                    stoneCnt += 1
                    ai.stoneCnt += 1
                    ai.resetEvaluationSpace(boardx, boardy)
                    ai.resetSearchSpace(boardx, boardy)
                    turn = (PLAYER1 if turn == PLAYER2 else PLAYER2)
                    pass
                pass

            # 새 게임 버튼 처리
            if NEW_RECT.collidepoint(mousex, mousey):
                pygame.mouse.set_cursor(*HAND_CURSOR)
                if mouseClicked:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    break
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

            pygame.display.update()
        pass

# 프로그램을 종료시키는 함수
def terminate():
    pygame.quit()
    sys.exit()
    pass

# 텍스트 객체와 그에 대응하는 직사각형 객체를 반환하는 함수
def makeText(text, color, bgcolor, x, y):
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.center = (x, y)
    return (textSurf, textRect)

# 초기 바둑판 2차원 리스트를 반환하는 함수
def getInitialBoard():
    board = []
    for i in range(GO_BOARD_X_COUNT):
        board.append([EMPTY] * GO_BOARD_Y_COUNT)
    board[10][9] = board[2][1] = board[2][9]\
        = board[3][15] = board[5][4] = board[11][4]\
        = board[11][16] = board[15][2] = board[14][12]\
        = board[17][17] = RED_STONE
    return board

# 바둑판 좌표를 픽셀 좌표로 변환하여 반환하는 함수
def getPixelPosOfBoard(boardx, boardy):
    left = GO_BOARD_IMG_X + GO_BOARD_MARGIN + boardx * GO_BOARD_CELL_GAP
    top = GO_BOARD_IMG_Y + GO_BOARD_MARGIN + boardy * GO_BOARD_CELL_GAP
    return (left, top)

# 픽셀 좌표를 바둑판 좌표로 변환하여 반환하는 함수
def getBoardPosAtPixel(x, y):
    boardx = int((x - TOP_LEFT_X + STONE_RADIUS) / GO_BOARD_CELL_GAP)
    boardy = int((y - TOP_LEFT_Y + STONE_RADIUS) / GO_BOARD_CELL_GAP)
    if boardx >= 0 and boardx < 19 and boardy >=0 and boardy < 19:
        return (boardx, boardy)
    return (None, None)

# 바둑판과 새 게임 버튼을 화면에 그리는 함수
def drawBoard(board, lastX, lastY):
    DISPLAYSURF.blit(GO_BOARD_IMG, (GO_BOARD_IMG_X, GO_BOARD_IMG_Y))
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    for x in range(GO_BOARD_X_COUNT):
        for y in range(GO_BOARD_Y_COUNT):
            left, top = getPixelPosOfBoard(x, y)
            if board[x][y] == PLAYER1:
                pygame.draw.circle(DISPLAYSURF, P1_COLOR, (left, top), STONE_RADIUS, 0)
                pass
            elif board[x][y] == PLAYER2:
                pygame.draw.circle(DISPLAYSURF, P2_COLOR, (left, top), STONE_RADIUS, 0)
                pass
            elif board[x][y] == RED_STONE:
                pygame.draw.circle(DISPLAYSURF, RED, (left, top), STONE_RADIUS, 0)
                pass
    left, top = getPixelPosOfBoard(lastX, lastY)
    pygame.draw.circle(DISPLAYSURF, GRAY, (left, top), int(STONE_RADIUS/2), 0)
    pass

# 플레이어가 마우스로 위치 시키고 있는 바둑판 좌표를 표시해주는 함수
def drawPseudoStone(board, x, y):
    left, top = getPixelPosOfBoard(x, y)
    if board[x][y] == EMPTY:
        if turn == PLAYER1:
            pygame.draw.circle(DISPLAYSURF, P1_COLOR, (left, top), STONE_RADIUS, 2)
        else: # turn == PLAYER2
            pygame.draw.circle(DISPLAYSURF, P2_COLOR, (left, top), STONE_RADIUS, 2)
    pass

# 오목 게임의 승패를 판정 하는 함수
def finishCheck(board, cnt):
    # ↘ 오목 체크
    for x in range(GO_BOARD_X_COUNT - 4):
        for y in range(GO_BOARD_Y_COUNT - 4):
            if(board[x][y]==PLAYER1 and board[x+1][y+1]==PLAYER1 and board[x+2][y+2]==PLAYER1\
                    and board[x+3][y+3]==PLAYER1 and board[x+4][y+4]==PLAYER1) :
                return PLAYER1
            elif(board[x][y]==PLAYER2 and board[x+1][y+1]==PLAYER2 and board[x+2][y+2]==PLAYER2\
                    and board[x+3][y+3]==PLAYER2 and board[x+4][y+4]==PLAYER2) :
                return PLAYER2

    # → 오목 체크
    for x in range(GO_BOARD_X_COUNT - 4):
        for y in range(GO_BOARD_Y_COUNT):
            if (board[x][y] == PLAYER1 and board[x + 1][y] == PLAYER1 and board[x + 2][y] == PLAYER1 \
                    and board[x + 3][y] == PLAYER1 and board[x + 4][y] == PLAYER1):
                return PLAYER1
            elif (board[x][y] == PLAYER2 and board[x + 1][y] == PLAYER2 and board[x + 2][y] == PLAYER2 \
                  and board[x + 3][y] == PLAYER2 and board[x + 4][y] == PLAYER2):
                return PLAYER2

    # ↓ 오목 체크
    for x in range(GO_BOARD_X_COUNT):
        for y in range(GO_BOARD_Y_COUNT - 4):
            if (board[x][y] == PLAYER1 and board[x][y + 1] == PLAYER1 and board[x][y + 2] == PLAYER1 \
                    and board[x][y + 3] == PLAYER1 and board[x][y + 4] == PLAYER1):
                return PLAYER1
            elif (board[x][y] == PLAYER2 and board[x][y + 1] == PLAYER2 and board[x][y + 2] == PLAYER2 \
                  and board[x][y + 3] == PLAYER2 and board[x][y + 4] == PLAYER2):
                return PLAYER2

    # ↙ 오목 체크
    for x in range(4, GO_BOARD_X_COUNT):
        for y in range(GO_BOARD_Y_COUNT - 4):
            if (board[x][y] == PLAYER1 and board[x - 1][y + 1] == PLAYER1 and board[x - 2][y + 2] == PLAYER1 \
                    and board[x - 3][y + 3] == PLAYER1 and board[x - 4][y + 4] == PLAYER1):
                return PLAYER1
            elif (board[x][y] == PLAYER2 and board[x - 1][y + 1] == PLAYER2 and board[x - 2][y + 2] == PLAYER2 \
                  and board[x - 3][y + 3] == PLAYER2 and board[x - 4][y + 4] == PLAYER2):
                return PLAYER2

    # 무승부 판정
    if cnt == GO_BOARD_X_COUNT * GO_BOARD_Y_COUNT:
        return DRAW
    else:
        return CONTINUE
    pass

# 승패가 결정된 경우 결과를 화면에 표시해주는 함수
def drawFinishEvent(gameState):
    if gameState == PLAYER1:
        RESULT_SURF, RESULT_RECT = makeText('PLAYER1 WIN', BLACK, WHITE, WINDOWWIDTH - 170, 90)
    elif gameState == PLAYER2:
        RESULT_SURF, RESULT_RECT = makeText('PLAYER2(AI) WIN', BLACK, WHITE, WINDOWWIDTH - 170, 90)
    elif gameState == DRAW:
        RESULT_SURF, RESULT_RECT = makeText('DRAW', BLACK, WHITE, WINDOWWIDTH - 170, 90)

    DISPLAYSURF.blit(RESULT_SURF, RESULT_RECT)
    pygame.display.update()
    pass

# 승패가 결정된 뒤 사용자가 새 게임 버튼을 누를 때까지 기다리는 함수
def waitForNewGame():
    mousex = 0
    mousey = 0
    while True:
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

        if NEW_RECT.collidepoint(mousex, mousey):
            pygame.mouse.set_cursor(*HAND_CURSOR)
            if mouseClicked:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                break
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
    pass

# player1, player2 의 돌의 색깔을 선택하여 반환해준다.
def selectStoneColor():
    pygame.draw.rect(DISPLAYSURF, GRAY, (WINDOWWIDTH/2 - 200, WINDOWHEIGHT/2 - 200, 400, 400))
    OPTION_BLACK_SURF, OPTION_BLACK_RECT = makeText('Black', BLACK, GRAY, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 50)
    OPTION_WHITE_SURF, OPTION_WHITE_RECT = makeText('White', BLACK, GRAY, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 50)
    DISPLAYSURF.blit(OPTION_BLACK_SURF, OPTION_BLACK_RECT)
    DISPLAYSURF.blit(OPTION_WHITE_SURF, OPTION_WHITE_RECT)
    pygame.display.update()

    mousex = 0
    mousey = 0

    mouseClicked = False

    # 마우스 입력을 받을 때까지 대기
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mouseClicked = True
                mousex, mousey = event.pos


        if OPTION_BLACK_RECT.collidepoint(mousex, mousey):
            pygame.mouse.set_cursor(*HAND_CURSOR)
            if mouseClicked:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                return (BLACK, WHITE)
        elif OPTION_WHITE_RECT.collidepoint(mousex, mousey):
            pygame.mouse.set_cursor(*HAND_CURSOR)
            if mouseClicked:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                return (WHITE, BLACK)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
    pass

# 게임의 난이도를 선택하여 반환
def selectLevel():
    pygame.draw.rect(DISPLAYSURF, GRAY, (WINDOWWIDTH / 2 - 200, WINDOWHEIGHT / 2 - 200, 400, 400))
    LEVEL_ONE_SURF, LEVEL_ONE_RECT = makeText('Level 1', BLACK, GRAY, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 50)
    LEVEL_TWO_SURF, LEVEL_TWO_RECT = makeText('Level 2', BLACK, GRAY, WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    LEVEL_THREE_SURF, LEVEL_THREE_RECT = makeText('Level 3', BLACK, GRAY, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 50)
    DISPLAYSURF.blit(LEVEL_ONE_SURF, LEVEL_ONE_RECT)
    DISPLAYSURF.blit(LEVEL_TWO_SURF, LEVEL_TWO_RECT)
    DISPLAYSURF.blit(LEVEL_THREE_SURF, LEVEL_THREE_RECT)
    pygame.display.update()

    mousex = 0
    mousey = 0

    mouseClicked = False

    # 마우스 입력을 받을 때까지 대기
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mouseClicked = True
                mousex, mousey = event.pos

        if LEVEL_ONE_RECT.collidepoint(mousex, mousey):
            pygame.mouse.set_cursor(*HAND_CURSOR)
            if mouseClicked:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                return 1
        elif LEVEL_TWO_RECT.collidepoint(mousex, mousey):
            pygame.mouse.set_cursor(*HAND_CURSOR)
            if mouseClicked:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                return 2
        elif LEVEL_THREE_RECT.collidepoint(mousex, mousey):
            pygame.mouse.set_cursor(*HAND_CURSOR)
            if mouseClicked:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                return 3
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
    pass


if __name__ == "__main__":
    main()
