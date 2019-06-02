#    alpha_beta3.py
#    평가함수와 탐색공간을 개선한 버전.
#    탐색공간에 반드시 포함되어야 하는 좌표를 포함시키고,
#    평가공간에 들어가지 않아도 되는 좌표를 제거

from evaluation_constant import *
import random


class Ai10:
    def __init__(self, board):
        self.goBoard = board
        self.compulsoryState, self.compulsorySpace = self.getInitialCompulsorySpace()
        self.candidateState, self.candidateSpace = self.getInitialCandidateSpace()
        self.searchSpace = []
        self.evaluationSpaceState, self.evaluationSpace = self.getInitialEvaluationSpace()
        self.stoneCnt = 1
        self.searchSize = 20
        pass

    # 탐색 공간에 포함될 수 있는 좌표들을 모아 리스트로 반환하는 메소드
    def getInitialCandidateSpace(self):
        candidateState = []
        candidateSpace = []

        for i in range(GO_BOARD_X_COUNT):
            candidateState.append([False] * GO_BOARD_Y_COUNT)
        for i in range(int(GO_BOARD_X_COUNT / 2) - 2, int(GO_BOARD_X_COUNT / 2) + 3):
            for j in range(int(GO_BOARD_Y_COUNT / 2) - 2, int(GO_BOARD_Y_COUNT / 2) + 3):
                candidateState[i][j] = True
                if i == int(GO_BOARD_X_COUNT / 2) and j == int(GO_BOARD_Y_COUNT / 2):
                    continue
                if self.compulsoryState[i][j]:
                    continue
                candidateSpace.append((i, j))
        return candidateState, candidateSpace

    # 초기에 탐색공간에 반드시 포함되어야 하는 좌표를 리스트로 반환하는 메소드
    def getInitialCompulsorySpace(self):
        compulsoryState = []
        compulsorySpace = []

        for i in range(GO_BOARD_X_COUNT):
            compulsoryState.append([False] * GO_BOARD_Y_COUNT)
        compulsoryState[int(GO_BOARD_X_COUNT / 2)][int(GO_BOARD_Y_COUNT / 2)] = True

        for i in range(int(GO_BOARD_X_COUNT / 2) - 1, int(GO_BOARD_X_COUNT / 2) + 2):
            for j in range(int(GO_BOARD_Y_COUNT / 2) - 1, int(GO_BOARD_Y_COUNT / 2) + 2):
                compulsoryState[i][j] = True
                if i == int(GO_BOARD_X_COUNT / 2) and j == int(GO_BOARD_Y_COUNT / 2):
                    continue
                compulsorySpace.append((i, j))

        return compulsoryState, compulsorySpace

    # 탐색공간에 반드시 포함되어야 하는 좌표를 찾는 메소드
    def resetCompulsorySpace(self):
        for k in self.evaluationSpace:
            x, y = k
            # AI 필수 탐색지역 확인
            for i in range(4):  # 방향
                for p in AI_7PATTERNS:
                    if EMPTY not in p: continue
                    if self.patternCheck(x, y, p, i):
                        for j in range(len(p)):
                            if p[j] == EMPTY:
                                nx = x + dx[i] * j
                                ny = y + dy[i] * j
                                if self.compulsoryState[nx][ny]: continue
                                self.compulsoryState[nx][ny] = True
                                self.compulsorySpace.append((nx, ny))

                for p in AI_6PATTERNS:
                    if EMPTY not in p: continue
                    if self.patternCheck(x, y, p, i):
                        for j in range(len(p)):
                            if p[j] == EMPTY:
                                nx = x + dx[i] * j
                                ny = y + dy[i] * j
                                if self.compulsoryState[nx][ny]: continue
                                self.compulsoryState[nx][ny] = True
                                self.compulsorySpace.append((nx, ny))

                for p in AI_5PATTERNS:
                    if EMPTY not in p: continue
                    if self.patternCheck(x, y, p, i):
                        for j in range(len(p)):
                            if p[j] == EMPTY:
                                nx = x + dx[i] * j
                                ny = y + dy[i] * j
                                if self.compulsoryState[nx][ny]: continue
                                self.compulsoryState[nx][ny] = True
                                self.compulsorySpace.append((nx, ny))

                for p in AI_4PATTERNS:
                    if EMPTY not in p: continue
                    if self.patternCheck(x, y, p, i):
                        for j in range(len(p)):
                            if p[j] == EMPTY:
                                nx = x + dx[i] * j
                                ny = y + dy[i] * j
                                if self.compulsoryState[nx][ny]: continue
                                self.compulsoryState[nx][ny] = True
                                self.compulsorySpace.append((nx, ny))

            # 플레이어 필수 탐색지역 확인
            for i in range(4):  # 방향
                for p in PLAYER1_7PATTERNS:
                    if EMPTY not in p: continue
                    if self.patternCheck(x, y, p, i):
                        for j in range(len(p)):
                            if p[j] == EMPTY:
                                nx = x + dx[i] * j
                                ny = y + dy[i] * j
                                if self.compulsoryState[nx][ny]: continue
                                self.compulsoryState[nx][ny] = True
                                self.compulsorySpace.append((nx, ny))

                for p in PLAYER1_6PATTERNS:
                    if EMPTY not in p: continue
                    if self.patternCheck(x, y, p, i):
                        for j in range(len(p)):
                            if p[j] == EMPTY:
                                nx = x + dx[i] * j
                                ny = y + dy[i] * j
                                if self.compulsoryState[nx][ny]: continue
                                self.compulsoryState[nx][ny] = True
                                self.compulsorySpace.append((nx, ny))

                for p in PLAYER1_5PATTERNS:
                    if EMPTY not in p: continue
                    if self.patternCheck(x, y, p, i):
                        for j in range(len(p)):
                            if p[j] == EMPTY:
                                nx = x + dx[i] * j
                                ny = y + dy[i] * j
                                if self.compulsoryState[nx][ny]: continue
                                self.compulsoryState[nx][ny] = True
                                self.compulsorySpace.append((nx, ny))

                for p in PLAYER1_4PATTERNS:
                    if EMPTY not in p: continue
                    if self.patternCheck(x, y, p, i):
                        for j in range(len(p)):
                            if p[j] == EMPTY:
                                nx = x + dx[i] * j
                                ny = y + dy[i] * j
                                if self.compulsoryState[nx][ny]: continue
                                self.compulsoryState[nx][ny] = True
                                self.compulsorySpace.append((nx, ny))
        pass

    # 착수된 좌표를 기준으로 탐색 공간을 갱신하는 메소드
    def resetSearchSpace(self, x, y):
        self.candidateState[x][y] = True
        self.compulsoryState[x][y] = True

        if (x, y) in self.candidateSpace:
            i = self.candidateSpace.index((x, y))
            del self.candidateSpace[i]

        if (x, y) in self.compulsorySpace:
            i = self.compulsorySpace.index((x, y))
            del self.compulsorySpace[i]

        self.resetCompulsorySpace()

        left = x - 2 if x - 2 >= 0 else 0
        right = x + 2 if x + 2 < GO_BOARD_X_COUNT else GO_BOARD_X_COUNT
        top = y - 2 if y - 2 >= 0 else 0
        bottom = y + 2 if y + 2 < GO_BOARD_Y_COUNT else GO_BOARD_Y_COUNT
        for i in range(left, right):
            for j in range(top, bottom):
                if self.candidateState[i][j] or self.compulsoryState[i][j]:
                    continue
                if self.goBoard[i][j] != EMPTY:
                    continue
                self.candidateState[i][j] = True
                self.candidateSpace.append((i, j))

        length = len(self.compulsorySpace)
        if length < self.searchSize:
            count = len(self.candidateSpace)
            if count > self.searchSize - length:
                count = self.searchSize - length
            self.searchSpace = self.compulsorySpace + random.sample(self.candidateSpace, count)
        else:
            self.searchSpace = self.compulsorySpace

    # 초기 평가함수가 적용될 공간을 2차원 리스트로 반환해주는 메소드
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

    # 착수가 된 좌표를 기준으로 새로 평가함수에 반영되야하는 공간을 갱신하는 메소드
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

        length = len(self.evaluationSpace)
        k = 0
        while k < length:
            x, y = self.evaluationSpace[k]
            check = True
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if nx >= 0 and nx < GO_BOARD_X_COUNT and ny >=0 and ny < GO_BOARD_Y_COUNT:
                    if self.goBoard[x][y] != self.goBoard[nx][ny]:
                        check = False
                        break
            if check:
                print("deleted from eval space : ", x, y)
                del self.evaluationSpace[k]
                self.evaluationSpaceState[x][y] = False
                length -= 1
            else:
                k += 1

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
                    self.stoneCnt += 1
                    ret = self.minmaxWithAlphaBeta(alpha, beta, depth - 1, AI)
                    if ret[0] < minValue:
                        minValue = ret[0]
                        x = i
                        y = j
                        beta = min(beta, minValue)
                    self.stoneCnt -= 1
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
