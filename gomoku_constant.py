import pygame


WINDOWWIDTH = 1000
WINDOWHEIGHT = 600

BASICFONTSIZE = 20
#the hand cursor
_HAND_CURSOR = (
"     XX         ",
"    X..X        ",
"    X..X        ",
"    X..X        ",
"    X..XXXXX    ",
"    X..X..X.XX  ",
" XX X..X..X.X.X ",
"X..XX.........X ",
"X...X.........X ",
" X.....X.X.X..X ",
"  X....X.X.X..X ",
"  X....X.X.X.X  ",
"   X...X.X.X.X  ",
"    X.......X   ",
"     X....X.X   ",
"     XXXXX XX   ")
_HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)

#색깔       R,   G,   B
BLACK  = (  0,   0,   0)
GRAY   = (200, 200, 200)
WHITE  = (255, 255, 255)
YELLOW = (255, 211,  21)
RED    = (255,   0,   0)

BGCOLOR = WHITE
TEXTCOLOR = BLACK

# 바둑판 이미지
GO_BOARD_IMG = pygame.image.load('go2.png')
GO_BOARD_WIDTH = 580
GO_BOARD_HEIGHT = 580
GO_BOARD_IMG_X = int(WINDOWWIDTH / 3) - int(GO_BOARD_WIDTH / 2)
GO_BOARD_IMG_Y = int(WINDOWHEIGHT / 2) - int(GO_BOARD_HEIGHT / 2)
GO_BOARD_MARGIN = 20
GO_BOARD_CELL_GAP = 30
GO_BOARD_X_COUNT = 19
GO_BOARD_Y_COUNT = 19
STONE_RADIUS = int(GO_BOARD_CELL_GAP / 2)

# 바둑판에서 (0,0)의 픽셀 좌표
TOP_LEFT_X = GO_BOARD_IMG_X + GO_BOARD_MARGIN
TOP_LEFT_Y = GO_BOARD_IMG_Y + GO_BOARD_MARGIN

# 바둑판 상태, PLAYER1이 인간, PLAYER2가 AI
EMPTY   = 0
PLAYER1 = 1
PLAYER2 = 2
AI = 2
RED_STONE = 3

# 게임 상태
CONTINUE = 3
DRAW = 4

INF = 2000000000

# 패턴 확인이 탐색 방향
HORIZONTAL = 0
VERTICAL = 1
MAIN_DIAGONAL = 2
SUB_DIAGONAL = 3

dx = (1, 0, 1, -1)
dy = (0, 1, 1,  1)