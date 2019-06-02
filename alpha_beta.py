#    alpha_beta.py
#    minmax 알고리즘에 alpha_beta pruning 기법을 도입한 Ai7 클래스가 정의된 파일

from gomoku_constant import *
from evaluation_constant import *
import copy
import random


class Ai7:
    def __init__(self, board):
        self.goBoard = board
        self.searchSpaceState, self.searchSpace = self.getInitialSearchSpace()
        self.searchCandidate = copy.deepcopy(self.searchSpace)
        self.evaluationSpaceState, self.evaluationSpace = self.getInitialEvaluationSpace()
        self.stoneCnt = 1
        self.searchSize = 20
        pass

    # 초기 바둑판 한가운데를 기준으로 사방의 2칸을 탐색공간으로 설정하는 메소드
    def getInitialSearchSpace(self):
        board = []
        searchSpace = []
        for i in range(GO_BOARD_X_COUNT):
            board.append([EMPTY] * GO_BOARD_Y_COUNT)
        for i in range(int(GO_BOARD_X_COUNT / 2) - 2, int(GO_BOARD_X_COUNT / 2) + 3):
            for j in range(int(GO_BOARD_Y_COUNT / 2) - 2, int(GO_BOARD_Y_COUNT / 2) + 3):
                board[i][j] = True
                if i == j:
                    continue
                searchSpace.append((i, j))
        return board, searchSpace

    # 착수된 좌표를 기준으로 탐색 공간을 갱신하는 메소드
    def resetSearchSpace(self, x, y):
        self.searchSpaceState[x][y] = True
        length = len(self.searchCandidate)
        for i in range(length):
            if self.searchCandidate[i] == (x, y):
                del self.searchCandidate[i]
                break

        count = len(self.searchCandidate)
        if self.searchSize <= count:
            count = self.searchSize
        self.searchSpace = random.sample(self.searchCandidate, count)

        left = x - 2 if x - 2 >= 0 else 0
        right = x + 2 if x + 2 < GO_BOARD_X_COUNT else GO_BOARD_X_COUNT
        top = y - 2 if y - 2 >= 0 else 0
        bottom = y + 2 if y + 2 < GO_BOARD_Y_COUNT else GO_BOARD_Y_COUNT
        for i in range(left, right):
            for j in range(top, bottom):
                if self.searchSpaceState[i][j]:
                    continue
                self.searchSpaceState[i][j] = True
                self.searchCandidate.append((i, j))
                self.searchSpace.append((i, j))
        pass

    # 최초 바둑판 한가운데를 기준 사방으로 1칸 떨어진 공간을 평가함수가 적용될 공간으로 설정하는 메소드
    def getInitialEvaluationSpace(self):
        board = []
        evaluationSpace = []
        for i in range(GO_BOARD_X_COUNT):
            board.append([EMPTY] * GO_BOARD_Y_COUNT)
        for i in range(int(GO_BOARD_X_COUNT / 2) - 1, int(GO_BOARD_X_COUNT / 2) + 2):
            for j in range(int(GO_BOARD_Y_COUNT / 2) - 1, int(GO_BOARD_Y_COUNT / 2) + 2):
                board[i][j] = True
                evaluationSpace.append((i, j))
        return board, evaluationSpace

    # 착수된 좌표를 기준으로 평가함수가 적용될 공간을 갱신하는 메소드
    def resetEvaluationSpace(self, x, y):
        left = x - 1 if x - 1 >= 0 else 0
        right = x + 2 if x + 2 < GO_BOARD_X_COUNT else GO_BOARD_X_COUNT
        top = y - 1 if y - 1 >= 0 else 0
        bottom = y + 2 if y + 2 < GO_BOARD_Y_COUNT else GO_BOARD_Y_COUNT
        for i in range(left, right):
            for j in range(top, bottom):
                if self.evaluationSpaceState[i][j]:
                    continue
                self.evaluationSpaceState[i][j] = True
                self.evaluationSpace.append((i, j))
        pass

    # x, y 좌표에서 direction 방향으로 pattern 인자로 주어진 패턴이 존재하는지 확인하는 메소드
    def patternCheck(self, x, y, pattern, direction):
        if direction == HORIZONTAL and x >= GO_BOARD_X_COUNT - len(pattern) + 1:
            return False
        elif direction == VERTICAL and y >= GO_BOARD_Y_COUNT - len(pattern) + 1:
            return False
        elif direction == MAIN_DIAGONAL and\
                (x >= GO_BOARD_X_COUNT - len(pattern) + 1 or y >= GO_BOARD_Y_COUNT - len(pattern) + 1):
            return False
        elif direction == SUB_DIAGONAL and \
                (x < len(pattern) - 1 or y >= GO_BOARD_Y_COUNT - len(pattern) + 1):
            return False

        check = True
        for i in range(len(pattern)):
            nx = x + dx[direction] * i
            ny = y + dy[direction] * i
            if self.goBoard[nx][ny] != pattern[i]:
                check = False
                break
        return check

    # 필수로 방어를 해야하는 수가 있는지 확인하는 메소드
    def defenceCheck(self):
        retx, rety = (None, None)

        for t in self.evaluationSpace:
            x, y = t
            for i in range(4):  # 방향
                for p in AI_DEFENCE_PATTERN1:
                    if self.patternCheck(x, y, p, i):
                        loc = p.index(EMPTY)
                        retx = x + dx[i] * loc
                        rety = y + dy[i] * loc
                        return retx, rety

                for p in AI_DEFENCE_PATTERN2:
                    if self.patternCheck(x, y, p, i):
                        loc = p.index(EMPTY)
                        loc += p[loc + 1:].index(EMPTY)
                        loc += 1
                        retx = x + dx[i] * loc
                        rety = y + dy[i] * loc
                        return retx, rety

        return retx, rety

    # 끝내기 수가 존재하는지 확인하는 메소드
    def endGameCheck(self):
        retx, rety = (None, None)

        for t in self.evaluationSpace:
            x, y = t
            for i in range(4):  # 방향
                for p in AI_ENDGAME_PATTERN1:
                    if self.patternCheck(x, y, p, i):
                        loc = p.index(EMPTY)
                        retx = x + dx[i] * loc
                        rety = y + dy[i] * loc
                        return retx, rety

                for p in AI_ENDGAME_PATTERN2:
                    if self.patternCheck(x, y, p, i):
                        loc = p.index(EMPTY)
                        loc += p[loc + 1:].index(EMPTY)
                        loc += 1
                        retx = x + dx[i] * loc
                        rety = y + dy[i] * loc
                        return retx, rety

        return retx, rety

    # 오목판의 점수를 평가하는 평가함수
    def evaluate(self):
        ai_score = 0
        player_score = 0

        for k in self.evaluationSpace:
            x, y = k
            # AI 스코어 체크
            for i in range(4):  # 방향
                for p in range(len(AI_7PATTERNS)):
                    if self.patternCheck(x, y, AI_7PATTERNS[p], i):
                        ai_score += AI_7PATTERNS_SCORE[p]

                for p in range(len(AI_6PATTERNS)):
                    if self.patternCheck(x, y, AI_6PATTERNS[p], i):
                        ai_score += AI_6PATTERNS_SCORE[p]

                for p in range(len(AI_5PATTERNS)):
                    if self.patternCheck(x, y, AI_5PATTERNS[p], i):
                        ai_score += AI_5PATTERNS_SCORE[p]

                for p in range(len(AI_4PATTERNS)):
                    if self.patternCheck(x, y, AI_4PATTERNS[p], i):
                        ai_score += AI_4PATTERNS_SCORE[p]


            # 플레이어 스코어 체크
            for i in range(4):  # 방향
                for p in range(len(PLAYER1_7PATTERNS)):
                    if self.patternCheck(x, y, PLAYER1_7PATTERNS[p], i):
                        player_score += PLAYER1_7PATTERNS_SCORE[p]

                for p in range(len(PLAYER1_6PATTERNS)):
                    if self.patternCheck(x, y, PLAYER1_6PATTERNS[p], i):
                        player_score += PLAYER1_6PATTERNS_SCORE[p]

                for p in range(len(PLAYER1_5PATTERNS)):
                    if self.patternCheck(x, y, PLAYER1_5PATTERNS[p], i):
                        player_score += PLAYER1_5PATTERNS_SCORE[p]

                for p in range(len(PLAYER1_4PATTERNS)):
                    if self.patternCheck(x, y, PLAYER1_4PATTERNS[p], i):
                        player_score += PLAYER1_4PATTERNS_SCORE[p]

        return ai_score - player_score

    def minmaxWithAlphaBeta(self, alpha, beta, depth, player):
        if depth == 0 or self.stoneCnt == GO_BOARD_X_COUNT * GO_BOARD_Y_COUNT:
            return (self.evaluate(), None, None)
        if player == AI:
            maxValue = -INF
            x = 0
            y = 0
            for k in self.searchSpace:
                i, j = k
                if self.goBoard[i][j] == EMPTY:
                    self.goBoard[i][j] = AI
                    self.stoneCnt += 1
                    ret = self.minmaxWithAlphaBeta(alpha, beta, depth - 1, PLAYER1)
                    if ret[0] > maxValue:
                        maxValue = ret[0]
                        x = i
                        y = j
                        alpha = max(alpha, maxValue)
                    self.stoneCnt -= 1
                    self.goBoard[i][j] = EMPTY
                    if beta <= alpha:  # Beta Cut
                        break
            if depth == 2:
                return (maxValue, x, y)
            else:
                return (maxValue, None, None)
            pass
        else: # player == PLAYER1
            minValue = INF
            x = 0
            y = 0
            for k in self.searchSpace:
                i, j = k
                if self.goBoard[i][j] == EMPTY:
                    self.goBoard[i][j] = PLAYER1
                    ret = self.minmaxWithAlphaBeta(alpha, beta, depth - 1, AI)
                    if ret[0] < minValue:
                        minValue = ret[0]
                        x = i
                        y = j
                        beta = min(beta, minValue)
                    self.goBoard[i][j] = EMPTY
                    if beta <= alpha:  # Alpha Cut
                        break
            if depth == 2:
                return (minValue, x, y)
            else:
                return (minValue, None, None)
            pass

    # AI가 바둑판에 착수하는 메소드
    def placement(self):
        print("Search space size : \n", len(self.searchSpace))
        print("Evaluation space size : \n", len(self.evaluationSpace))

        x, y = self.endGameCheck()
        if x is None and y is None:
            x, y = self.defenceCheck()
        if x is None and y is None:
            place = self.minmaxWithAlphaBeta(-INF, INF, 2, AI)
            x = place[1]
            y = place[2]

        print("place stone at : ", x, y)
        self.goBoard[x][y] = AI
        self.stoneCnt += 1
        self.resetEvaluationSpace(x, y)
        self.resetSearchSpace(x, y)
        return x, y

    pass
